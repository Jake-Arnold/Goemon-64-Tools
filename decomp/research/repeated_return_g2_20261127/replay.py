#!/usr/bin/env python3
"""Research only: reproduce isolated IDO -g2 return-tail matches at original VMAs."""
import argparse, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(args, cwd):
    return subprocess.check_output([str(x) for x in args], cwd=cwd, stderr=subprocess.STDOUT)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--upstream', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    repo, co = a.repo.resolve(), a.upstream.resolve()
    sys.path.insert(0, str(repo))
    from decomp.consolidated_batch_promotion import FLAGS, exact, glitch, probe, rels, text
    from scripts.harvest_cross_region import _get_asm_block
    from decomp import batch_registry as registry, promo36_promotion as predecessor
    assert run(['git', 'rev-parse', 'HEAD'], co).decode().strip() == '7e2029c5c7beca705e7ded2c8fa85a5a21d1c3ee'
    cc = co/'tools/ido-5.3/cc'
    compiler_sha = sha(cc.read_bytes())
    assert compiler_sha == '76d796c9591c9f5504949f85b29c32a6039a663791afe2f36f34ca18425b64d0'
    roms = {}
    for region, retail, expanded in [('usa','df8083a54296b8c151917c5333e1c85f014a2a66','6ea0ed71032ce08fc2745f412d84936382197494'), ('japan_0','9843ee979b5f6c80f5eda85df0baed9ae7c4e73b','6f8745fecc3a5e7d4918c7a73353eb0726116ded')]:
        r = (co/f'config/{region}/baserom.z64').read_bytes()
        e = (co/f'config/{region}/baserom.decompressed.z64').read_bytes()
        assert len(r) == 16777216 and hashlib.sha1(r).hexdigest() == retail
        assert len(e) == 33554432 and hashlib.sha1(e).hexdigest() == expanded
        roms[region] = e
    elf = co/'build/usa/mnsg.elf'
    assert (co/'build/usa/mnsg.z64').read_bytes() == roms['usa']
    assert sha(elf.read_bytes()) == '83eda0f1df831d997f9e505c92a8a7fdb55728d3ad28b30d224f5e1ae975a038'
    elf_symbols = run(['readelf','-Ws',elf],co).decode()
    combined = json.loads((repo/'decomp/results/combined.json').read_text())
    claims = combined['comparison']['functions']
    usa = {x['name'] for x in claims}
    base_inv = json.loads((repo/'decomp/results'/predecessor.JP_INV).read_text())
    jp = set(base_inv['previous_C_names']) | set(base_inv['new_C_names'])
    for b in registry.jp_batches(repo/'decomp'):
        jp.update(x['name'] for x in registry.batch_rows(b,'japan_0',repo/'decomp'))
    records = []
    for t in json.loads((HERE/'targets.json').read_text()):
        region, name, off, vma, z = (t[k] for k in ('region','name','rom_offset','vma','original_bytes'))
        assert name not in (usa if region == 'usa' else jp)
        if region == 'usa':
            assert not any(int(str(x['rom_offset']),0) < off+z and off < int(str(x['rom_offset']),0)+int(x['size']) for x in claims)
            matches = re.findall(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+FUNC\s+\S+\s+\S+\s+(\S+)\s+'+re.escape(name)+r'\s*$',elf_symbols,re.M)
            assert len(matches)==1 and int(matches[0][0],16)==vma and int(matches[0][1])==z
            # Reject an interior ELF symbol in the same original overlay/text section.
            for addr, size, typ, sec, sym in re.findall(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s*$',elf_symbols,re.M):
                assert not(sec==matches[0][2] and vma<int(addr,16)<vma+z and typ in ('FUNC','NOTYPE','OBJECT')), (name,sym)
        orig = roms[region][off:off+z]
        lines = probe.get_original_splat_lines(co/f'asm/{region}'/t['owner'],name,off,vma,z,orig)
        assert not probe.original_relocs(lines)
        header, body = _get_asm_block(co,region,t['owner'],name)
        folder = HERE/'sources'/region/name
        rec = dict(t, original_sha256=sha(orig), original_elf_extent_verified=region=='usa', attempts=[])
        with tempfile.TemporaryDirectory() as td:
            w = Path(td); ref = w/'reference.o'; (w/'reference.s').write_text(header+body)
            run(['mips-linux-gnu-as','-EB','-mtune=vr4300','-march=vr4300','-mabi=32','-Iinclude','-I.','-o',ref,w/'reference.s'],co)
            assert text(ref)[:z]==orig and not rels(ref)
            f = dict(t, relocation_count=0)
            for label, source, flags, want in [('default','candidate.c',list(FLAGS),False),('positive','candidate.c',list(FLAGS)+['-g2'],True),('negative','negative.c',list(FLAGS)+['-g2'],False)]:
                ledger = (repo/'decomp/COMPILER_QUIRKS.md').read_bytes()
                obj=w/(label+'.o'); src=folder/source
                run([cc,*flags,'-o',obj,src],co)
                b=text(obj); ok=exact(obj,ref,f)
                assert ok==want,(name,label)
                result=dict(label=label,source_sha256=sha(src.read_bytes()),flags=flags,ledger_sha256=sha(ledger),exact=ok,relocations_equal=rels(obj)==rels(ref),first_mismatch_offset=next((i for i in range(0,z,4) if b[i:i+4]!=orig[i:i+4]),None),compiler_quirk_outcome='NEW_REPRODUCIBLE_QUIRK' if label=='positive' else 'NO_NEW_COMPILER_FINDING')
                if ok:
                    glitch.check_nontext(obj)
                    linked=w/'linked.elf'; binary=w/'linked.bin'
                    script=w/'link.ld'; script.write_text('SECTIONS { .text '+hex(vma)+' : SUBALIGN(4) { *(.text) } }\n')
                    run(['mips-linux-gnu-ld','-EB','-m','elf32btsmip','-T',script,'-e',name,'-o',linked,obj],co)
                    run(['mips-linux-gnu-objcopy','-O','binary','-j','.text',linked,binary],co)
                    assert binary.read_bytes()[:z]==orig
                    syms=run(['readelf','-Ws',linked],co).decode()
                    assert re.search(r'^\s*\d+:\s+'+format(vma,'08x')+r'\s+'+str(z)+r'\s+FUNC\s+\S+\s+\S+\s+\S+\s+'+re.escape(name)+r'\s*$',syms,re.M|re.I)
                    result.update(linked_original_exact=True,linked_function_identity_exact=True,linked_code_sha256=sha(binary.read_bytes()[:z]))
                rec['attempts'].append(result)
        records.append(rec)
    report=dict(status='RESEARCH_ONLY',compiler_sha256=compiler_sha,canonical_usa=len(usa),canonical_japan=len(jp),records=records,whole_owner='NOT_RUN',candidate_full_rom='NOT_RUN',candidate_inventory='NOT_RUN',candidate_promotion_integrity='NOT_RUN')
    a.report.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS:',len(records),'isolated original-address IDO matches; canonical promotions: 0')

if __name__ == '__main__':
    main()

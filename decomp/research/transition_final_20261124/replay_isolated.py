from pathlib import Path
import sys,os,json,hashlib,re,subprocess,argparse
import isolated_usa_helpers as us, isolated_jp_helpers as jp
B=Path(__file__).resolve().parent
U=O=ledger=None
def run(region,src):
    # Pinned archive ledger: consult before each compile.
    led=ledger.read_bytes()[:60826];assert hashlib.sha1(b'blob '+str(len(led)).encode()+b'\0'+led).hexdigest()=='d38d51930c83c8c35682974da3a49e82b2acb76f';assert b'prototype compatibility' in led and b'source-line grouping' in led
    assert us.digest((U/'tools/ido-5.3/cc').read_bytes())==us.CC_SHA
    src=Path(src).resolve();obj=O/(src.stem+'.o');name,off,vma,size=('func_800030F0_3CF0',0x3cf0,0x800030f0,568) if region=='usa' else ('func_80003090_3C90',0x3c90,0x80003090,444)
    rom=(U/'config'/region/'baserom.decompressed.z64').read_bytes();assert us.digest(rom,'sha1')==(us.ROM_SHA if region=='usa' else jp.ROM_SHA);orig=rom[off:off+size]
    us.run([U/'tools/ido-5.3/cc',*us.FLAGS,'-o',obj,src],U)
    actual=us.link(obj,'3cf0',O,U)[0] if region=='usa' else jp.link(obj,name,vma,O,U)
    n=min(len(orig),len(actual));diff=[i for i in range(0,n,4) if orig[i:i+4]!=actual[i:i+4]];first=diff[0] if diff else (None if len(orig)==len(actual) else n)
    rr=us.reloc(obj,U);res=dict(region=region,variant=src.name,source_sha256=us.digest(src.read_bytes()),ledger_git_blob='d38d51930c83c8c35682974da3a49e82b2acb76f',generated_size=len(actual),matching_words=n//4-len(diff),total_words=size//4,first_mismatch=first,first_original=None if first is None else orig[first:first+4].hex(),first_generated=None if first is None else actual[first:first+4].hex(),linked_sha256=us.digest(actual),original_sha256=us.digest(orig),text_relocs=sum(rr.values()),classification='NO_NEW_COMPILER_FINDING',flags=us.FLAGS)
    (O/(src.stem+'.json')).write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res),flush=True)
    (O/(src.stem+'.orig')).write_bytes(orig);(O/(src.stem+'.actual')).write_bytes(actual)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--upstream',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--ledger',type=Path,required=True);p.add_argument('--region',choices=['usa','japan_0'],required=True);p.add_argument('source',type=Path,nargs='+');a=p.parse_args();U=a.upstream.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False);ledger=a.ledger.resolve();assert us.run(['git','rev-parse','HEAD'],U).strip()==us.UPSTREAM;assert not us.run(['git','status','--porcelain','--untracked-files=no'],U).strip()
 for s in a.source:run(a.region,s)

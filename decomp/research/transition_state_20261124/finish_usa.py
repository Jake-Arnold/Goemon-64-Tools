"""Continue a fresh successful USA2323 decomp.verify workdir to USA2324.
This invokes the exact same final stage as the canonical verifier, not a report
rewrite without native verification. Only use a disposable private checkout.
"""
import argparse,json
from pathlib import Path
from datetime import datetime,timezone
from decomp import verify,transition_promotion as tr,inventory

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--predecessor-report',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--uv',required=True);p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
    old=tr.read(a.predecessor_report);frozen=tr.read(tr.ROOT/'results/combined_2323_before_transition_20261124.json')
    tr.need(old['status']=='matched' and old['comparison']==frozen['comparison'] and old['sources_sha256_lf']==frozen['sources_sha256_lf'] and old['retained_assembly_functions']==frozen['retained_assembly_functions'] and old['usa_cright4_promotion']==frozen['usa_cright4_promotion'],'fresh USA2323 report differs from canonical predecessor')
    m=verify.load_manifest(tr.ROOT/'results/manifest_2323_before_transition_20261124.json');m[tr.KEY]={'format':tr.FORMAT};tr.validate_predecessor(m)
    w=a.work.resolve();co=w/'candidate';base=w/'baseline';rom=(base/'build/usa/mnsg.z64').read_bytes()
    verify.apply_transition_stage(co,base,w,a.uv,a.jobs,m,old,rom)
    old['verifier_source_sha256_lf']=tr.sha(Path(verify.__file__).read_bytes());old['ended_utc']=datetime.now(timezone.utc).isoformat();old['stage']='complete';old['status']='matched'
    inv=inventory.collect_inventory(base,co,m)
    for path,data in ((a.report,old),(a.inventory,inv)):
        with path.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    print('Fresh final USA2324 verifier continuation and upstream-relative strict inventory PASS')
if __name__=='__main__':main()

"""Restore authenticated original ABS NOTYPE metadata using existing guarded helper."""
from pathlib import Path
import subprocess
from decomp import native251_promotion as native

def restore(co,region,objects,old_globals,new_globals):
    removed=old_globals-new_globals;added=new_globals-old_globals
    if not removed and not added:return []
    expected={}
    for k,n in removed.items():
        if n!=1 or k[1:6]!=('0','NOTYPE','GLOBAL','DEFAULT','ABS'):raise ValueError('Unexpected global difference: '+str(k))
        other=(*k[:2],'OBJECT',*k[3:])
        if added[other]!=1:raise ValueError('Unexpected ABS metadata difference: '+str(k))
        expected[k[-1]]=k
    if len(expected)!=sum(added.values()):raise ValueError('Additional unexpected global differences')
    fixes=[];seen=set()
    for obj in objects:
        obj=Path(obj);syms=subprocess.check_output(['readelf','-Ws',str(obj)],text=True)
        for line in syms.splitlines():
            p=line.split()
            if len(p)!=8 or p[-1] not in expected or p[3:7]!=['OBJECT','GLOBAL','DEFAULT','UND']:continue
            name=p[-1];size=int(p[2],0);f=native.restore_undefined_type(obj,name,size,old_globals);fixes.append({'object':str(obj.relative_to(co)),**f});seen.add(name)
    if seen!=set(expected):raise ValueError('Missing original ABS input provenance: '+str(sorted(set(expected)-seen)))
    return fixes

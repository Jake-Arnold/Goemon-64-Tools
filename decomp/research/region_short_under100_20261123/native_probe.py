#!/usr/bin/env python3
"""Reproduce isolated IDO original-byte matches with negative controls; NOT full ROM G2."""
import argparse, hashlib, json, subprocess
from pathlib import Path
CASES=[
 ("usa","func_800352AC_35EAC",0x35EAC,64,"callback(task, task->data18);","callback(task, task->callback14);"),
 ("japan_0","func_801ECEC8_5A8E98",0x5A8E98,32,"state < 4","state < 5"),
 ("japan_0","func_801ECEE8_5A8EB8",0x5A8EB8,40,"character==0","character==1"),
 ("japan_0","func_801ECF10_5A8EE0",0x5A8EE0,48,"0xffff","0xfffe"),
 ("japan_0","func_801ECF40_5A8F10",0x5A8F10,40,"mode==184","mode==185"),
 ("japan_0","func_801ED030_5A9000",0x5A9000,40,"mode==185","mode==184")
]
SHA1={"usa":"6ea0ed71032ce08fc2745f412d84936382197494",
      "japan_0":"6f8745fecc3a5e7d4918c7a73353eb0726116ded"}
def compile_source(cc,objcopy,out,src,name):
    c=out/(name+".c");o=out/(name+".o");b=out/(name+".bin")
    c.write_text(src)
    subprocess.run([str(cc),"-c","-G","0","-non_shared","-O2","-mips2","-o",str(o),str(c)],check=True,capture_output=True)
    subprocess.run([str(objcopy),"-O","binary","-j",".text",str(o),str(b)],check=True,capture_output=True)
    return b.read_bytes()
def main():
    a=argparse.ArgumentParser()
    for k in ["ido","objcopy","usa-rom","jp-rom","out"]:
        a.add_argument("--"+k,type=Path,required=True)
    a=a.parse_args()
    rom={"usa":a.usa_rom.read_bytes(),"japan_0":a.jp_rom.read_bytes()}
    for k,v in rom.items():
        assert len(v)==33554432 and hashlib.sha1(v).hexdigest()==SHA1[k]
    a.out.mkdir(parents=True,exist_ok=False)
    result=[]
    for reg,name,offset,size,old,new in CASES:
        src=(Path(__file__).parent/"source"/(name+".c")).read_text()
        assert old in src
        original=rom[reg][offset:offset+size]
        pos=compile_source(a.ido,a.objcopy,a.out,src,name+"_positive")
        neg=compile_source(a.ido,a.objcopy,a.out,src.replace(old,new,1),name+"_negative")
        first=next((i for i in range(0,size,4) if original[i:i+4]!=neg[i:i+4]),None)
        passed=(pos[:size]==original and set(pos[size:])<={0} and first is not None)
        result.append({"name":name,"region":reg,"original_bytes":size,"native_exact":pos[:size]==original,"first_negative_mismatch":first,"pad_bytes":len(pos)-size,"source_sha256":hashlib.sha256(src.encode()).hexdigest(),"whole_ROM":"NOT_RUN"})
        print(reg,name,size,"PASS" if passed else "FAIL","negative",first)
        if not passed:raise SystemExit("FAILED_NATIVE "+name)
    (a.out/"summary.json").write_text(json.dumps(result,indent=2)+"\n")
if __name__=="__main__":main()

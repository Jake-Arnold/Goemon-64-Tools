"""Label an isolated pinned recomp build as live-speed enabled.

Prepare the pinned runtime with prepare_runtime and prepare_live_runtime first.
This edits the explicitly supplied source checkout; it does not build or launch.
"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import tempfile

PIN='6661abc439327b9ed9e235c391720f9034f61a78'
ANCHOR='    SDL_SysWMinfo wmInfo;'
ADDITION='    SDL_SetWindowTitle(window, "Goemon 64: Recompiled (live speed enabled)");\n\n'


def render_main(source):
    if source.count(ANCHOR)!=1 or 'Goemon 64: Recompiled (live speed enabled)' in source:
        raise ValueError('Recomp window source differs from expected pinned layout')
    return source.replace(ANCHOR,ADDITION+ANCHOR,1)


def prepare_title(root):
    root=Path(root).resolve(strict=True)
    revision=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    if revision!=PIN:raise ValueError('Recomp checkout is not at the verified commit')
    dirty=subprocess.check_output(['git','-C',str(root),'status','--porcelain','--','src/main/main.cpp'],text=True)
    if dirty.strip():raise ValueError('Recomp window source has local changes')
    source=root/'src/main/main.cpp'
    original=subprocess.check_output(['git','-C',str(root),'show','HEAD:src/main/main.cpp'],text=True).replace('\r\n','\n')
    data=source.read_text(encoding='utf-8')
    if data!=original:raise ValueError('Recomp window source differs from the pinned version')
    changed=render_main(data)
    temp=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',newline='\n',dir=source.parent,
                                         prefix='.goemon-title-',suffix='.tmp',delete=False) as f:
            f.write(changed);temp=Path(f.name)
        os.chmod(temp,source.stat().st_mode)
        os.replace(temp,source)
    finally:
        if temp is not None:temp.unlink(missing_ok=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recomp',type=Path)
    args=parser.parse_args(argv)
    prepare_title(args.recomp)
    print('Prepared live-speed window label; rebuild the recomp before use.')

if __name__=='__main__':main()

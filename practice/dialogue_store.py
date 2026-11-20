"""Per-user verified, persistent copies of original USA/JP Dialogue ROMs.

Never writes source files or the checkout. A retail import auto-decompresses
through the original file table and requires an exact original-image digest.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

from practice.dialogue_rom import USA_DECOMPRESSED_SHA1, ROM_SIZE
from practice.dialogue_japan import (JP_DECOMPRESSED_SHA1, JP_RETAIL_SHA1,
                                     normalise_japan_retail)

USA_RETAIL_SHA1='df8083a54296b8c151917c5333e1c85f014a2a66'
RETAIL_SIZE=16*1024*1024
HASHES={'usa':{'retail':USA_RETAIL_SHA1,'decompressed':USA_DECOMPRESSED_SHA1},
        'japan':{'retail':JP_RETAIL_SHA1,'decompressed':JP_DECOMPRESSED_SHA1}}
TABLE={'usa':0x57FD8,'japan':0x58258}
FIRST={'usa':0x576E00,'japan':0x57C5F0}
FILE_COUNT=1312


def library_root():
    if sys.platform=='win32':
        return Path(os.environ.get('LOCALAPPDATA') or Path.home()/'AppData'/'Local')/'GoemonSpeedrunTools'/'dialogue-roms'
    if sys.platform=='darwin':
        return Path.home()/'Library'/'Application Support'/'GoemonSpeedrunTools'/'dialogue-roms'
    return Path(os.environ.get('XDG_DATA_HOME') or Path.home()/'.local'/'share')/'GoemonSpeedrunTools'/'dialogue-roms'


def build_directory(root=None):
    path=Path(root) if root is not None else library_root()
    path=path/'built'
    path.mkdir(parents=True,exist_ok=True)
    return path


def stored_path(region,kind,*,root=None):
    if region not in HASHES or kind not in HASHES[region]:
        raise ValueError('Unsupported ROM region/kind')
    base=Path(root) if root is not None else library_root()
    return base / f'{region}-{kind}.z64'


def verify_stored(region,kind,*,root=None):
    """Do not trust a previously saved path/hash without checking bytes."""
    target=stored_path(region,kind,root=root)
    try:
        if target.is_symlink() or not target.is_file():
            return None
        if hashlib.sha1(target.read_bytes()).hexdigest()!=HASHES[region][kind]:
            return None
        return target
    except OSError:
        return None


def identify_original_rom(data: bytes):
    """Return region, kind, canonical bytes; unsupported/edited ROMs fail."""
    if len(data)==RETAIL_SIZE:
        if data[:4]==b'\x37\x80\x40\x12':
            return 'japan','retail',normalise_japan_retail(data)
        sha=hashlib.sha1(data).hexdigest()
        if sha==USA_RETAIL_SHA1:
            return 'usa','retail',data
        if sha==JP_RETAIL_SHA1:
            return 'japan','retail',data
    if len(data)==ROM_SIZE and data[:4]==b'\x80\x37\x12\x40':
        sha=hashlib.sha1(data).hexdigest()
        for region in HASHES:
            if sha==HASHES[region]['decompressed']:
                return region,'decompressed',data
    raise ValueError('Only SHA-1-pinned unmodified USA or Japan-0 retail/decompressed ROMs may be stored')


def decompress_original(retail: bytes, region: str):
    """ROMMY-compatible source-table decompression; exact SHA-1 required."""
    if region not in HASHES or hashlib.sha1(retail).hexdigest()!=HASHES[region]['retail']:
        raise ValueError('Retail ROM is not the pinned regional source')
    try:
        import lzkn64
    except ImportError as exc:
        raise RuntimeError('One-time retail ROM import requires lzkn64==0.2.0 (pip install lzkn64==0.2.0)') from exc
    table=TABLE[region]
    entries=[struct.unpack_from('>I',retail,table+4*i)[0] for i in range(FILE_COUNT+1)]
    if (entries[0]&0x7fffffff)!=FIRST[region] or entries[-1]!=0:
        raise ValueError('Unrecognised regional resource table')
    result=bytearray(retail[:FIRST[region]])
    starts=[]
    for i in range(FILE_COUNT):
        start=entries[i]&0x7fffffff
        end=(entries[i+1]&0x7fffffff) if i<FILE_COUNT-1 else start
        if not FIRST[region]<=start<=end<=len(retail):
            raise ValueError(f'Invalid compressed resource range {i}')
        starts.append(len(result))
        data=retail[start:end]
        if data and entries[i]&0x80000000:
            data=lzkn64.decompress(data)
        result.extend(data)
    if len(result)>ROM_SIZE:
        raise ValueError('Decompression exceeds 32 MiB')
    for i,start in enumerate(starts):
        struct.pack_into('>I',result,table+4*i,start)
    struct.pack_into('>I',result,table+FILE_COUNT*4,0)
    result.extend(b'\0'*(ROM_SIZE-len(result)))
    from practice.dialogue_repack import _update_usa_crc
    _update_usa_crc(result)  # Both pinned retail ROMs use CIC-6102.
    output=bytes(result)
    if hashlib.sha1(output).hexdigest()!=HASHES[region]['decompressed']:
        raise ValueError('Retail file did not decompress into the pinned original region image')
    return output


def _atomic_write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    file=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.goemon-import-',suffix='.tmp',delete=False) as staged:
            file=Path(staged.name)
            staged.write(data)
        os.chmod(file,0o600)
        os.replace(file,path)
    finally:
        if file is not None:file.unlink(missing_ok=True)


def import_rom(path, *, root=None):
    """Import a verified original once; retail import stores retail and decompressed.

    Validation and decompression finish BEFORE any storage write, avoiding
    partial unverified inputs. Does not automatically change active game ROM.
    """
    path=Path(path)
    region,kind,data=identify_original_rom(path.read_bytes())
    outputs={'retail':data} if kind=='retail' else {'decompressed':data}
    if kind=='retail':
        outputs['decompressed']=decompress_original(data,region)
    base=Path(root) if root is not None else library_root()
    base.mkdir(parents=True,exist_ok=True)
    try:os.chmod(base,0o700)
    except OSError:pass
    # Do not overwrite a source path if the import happened from our own library.
    for key,payload in outputs.items():
        target=stored_path(region,key,root=base)
        if path.resolve()==target.resolve():
            if hashlib.sha1(target.read_bytes()).hexdigest()!=HASHES[region][key]:
                raise ValueError('Existing stored ROM failed verification')
            continue
        _atomic_write(target,payload)
    return region,kind,stored_path(region,'decompressed',root=base)


def open_directory(path):
    """Open a directory using the host file manager, without a shell."""
    folder=Path(path)
    folder.mkdir(parents=True,exist_ok=True)
    if sys.platform=='win32':
        os.startfile(str(folder))
    elif sys.platform=='darwin':
        subprocess.Popen(['open',str(folder)],close_fds=True)
    else:
        subprocess.Popen(['xdg-open',str(folder)],close_fds=True)
    return folder


def drop_paths(root, data):
    """Decode the TkDND Tcl list, including braced filenames with spaces."""
    try:
        items=root.tk.splitlist(data)
    except (ValueError,TypeError) as exc:
        raise ValueError('Could not parse dropped paths') from exc
    paths=[Path(p) for p in items]
    if len(paths)!=1 or not paths[0].is_file():
        raise ValueError('Drop exactly one existing ROM file at a time')
    return paths[0]

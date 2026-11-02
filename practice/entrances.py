"""Read-only USA entrance atlas extraction and validated spawn specifications.

Schema provenance: pinned mn64rando 9c580d0, actor 08C and room metadata.
Only functional entrance parameters are cached locally; no ROM or room assets.
"""
from __future__ import annotations
from dataclasses import dataclass
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import struct
import tempfile
import os

US_RETAIL_SHA1 = 'df8083a54296b8c151917c5333e1c85f014a2a66'
US_DECOMPRESSED_SHA1 = '6ea0ed71032ce08fc2745f412d84936382197494'
SCHEMA = 'goemon-usa-entrance-atlas-v1'
MAX_STAGE = 0x1E3
CODE_RAM = 0x20D2A0
ROOM_POINTERS = 0x231300 - CODE_RAM


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def canonical_rom(data):
    if len(data) < 4 or len(data) % 4:
        raise ValueError('Invalid N64 ROM size')
    if data[:4] == bytes.fromhex('80371240'): return data
    output=bytearray(len(data))
    if data[:4] == bytes.fromhex('37804012'):
        output[0::2],output[1::2]=data[1::2],data[0::2]
    elif data[:4] == bytes.fromhex('40123780'):
        for i in range(4):output[i::4]=data[3-i::4]
    else: raise ValueError('Unrecognized N64 ROM byte order')
    return bytes(output)


def decompress_block(chunk, maximum=0x400000):
    if len(chunk)<4:raise ValueError('Truncated compressed file header')
    size=int.from_bytes(chunk[:4],'big')
    if not 4<=size<=len(chunk):raise ValueError('Compressed file length is outside its file span')
    source=chunk[4:size];out=bytearray();i=0
    def take(count):
        nonlocal i
        if i+count>len(source):raise ValueError('Truncated compression command')
        value=source[i:i+count];i+=count;return value
    while i<len(source):
        opcode=take(1)[0]
        if opcode==0 and i==len(source):out.extend(bytes(2))
        elif opcode<0x80:
            distance=((opcode&3)<<8)|take(1)[0];count=(opcode>>2)+2
            if distance>len(out):raise ValueError('Invalid compressed back-reference')
            for _ in range(count):out.append(out[-distance] if distance else 0)
        elif opcode<0xC0:out.extend(take(opcode&0x7F))
        elif opcode<0xE0:out.extend(take(1)*((opcode&0x1F)+2))
        else:
            count=take(1)[0]+2 if opcode==0xFF else (opcode&0x1F)+2
            out.extend(bytes(count))
        if len(out)>maximum:raise ValueError('Decompressed file exceeds limit')
    return bytes(out)


class RomFiles:
    def __init__(self, data):
        self.data=canonical_rom(data)
        self.sha1=hashlib.sha1(self.data).hexdigest()
        if self.sha1 not in (US_RETAIL_SHA1,US_DECOMPRESSED_SHA1):
            raise ValueError('Entrance extraction requires the verified original USA ROM or its verified decompressed build')
        signature=b'Nisitenma-Ichigo';start=self.data.find(signature)
        if start<0 or self.data.find(signature,start+1)>=0:raise ValueError('Ambiguous or missing ROM file table')
        start+=len(signature)
        self.pointers=struct.unpack_from('>1312I',self.data,start)
        self.cache={}

    def file(self,index):
        if type(index) is not int or not 1<=index<len(self.pointers):raise ValueError('File ID outside ROM table')
        if index in self.cache:return self.cache[index]
        pointer=self.pointers[index-1];start=pointer&0x7FFFFFFF;end=self.pointers[index]&0x7FFFFFFF
        if not 0<start<end<=len(self.data):raise ValueError('Invalid ROM file span')
        chunk=self.data[start:end]
        value=decompress_block(chunk) if pointer&0x80000000 else chunk
        self.cache[index]=value
        return value


@dataclass(frozen=True)
class Spawn:
    destination: int
    position: tuple[float,float,float]
    heading: int = 0
    mode: int = 0x10
    label: str = 'Saved position'
    entrance_id: str = ''

    def validate(self):
        if type(self.destination) is not int or not 0<=self.destination<=0xFFFF:raise ValueError('Invalid spawn map')
        if not isinstance(self.position,(list,tuple)) or len(self.position)!=3 or any(type(v) not in (int,float) or not math.isfinite(v) or not -32768<=v<=32767 for v in self.position):
            raise ValueError('Spawn position must fit the native signed 16-bit coordinate range')
        if type(self.heading) is not int or not 0<=self.heading<=0xFFFF or type(self.mode) is not int or not 0<=self.mode<=0xFFFF:
            raise ValueError('Invalid native spawn heading/mode')
        return self

    def pending_bytes(self):
        self.validate()
        return struct.pack('>HHhhhH',self.destination,self.mode,*(round(v) for v in self.position),self.heading)


def room_entrances(stage,file_id,room,instance,footer,ending):
    if not (0<=instance<=footer<ending<=len(room)) or instance%16 or ending-footer!=28:
        raise ValueError(f'Invalid room metadata for stage {stage}')
    dims=struct.unpack_from('>HHH',room,footer+20)
    cells=math.prod(dims)
    if cells>0x10000 or ending+cells*4>len(room):raise ValueError('Invalid room instance grid')
    starts={instance}
    for p in range(ending,ending+cells*4,4):
        word=struct.unpack_from('>I',room,p)[0]
        if word:
            if word>>16!=0x800:raise ValueError('Invalid instance group pointer')
            starts.add(word&0xFFFF)
    used=set()
    for start in starts:
        if not instance<=start<footer:raise ValueError('Instance group outside room bounds')
        p=start
        while True:
            if p+20>footer:raise ValueError('Unterminated actor instance group')
            record=room[p:p+20];p+=20
            if not any(record):break
            if record[12:14]!=b'\x08\x00':raise ValueError('Invalid actor instance header')
            index=int.from_bytes(record[14:16],'big')
            if index&15==0 and index>>4<instance//16:used.add(index>>4)
    result=[]
    for index in sorted(used):
        offset=index*16;record=room[offset:offset+16]
        if int.from_bytes(record[:2],'big')!=0x8C or not record[14]:continue
        destination,x,height,horizontal,heading=struct.unpack_from('>HhhhH',record,4)
        result.append(dict(id=f'{stage:03X}:{index:03X}',kind='exit',source_map=stage,source_file=file_id,
            definition=index,exit_id=record[14]&15,destination=destination,position=[x,height,horizontal],
            heading=heading,mode=record[15]))
    return result


def extract_atlas(data):
    files=RomFiles(data);code=files.file(12);rooms={};entries=[]
    for stage in range(MAX_STAGE+1):
        address=ROOM_POINTERS+stage*4
        if address+4>len(code):raise ValueError('Truncated room pointer table')
        pointer=struct.unpack_from('>I',code,address)[0]
        if not pointer:continue
        offset=(pointer&0x7FFFFFFF)-CODE_RAM
        if not 0<=offset<=len(code)-28:raise ValueError('Room metadata pointer outside code file')
        meta=code[offset:offset+28];fid=struct.unpack_from('>H',meta,20)[0]
        if not fid:continue
        if not 0x336<=fid<=0x482:raise ValueError('Room file outside mapped USA range')
        if any(struct.unpack_from('>H',meta,p)[0]!=0x800 for p in (8,12,16)) or meta[22:24]!=bytes(2):
            raise ValueError('Unsupported room metadata markers')
        instance=struct.unpack_from('>H',meta,10)[0];footer=struct.unpack_from('>H',meta,18)[0];ending=struct.unpack_from('>H',meta,14)[0]
        rooms[stage]=fid
        entries.extend(room_entrances(stage,fid,files.file(fid),instance,footer,ending))
    invalid=[e for e in entries if e['destination'] not in rooms]
    entries=[e for e in entries if e['destination'] in rooms]
    # Separate native save/flute records provide explicitly labelled fallbacks.
    for kind,start,count in [('save',0x5C630,18),('flute',0x6E010,16)]:
        for index in range(count):
            record=files.data[start+index*12:start+(index+1)*12]
            if len(record)!=12 or not any(record):continue
            destination,x,height,horizontal,heading=struct.unpack_from('>HhhhH',record)
            if destination not in rooms:continue
            entries.append(dict(id=f'{kind}:{index}',kind=kind,source_map=None,source_file=None,definition=index,
                exit_id=record[10]&15,destination=destination,position=[x,height,horizontal],heading=heading,mode=record[11]))
    # Native func_800214E4_220E4 indexes ten-byte default records by stage.
    # All-zero XYZ is the native unspecified sentinel, not a usable fallback.
    for stage in sorted(rooms):
        x,height,horizontal,heading,mode=struct.unpack_from('>hhhHH',files.data,0x6C380+stage*10)
        if not any((x,height,horizontal)):continue
        entries.append(dict(id=f'default:{stage}',kind='default',source_map=None,source_file=None,definition=stage,
            exit_id=0,destination=stage,position=[x,height,horizontal],heading=heading,mode=mode))
    payload=dict(format=SCHEMA,rom_sha1=US_RETAIL_SHA1,rooms=sorted(rooms),entries=entries,
                 unsupported_destinations=len(invalid),source='mn64rando-9c580d0/native-spawn-chain',axis_order='native-x-height-horizontal')
    return validate_atlas({'payload':payload,'sha256':digest(payload)})


def validate_atlas(atlas):
    if not isinstance(atlas,dict) or not isinstance(atlas.get('payload'),dict):raise ValueError('Invalid entrance atlas')
    p=atlas['payload']
    if p.get('format')!=SCHEMA or p.get('rom_sha1')!=US_RETAIL_SHA1 or atlas.get('sha256')!=digest(p):raise ValueError('Entrance atlas identity/checksum mismatch')
    rooms=p.get('rooms');entries=p.get('entries')
    if not isinstance(rooms,list) or any(type(v) is not int or not 0<=v<=MAX_STAGE for v in rooms) or len(set(rooms))!=len(rooms):raise ValueError('Invalid atlas rooms')
    if not isinstance(entries,list) or not 0<len(entries)<=10000:raise ValueError('Invalid entrance count')
    seen=set()
    for e in entries:
        if not isinstance(e,dict) or not isinstance(e.get('id'),str) or e['id'] in seen:raise ValueError('Duplicate/invalid entrance ID')
        seen.add(e['id'])
        if e.get('kind') not in ('exit','save','flute','default') or e.get('destination') not in rooms:raise ValueError('Unsupported entrance type or destination')
        if e['kind']=='exit' and (type(e.get('source_map')) is not int or e['source_map'] not in rooms):raise ValueError('Invalid source room')
        if type(e.get('definition')) is not int or not 0<=e['definition']<4096 or type(e.get('exit_id')) is not int or not 0<=e['exit_id']<16:raise ValueError('Invalid entrance index')
        if not isinstance(e.get('position'),list):raise ValueError('Invalid entrance position')
        Spawn(e['destination'],tuple(e['position']),e.get('heading'),e.get('mode')).validate()
    return atlas


def incoming(atlas,destination):
    if not atlas:return []
    rows=[e for e in atlas['payload']['entries'] if e['destination']==destination]
    return sorted(rows,key=lambda e:(e['kind']!='exit',e['source_map'] if e['source_map'] is not None else 0,e['id']))


def spawn_from_entry(entry):
    label=f'From stage {entry["source_map"]}, exit {entry["exit_id"]}' if entry['kind']=='exit' else (f'Native default spawn for stage {entry["destination"]}' if entry['kind']=='default' else f'{entry["kind"].title()} point {entry["definition"]}')
    return Spawn(entry['destination'],tuple(entry['position']),entry['heading'],entry['mode'],label,entry['id']).validate()


def checkpoint_spawn(checkpoint):
    from practice.checkpoints import validate_checkpoint
    p,blobs=validate_checkpoint(checkpoint)
    heading=int.from_bytes(blobs['rotation'][2:4],'big')
    return Spawn(p['map_id'],tuple(p['position']),heading,0x10,'Checkpoint position').validate()


def load_atlas(path):
    path=Path(path)
    if not path.exists():return None
    if path.stat().st_size>4*1024*1024:raise ValueError('Entrance atlas file exceeds size limit')
    return validate_atlas(json.loads(path.read_text(encoding='utf-8')))


def save_atlas(path,atlas):
    validate_atlas(atlas);path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,prefix=path.name,suffix='.tmp',delete=False) as output:
        json.dump(atlas,output,separators=(',',':'));output.write('\n');temporary=Path(output.name)
    os.replace(temporary,path)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv)
    atlas=extract_atlas(args.rom.read_bytes());save_atlas(args.output,atlas)
    print(json.dumps(dict(rooms=len(atlas['payload']['rooms']),entrances=len(atlas['payload']['entries']),
                         kinds=dict(Counter(e['kind'] for e in atlas['payload']['entries'])),unsupported_destinations=atlas['payload']['unsupported_destinations'])))


if __name__=='__main__':main()

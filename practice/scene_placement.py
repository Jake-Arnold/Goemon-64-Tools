"""One-shot entrance placement after a tool-requested scene load."""
from __future__ import annotations
from dataclasses import dataclass
import math
import struct

from practice.checkpoints import MAP_ADDR, STATE_ADDR, _ensure_capture_safe
from practice.native_character import ready_for_scene_spawn
from practice.entrances import Spawn


def apply_spawn_position(ram, spawn, character, expected_player=None, expected_task=None):
    spawn.validate()
    before=_ensure_capture_safe(ram)
    if not ready_for_scene_spawn(ram,spawn.destination,character,before):raise ValueError('Destination player/character is not ready')
    if expected_player is not None and before['player_ptr']!=expected_player:raise ValueError('Player changed before placement')
    if expected_task is not None and before['task_ptr']!=expected_task:raise ValueError('Player task changed before placement')
    player,task=before['player_ptr'],before['task_ptr']
    desired=struct.pack('>fff',*spawn.position)
    # Recheck the complete destination guard immediately before the sole vector write.
    current=_ensure_capture_safe(ram)
    if current['player_ptr']!=player or current['task_ptr']!=task or not ready_for_scene_spawn(ram,spawn.destination,character,current):
        raise ValueError('Scene or player changed while preparing placement')
    ram.write_guest(player+8,desired)
    after=ram.snapshot()
    if ram.u16(MAP_ADDR)!=spawn.destination or ram.u8(STATE_ADDR)!=13 or after['player_ptr']!=player or after['task_ptr']!=task or not ready_for_scene_spawn(ram,spawn.destination,character,after):
        raise RuntimeError('Scene/player changed during placement; no retry sent')
    observed=tuple(after.get(k) for k in ('x','y','z'))
    # Physics/input can advance between process-memory calls. Record that movement;
    # do not repeatedly teleport or edit unknown velocity/collision fields.
    if any(v is None or not math.isfinite(v) or abs(v-t)>8 for v,t in zip(observed,spawn.position)):
        raise RuntimeError('Position did not remain near the requested entrance; no retry sent')
    return dict(status='placed',requested=list(spawn.position),observed=list(observed),player_ptr=player,task_ptr=task,
                entrance_id=spawn.entrance_id,character=character)


@dataclass
class SpawnPlacement:
    ram: object
    spawn: Spawn
    character: int
    source_map: int
    source_player: int
    source_task: int
    started: float
    timeout: float=15.0
    seen_transition: bool=False
    stable_key: tuple|None=None
    stable: int=0
    attempted: bool=False

    def poll(self,ram,now):
        if ram is not self.ram:raise RuntimeError('Connection changed; entrance placement cancelled')
        if self.attempted:raise RuntimeError('Placement already attempted; no automatic retry')
        if now-self.started>self.timeout:raise RuntimeError('Entrance placement timed out')
        state=ram.u8(STATE_ADDR);here=ram.u16(MAP_ADDR)
        if state!=13:
            if state==12:self.seen_transition=True
            self.stable=0
            return {'status':'waiting','reason':'loading'}
        if here!=self.spawn.destination:
            self.stable=0
            if here!=self.source_map:raise RuntimeError('Loaded a different stage; placement cancelled')
            return {'status':'waiting','reason':'destination'}
        try:
            snap=_ensure_capture_safe(ram)
            ready=ready_for_scene_spawn(ram,here,self.character,snap)
        except ValueError:
            self.stable=0
            return {'status':'waiting','reason':'player_initialization'}
        if not ready:
            self.stable=0
            return {'status':'waiting','reason':'character'}
        if self.source_map!=here or snap['player_ptr']!=self.source_player or snap['task_ptr']!=self.source_task:
            self.seen_transition=True
        if not self.seen_transition:
            return {'status':'waiting','reason':'same_stage_reload'}
        key=(snap['player_ptr'],snap['task_ptr'],snap['character'])
        if key!=self.stable_key:self.stable_key=key;self.stable=0
        self.stable+=1
        if self.stable<2:return {'status':'waiting','reason':'stable_player'}
        self.attempted=True
        return apply_spawn_position(ram,self.spawn,self.character,key[0],key[1])

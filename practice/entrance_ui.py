"""Local entrance atlas controls for the toolkit scene browser."""
import queue
import threading
from pathlib import Path
from tkinter import ttk,filedialog

from practice.entrances import extract_atlas,load_atlas,save_atlas,incoming,spawn_from_entry
from practice.known_entrances import known_entrances, known_entrance_count
from practice.launcher_preferences import preferences_path
from practice.paths import practice_data_dir
from practice.scenes import SCENES,unidentified_scene_name


def stored_entrance_atlas_path():
    """Keep the full numeric coordinate atlas across source checkout changes."""
    return preferences_path().parent / 'entrance-coordinates.json'


class EntranceMixin:
    def init_entrances(self):
        self.entrance_atlas=None;self.entrance_load_error=None
        self.entrance_rows=[];self.entrance_destination=None
        self.entrance_loading=False;self.entrance_results=queue.Queue()
        durable = stored_entrance_atlas_path()
        legacy = practice_data_dir() / 'entrances.json'
        # Try the stable per-user atlas first; old checkouts may still have a
        # valid per-repository cache. Migrate only validated numeric metadata.
        for candidate in (durable, legacy):
            try:
                atlas=load_atlas(candidate)
                if atlas is not None:
                    self.entrance_atlas=atlas
                    if candidate == legacy and not durable.exists():
                        try:save_atlas(durable, atlas)
                        except OSError:pass
                    break
            except (OSError,ValueError,TypeError,KeyError) as exc:
                self.entrance_load_error=str(exc)

    def scene_catalog(self):
        catalog=dict(SCENES)
        # Keep regional scene names separate; the selected USA entrance
        # coordinates are nevertheless shared by both native warp paths.
        if getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan':
            return catalog
        if self.entrance_atlas:
            for stage in self.entrance_atlas['payload']['rooms']:catalog.setdefault(stage,unidentified_scene_name(stage))
        return catalog

    def build_entrance_controls(self,parent):
        import tkinter as tk
        box=ttk.LabelFrame(parent,text=' Destination entrance ',padding=6);box.pack(fill='x',pady=4)
        self.entrance_box=box
        line=ttk.Frame(box);line.pack(fill='x')
        self.entrance_load_button=ttk.Button(line,text='Load original USA ROM…',command=self.load_entrance_rom)
        self.entrance_load_button.pack(side='left')
        ttk.Button(line,text='Cancel scene request',command=self.cancel_scene_request).pack(side='right')
        self.entrance_note=tk.StringVar(value=self.entrance_summary())
        ttk.Label(box,textvariable=self.entrance_note,wraplength=900).pack(anchor='w',pady=3)
        self.entrance_choice=ttk.Combobox(box,state='readonly',width=100)
        self.entrance_choice.pack(fill='x')
        self.entrance_choice.bind('<<ComboboxSelected>>',lambda _e:self.describe_entrance())

    def entrance_summary(self):
        built_in = known_entrance_count()
        if self.entrance_atlas:
            p=self.entrance_atlas['payload']
            return (f'Stored entrance coordinates: {len(p["rooms"])} scenes, '
                    f'{len(p["entries"])} entrance records, plus {built_in} '
                    'built-in observed point(s). No ROM needed on startup.')
        return (f'{built_in} permanent known warp point(s) included. '
                'For other scenes, load original USA ROM once to store all '
                'extracted coordinates permanently.'
                + (f' Cache error: {self.entrance_load_error}'
                   if self.entrance_load_error else ''))

    def load_entrance_rom(self):
        if self.entrance_loading:return
        path=filedialog.askopenfilename(title='Original USA Mystical Ninja ROM',filetypes=[('N64 ROM','*.z64 *.n64 *.v64'),('All files','*.*')])
        if not path:return
        self.entrance_loading=True;self.entrance_load_button.state(['disabled'])
        self.entrance_note.set('Reading entrance data from the ROM…')
        def work():
            try:
                atlas=extract_atlas(Path(path).read_bytes());save_atlas(stored_entrance_atlas_path(),atlas)
                self.entrance_results.put(('ok',atlas))
            except (OSError,ValueError,TypeError,KeyError) as exc:self.entrance_results.put(('error',str(exc)))
        threading.Thread(target=work,daemon=True).start();self.root.after(60,self.poll_entrance_rom)

    def poll_entrance_rom(self):
        try:kind,value=self.entrance_results.get_nowait()
        except queue.Empty:
            self.root.after(60,self.poll_entrance_rom);return
        self.entrance_loading=False;self.entrance_load_button.state(['!disabled'])
        if kind=='ok':
            self.entrance_atlas=value;self.entrance_load_error=None
            self.draw_scene_list();self.refresh_entrance_choices()
            self.entrance_note.set(self.entrance_summary())
        else:self.entrance_note.set('Entrance ROM load failed: '+value)

    def refresh_entrance_choices(self,destination=None):
        if not hasattr(self,'entrance_choice'):return
        if destination is None:
            chosen=self.scene_list.curselection()
            destination=self.scene_options[chosen[0]][0] if chosen else None
        previous=None
        index=self.entrance_choice.current()
        if self.entrance_destination==destination and 0<=index<len(self.entrance_rows):previous=self.entrance_rows[index]['id']
        self.entrance_destination=destination
        self.entrance_rows=incoming(self.entrance_atlas,destination)
        if not self.entrance_rows:
            # The checked-in known XYZ records are available without any ROM.
            # Never override more complete validated USA-atlas entrance rows.
            self.entrance_rows=known_entrances(destination)
        values=[]
        catalog=self.scene_catalog()
        for row in self.entrance_rows:
            spawn=spawn_from_entry(row)
            source=catalog.get(row['source_map'],f'Stage {row["source_map"]}') if row['kind']=='exit' else spawn.label
            values.append(f'{row["id"]} — {source} → XYZ {tuple(spawn.position)}; facing 0x{spawn.heading:03X}')
        self.entrance_choice['values']=values
        self.entrance_choice.set('')
        chosen_index=next((i for i,e in enumerate(self.entrance_rows) if e['id']==previous),None)
        if chosen_index is None:
            try:
                if getattr(self.active_version, 'key', 'usa') == 'japan':
                    reader = getattr(self, 'jp_rdram', None)
                    origin = (int.from_bytes(
                        reader.read_guest(0x800CD2A2, 2), 'big')
                        if reader is not None else None)
                else:
                    origin = self.mem.u16(0x800C7AB2) if self.mem else None
            except (OSError, ValueError, RuntimeError, PermissionError):
                origin = None
            candidates=[i for i,e in enumerate(self.entrance_rows) if e['source_map']==origin and e['kind']=='exit']
            if not candidates:
                defaults=[i for i,e in enumerate(self.entrance_rows) if e['kind']=='default']
                candidates=defaults or list(range(len(self.entrance_rows)))
            variants={tuple(self.entrance_rows[i]['position'])+(self.entrance_rows[i]['heading'],self.entrance_rows[i]['mode']) for i in candidates}
            if len(variants)==1:chosen_index=candidates[0]
        if chosen_index is not None:self.entrance_choice.current(chosen_index);self.describe_entrance()
        else:
            self.entrance_note.set(
                f'{len(values)} recorded entrances for this scene; choose one.'
                if values else
                'No stored coordinates for this scene. Load original USA ROM '
                'once to save its entrance records, or select a known scene.')

    def selected_scene_spawn(self,destination):
        if self.entrance_destination!=destination or self.entrance_choice.current()<0:
            self.refresh_entrance_choices(destination)
        if not self.entrance_rows:
            raise ValueError(
                'No known coordinates for this scene. Load original USA ROM '
                'once to store the full entrance table')
        index=self.entrance_choice.current()
        if not 0<=index<len(self.entrance_rows):raise ValueError('Choose a destination entrance first; no reload sent')
        spawn=spawn_from_entry(self.entrance_rows[index])
        if spawn.destination!=destination:raise ValueError('Entrance belongs to a different stage')
        return spawn

    def describe_entrance(self):
        index=self.entrance_choice.current()
        if 0<=index<len(self.entrance_rows):
            spawn=spawn_from_entry(self.entrance_rows[index])
            evidence=(' Heading/mode are experimental for this observed point.'
                      if self.entrance_rows[index].get('heading_mode_verified') is False
                      else '')
            self.entrance_note.set(
                f'{spawn.label}; XYZ {tuple(spawn.position)}. '
                'Staged before reload and verified against the loaded player.'
                + evidence)

    def cancel_scene_request(self):
        self.pending_direct_warp=None;self.pending_native_warp=None
        if getattr(self,'native_key_release',None):self._release_debug_key()
        self.scene_status.set('Scene monitoring/placement cancelled. A reload already requested from the game may still continue.')

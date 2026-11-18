"""Local entrance atlas controls for the toolkit scene browser."""
import queue
import threading
from pathlib import Path
from tkinter import ttk,filedialog

from practice.entrances import extract_atlas,load_atlas,save_atlas,incoming,spawn_from_entry
from practice.room_actors import extract_actors, load_actors, save_actors
from practice.room_actor_ui import RoomActorBrowser
from practice.known_entrances import known_entrances, known_entrance_count
from practice.launcher_preferences import preferences_path
from practice.paths import practice_data_dir, resource_root
from practice.scenes import SCENES,unidentified_scene_name
from practice.region_session import active_session


def stored_entrance_atlas_path():
    """Keep the full numeric coordinate atlas across source checkout changes."""
    return preferences_path().parent / 'entrance-coordinates.json'


def repository_entrance_atlas_path():
    """Versioned numeric scene/entrance atlas shipped with the toolkit.

    The extraction file is committed only after validated original-USA ROM
    data has been supplied; it never contains a ROM or executable.
    """
    return resource_root() / 'practice' / 'data' / 'entrance-coordinates.json'


class EntranceMixin:
    def init_entrances(self):
        self.entrance_atlas=None;self.entrance_load_error=None
        self.entrance_rows=[];self.entrance_destination=None
        self._entrance_selection_context=None
        self._entrance_manual_selection=False
        self.entrance_loading=False;self.entrance_results=queue.Queue()
        self.room_actor_atlas = None
        self.japan_actor_atlas = None
        self.room_actor_browser = None
        for attr, filename in (('room_actor_atlas', 'room-actors.json'),
                               ('japan_actor_atlas', 'room-actors-japan-0.json')):
            try:
                setattr(self, attr, load_actors(practice_data_dir() / filename))
            except (OSError, ValueError, TypeError, KeyError):
                pass
        bundled = repository_entrance_atlas_path()
        durable = stored_entrance_atlas_path()
        legacy = practice_data_dir() / 'entrances.json'
        self.entrance_atlas_source = 'none'
        # Prefer the version-controlled, reviewed numeric table when present.
        # Fall back to local user data until the full extracted table is
        # committed. Never mistake a corrupted bundled file for a valid atlas.
        for candidate in (bundled, durable, legacy):
            try:
                atlas=load_atlas(candidate)
                if atlas is not None:
                    self.entrance_atlas=atlas
                    self.entrance_atlas_source = (
                        'repository' if candidate == bundled else
                        'persistent user cache' if candidate == durable else
                        'legacy checkout cache')
                    if candidate == legacy:
                        try:save_atlas(durable, atlas)
                        except OSError:pass
                    break
            except (OSError,ValueError,TypeError,KeyError) as exc:
                self.entrance_load_error=str(exc)

    def scene_catalog(self):
        """One scene list for USA/JP; label confidence is separate from IDs."""
        catalog = dict(SCENES)
        if self.entrance_atlas:
            for stage in self.entrance_atlas['payload']['rooms']:
                catalog.setdefault(stage, unidentified_scene_name(stage))
        return catalog

    def build_entrance_controls(self,parent):
        import tkinter as tk
        box=ttk.LabelFrame(parent,text=' Destination entrance ',padding=6);box.pack(fill='x',pady=4)
        self.entrance_box=box
        line=ttk.Frame(box);line.pack(fill='x')
        self.entrance_load_button=ttk.Button(line,text='Load original USA ROM…',command=self.load_entrance_rom)
        self.entrance_load_button.pack(side='left')
        self.japan_actor_load_button=ttk.Button(
            line, text='Load Japan actor ROM…',
            command=self.load_japan_actor_rom)
        self.japan_actor_load_button.pack(side='left', padx=8)
        ttk.Button(line, text='Room actors…',
                   command=self.show_room_actors).pack(side='left', padx=8)
        ttk.Button(line,text='Cancel scene request',command=self.cancel_scene_request).pack(side='right')
        self.entrance_note=tk.StringVar(value=self.entrance_summary())
        ttk.Label(box,textvariable=self.entrance_note,wraplength=900).pack(anchor='w',pady=3)
        self.entrance_choice=ttk.Combobox(box,state='readonly',width=100)
        self.entrance_choice.pack(fill='x')
        self.entrance_choice.bind('<<ComboboxSelected>>',self._entrance_chosen_by_user)

    def _entrance_chosen_by_user(self, _event):
        # Preserve an explicitly chosen entrance, but not an auto-selected
        # entry carried over from an obsolete scene/region/atlas context.
        self._entrance_manual_selection=True
        self.describe_entrance()

    def entrance_summary(self):
        built_in = known_entrance_count()
        if self.entrance_atlas:
            p=self.entrance_atlas['payload']
            source = getattr(self, 'entrance_atlas_source', 'stored cache')
            return (f'{source} entrance coordinates: {len(p["rooms"])} scenes, '
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
        self.entrance_loading=True
        self.entrance_load_button.state(['disabled'])
        self.japan_actor_load_button.state(['disabled'])
        self.entrance_note.set('Reading entrance data from the ROM…')
        def work():
            try:
                rom = Path(path).read_bytes()
                # Preserve the current reviewed entrance atlas storage and
                # game-warp semantics; actor metadata is an independent,
                # read-only companion extraction.
                atlas = extract_atlas(rom)
                save_atlas(stored_entrance_atlas_path(), atlas)
                actors = None
                actor_warning = None
                try:
                    actors = extract_actors(rom)
                    save_actors(practice_data_dir() / 'room-actors.json', actors)
                except (OSError, ValueError, TypeError, KeyError) as error:
                    # Actor-research failure cannot invalidate the proven
                    # entrance coordinates needed by the native warp path.
                    actor_warning = str(error)
                self.entrance_results.put(('ok', (atlas, actors, actor_warning)))
            except (OSError,ValueError,TypeError,KeyError) as exc:self.entrance_results.put(('error',str(exc)))
        threading.Thread(target=work,daemon=True).start();self.root.after(60,self.poll_entrance_rom)

    def load_japan_actor_rom(self):
        """Read-only Japanese ROM actor extraction, no scene or RAM changes."""
        if self.entrance_loading:
            return
        path=filedialog.askopenfilename(
            title='Original Japan rev-0 Goemon ROM',
            filetypes=[('N64 ROM','*.z64 *.n64 *.v64'),('All files','*.*')])
        if not path:
            return
        self.entrance_loading=True
        self.entrance_load_button.state(['disabled'])
        self.japan_actor_load_button.state(['disabled'])
        self.entrance_note.set(
            'Reading original Japanese room actor metadata (no game writes)…')
        def work():
            try:
                actors=extract_actors(Path(path).read_bytes(),region='japan_0')
                save_actors(practice_data_dir() / 'room-actors-japan-0.json',actors)
                self.entrance_results.put(('japan-ok',actors))
            except (OSError, ValueError, TypeError, KeyError) as error:
                self.entrance_results.put(
                    ('error','Japanese actor extraction: '+str(error)))
        threading.Thread(target=work,daemon=True).start()
        self.root.after(60,self.poll_entrance_rom)

    def poll_entrance_rom(self):
        try:
            kind, value = self.entrance_results.get_nowait()
        except queue.Empty:
            self.root.after(60,self.poll_entrance_rom)
            return
        self.entrance_loading=False
        self.entrance_load_button.state(['!disabled'])
        self.japan_actor_load_button.state(['!disabled'])
        if kind=='japan-ok':
            self.japan_actor_atlas=value
            browser=self.room_actor_browser
            if browser is not None and browser.window.winfo_exists():
                browser.refresh(
                    self.room_actor_atlas,
                    getattr(self,'scene_selected',None),
                    self.japan_actor_atlas)
                browser.region.set('japan_0')
                browser.redraw()
            self.entrance_note.set(
                'Japan-0 actor placements loaded from original ROM '
                '(research only; USA entrance coordinates unchanged).')
        elif kind=='ok':
            warning=None
            if isinstance(value,tuple):
                self.entrance_atlas,self.room_actor_atlas,warning=value
            else:
                self.entrance_atlas=value
            self.entrance_load_error=None
            self.entrance_atlas_source='persistent user cache (new extraction)'
            self.draw_scene_list()
            self.refresh_entrance_choices()
            self.entrance_note.set(
                self.entrance_summary() +
                (f' Actor research unavailable: {warning}' if warning else ''))
            browser=self.room_actor_browser
            if browser is not None and browser.window.winfo_exists():
                browser.refresh(
                    self.room_actor_atlas,
                    getattr(self,'scene_selected',None),self.japan_actor_atlas)
        else:
            self.entrance_note.set('Entrance ROM load failed: '+value)

    def show_room_actors(self):
        """Shared static actor research window, never a live actor pointer."""
        stage=getattr(self,'scene_selected',None)
        browser=self.room_actor_browser
        if browser is not None and browser.window.winfo_exists():
            browser.refresh(self.room_actor_atlas,stage,self.japan_actor_atlas)
            browser.window.lift()
            return
        browser=RoomActorBrowser(
            self.root,self.room_actor_atlas,stage,self.japan_actor_atlas)
        browser.region.set(
            'japan_0' if self.active_version.key=='japan' else 'usa')
        browser.redraw()
        self.room_actor_browser=browser

    def refresh_entrance_choices(self,destination=None):
        if not hasattr(self,'entrance_choice'):return
        if destination is None:
            chosen=self.scene_list.curselection()
            destination=self.scene_options[chosen[0]][0] if chosen else None
        context=(getattr(getattr(self,'active_version',None),'key','usa'),id(self.entrance_atlas))
        previous=None
        index=self.entrance_choice.current()
        if (self._entrance_manual_selection and
                self._entrance_selection_context==context and
                self.entrance_destination==destination and
                0<=index<len(self.entrance_rows)):
            previous=self.entrance_rows[index]['id']
        self.entrance_destination=destination
        browser=getattr(self,'room_actor_browser',None)
        if browser is not None and browser.window.winfo_exists():
            browser.refresh(
                self.room_actor_atlas,destination,self.japan_actor_atlas)
        self._entrance_selection_context=context
        self._entrance_manual_selection=False
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
                session = active_session(self)
                origin = session.read_current_scene() if session.connected else None
            except (OSError, ValueError, RuntimeError, PermissionError):
                origin = None
            candidates=[i for i,e in enumerate(self.entrance_rows) if e['source_map']==origin and e['kind']=='exit']
            if not candidates:
                defaults=[i for i,e in enumerate(self.entrance_rows) if e['kind']=='default']
                candidates=defaults or list(range(len(self.entrance_rows)))
            variants={tuple(self.entrance_rows[i]['position'])+(self.entrance_rows[i]['heading'],self.entrance_rows[i]['mode']) for i in candidates}
            if len(variants)==1:chosen_index=candidates[0]
        if chosen_index is not None:
            self.entrance_choice.current(chosen_index)
            self._entrance_manual_selection=(previous is not None)
            self.describe_entrance()
        else:
            self.entrance_note.set(
                f'{len(values)} recorded entrances for this scene; choose one.'
                if values else
                'No stored coordinates for this scene. Load original USA ROM '
                'once to save its entrance records, or select a known scene.')

    def selected_scene_spawn(self,destination):
        context=(getattr(getattr(self,'active_version',None),'key','usa'),id(self.entrance_atlas))
        if (self.entrance_destination!=destination or
                self.entrance_choice.current()<0 or
                self._entrance_selection_context!=context or
                not self._entrance_manual_selection):
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

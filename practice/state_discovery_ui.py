"""Tk interface for read-only, user-labelled A/B/C N64 state probes."""
from __future__ import annotations

from datetime import datetime
import json
import queue
import threading
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from practice.paths import diagnostics_dir
from practice.state_discovery import PROBE_ACTIONS, capture_state, compare_captures
from practice.theme import PALETTE
from practice.japan_state_comparison import (
    capture_japan_memory, compare_japan_memory,
)
from practice.japan_player_position_research import (
    find_japan_xyz_candidates, export_japan_xyz_all_candidates,
)
from practice.japanese_scene_probes import read_japan_scene_probes
from practice.transition_observer import read_transition_observation, format_transition_observation

JAPAN_PROBE_ACTIONS = {
    'Scene transition': 'Capture A before using a doorway, B after loading. Repeat in both directions; no scene writes.',
    'Character switch': 'Capture A before native C-Down and B afterward. Confirm model identity and character index separately.',
    'Ryo or inventory change': 'Capture before/after a Ryo pickup or item action. Changed bytes are candidates only.',
    'Menu or map shown': 'Capture A closed, B displayed, C closed again to filter reversible changes.',
    'Story event candidate': 'Capture a repeated story action. Japan saved-event banks are not mapped; do not assume USA offsets.',
    'Player movement': 'For XYZ research use WIDE A stationary, B after walking to a different position, C stationary at B. Click Find XYZ triples. No player position writes.',
}


class StateDiscoveryMixin:
    def build_state_discovery_tab(self, notebook):
        tab=ttk.Frame(notebook,padding=10)
        notebook.add(tab,text='Advanced RAM comparison')
        self.state_discovery_tab=tab
        self.state_captures={}
        self.state_report=None
        self._jp_probe_generation = 0
        self._jp_probe_busy = False
        ttk.Label(tab,text='Advanced A/B/C guest memory comparison',font=('Segoe UI Semibold',16),
                  foreground=PALETTE['gold']).pack(anchor='w',pady=(2,6))
        ttk.Label(tab,text='Capture A (before), B (after) and optionally C (returned to the original state). '
                  'Only observed values are reported: no addresses are assumed to represent the requested flag.',
                  style='Muted.TLabel',wraplength=1080).pack(anchor='w',pady=(0,9))
        context=ttk.LabelFrame(tab,text='Scene / boss investigation (read-only)',padding=8)
        context.pack(fill='x',pady=(0,9))
        ttk.Label(context,text='Works without a valid player object. Capture engine and Script VM context before and after a boss phase, loading screen or scene change. Values are observations, not confirmed boss HP or safe warp targets.',style='Muted.TLabel',wraplength=1050).pack(anchor='w')
        self.transition_observation_text=tk.StringVar(value='Connect to the game, then select Read scene context.')
        ttk.Button(context,text='Read scene context',command=self.read_scene_context).pack(anchor='w',pady=(5,3))
        ttk.Label(context,textvariable=self.transition_observation_text,wraplength=1050,justify='left').pack(anchor='w')
        row=ttk.Frame(tab);row.pack(fill='x',pady=(0,6))
        ttk.Label(row,text='Test:').pack(side='left',padx=(0,6))
        self.state_probe_kind=tk.StringVar(value='Map displayed')
        selector=ttk.Combobox(row,textvariable=self.state_probe_kind,values=list(PROBE_ACTIONS),
                              width=26,state='readonly')
        selector.pack(side='left')
        self.state_probe_selector = selector
        ttk.Label(row,text='Memory range:').pack(side='left',padx=(18,5))
        self.state_probe_scope=tk.StringVar(value='focused')
        ttk.Combobox(row,textvariable=self.state_probe_scope,values=('focused','wide'),
                     width=10,state='readonly').pack(side='left')
        self.state_probe_instruction=tk.StringVar(value=PROBE_ACTIONS[self.state_probe_kind.get()])
        selector.bind('<<ComboboxSelected>>',
                      lambda _e: self._set_state_probe_instruction())
        ttk.Label(tab,textvariable=self.state_probe_instruction,style='Muted.TLabel',
                  wraplength=1100).pack(anchor='w',pady=(0,6))
        self.state_probe_scope_hint = tk.StringVar(
            value='USA focused: game globals and optional player regions. '
                  'USA wide: 4 MiB N64 RAM. Use identical ranges for A/B/C.')
        ttk.Label(tab,textvariable=self.state_probe_scope_hint,
                  style='Muted.TLabel',wraplength=1080).pack(anchor='w',pady=(0,8))
        row=ttk.Frame(tab);row.pack(fill='x',pady=(0,9))
        self.state_probe_capture_buttons = {}
        for stage,caption in (('A','Capture A: Before'),('B','Capture B: After'),
                              ('C','Capture C: Reverted')):
            button = ttk.Button(
                row, text=caption, command=lambda s=stage:self.capture_state_probe(s))
            button.pack(side='left',padx=(0,7))
            self.state_probe_capture_buttons[stage] = button
        ttk.Button(row,text='Compare',style='Gold.TButton',
                   command=self.compare_state_probes).pack(side='left',padx=8)
        self.state_xyz_button = ttk.Button(
            row, text='Find XYZ triples (read-only)',
            command=self.find_japan_xyz_from_captures)
        self.state_probe_export_button = ttk.Button(
            row, text='Export comparison JSON', command=self.export_state_probe)
        self.state_probe_export_button.pack(side='left',padx=(0,7))
        ttk.Button(row,text='Clear',command=self.reset_state_probes).pack(side='left')
        self.state_probe_status=tk.StringVar(value='No captures. Select a test and connect to the game.')
        ttk.Label(tab,textvariable=self.state_probe_status,wraplength=1060).pack(anchor='w',pady=(0,10))
        headings=('address','region','before','after','bitmask','returned','kind')
        frame=ttk.Frame(tab);frame.pack(fill='both',expand=True)
        self.state_probe_table=ttk.Treeview(frame,columns=headings,show='headings',height=15)
        for key,heading,width in (
                ('address','Guest address',150),('region','Region',135),
                ('before','A: before',95),('after','B: after',95),
                ('bitmask','XOR mask',85),('returned','C matched A?',125),
                ('kind','Potential type',150)):
            self.state_probe_table.heading(key,text=heading)
            self.state_probe_table.column(key,width=width,stretch=key=='region')
        bar=ttk.Scrollbar(frame,orient='vertical',command=self.state_probe_table.yview)
        self.state_probe_table.configure(yscrollcommand=bar.set)
        self.state_probe_table.pack(side='left',fill='both',expand=True)
        bar.pack(side='right',fill='y')
        row=ttk.Frame(tab);row.pack(fill='x',pady=7)
        ttk.Button(row,text='Copy selected address',command=self.copy_state_probe_address).pack(side='left')
        ttk.Button(row,text='Watch selected address',command=self.watch_state_probe_candidate,
                   style='Gold.TButton').pack(side='left',padx=(8,0))
        ttk.Label(row,text='A/B changes alone are hypotheses. For persistent storyline flags, A/B is sufficient. '
                  'Player-task float values are not proven velocity.',style='Muted.TLabel',
                  wraplength=850).pack(side='left',padx=(15,0))

    def _state_is_japan(self):
        return getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan'

    def _set_state_probe_instruction(self):
        actions = JAPAN_PROBE_ACTIONS if self._state_is_japan() else PROBE_ACTIONS
        self.state_probe_instruction.set(
            actions.get(self.state_probe_kind.get(), 'Choose a capture experiment.'))
        # For movement heuristics, C is taken *at B*, not at A as in the
        # general reversible A/B/C experiment. Avoid a misleading button name.
        moving = self._state_is_japan() and self.state_probe_kind.get() == 'Player movement'
        self.state_probe_capture_buttons['C'].configure(
            text='Capture C: Still at B' if moving else 'Capture C: Reverted')

    def configure_state_probe_region(self):
        actions = JAPAN_PROBE_ACTIONS if self._state_is_japan() else PROBE_ACTIONS
        self.state_probe_selector['values'] = tuple(actions)
        self.state_probe_kind.set(next(iter(actions)))
        self._set_state_probe_instruction()
        if self._state_is_japan():
            self.state_xyz_button.pack(side='left', padx=(0, 7),
                                       before=self.state_probe_export_button)
        else:
            self.state_xyz_button.pack_forget()
        self.state_probe_scope_hint.set(
            'Japan focused: two 4 KiB engine/save candidate ranges (not confirmed '
            'event banks). Wide: read-only full verified 4/8 MiB Japan RDRAM. '
            'For XYZ: A still, B moved, C still at B; no player pointer required.'
            if self._state_is_japan() else
            'USA focused: game globals and optional player regions. '
            'USA wide: 4 MiB N64 RAM. Use identical ranges for A/B/C.')

    def read_scene_context(self):
        if self._state_is_japan():
            if getattr(self, 'jp_rdram', None) is None:
                self.transition_observation_text.set(
                    'Connect to verified Japanese Project64 or Mupen64Plus first.')
                return
            readings = read_japan_scene_probes(self.jp_rdram)
            self.transition_observation_text.set('\n'.join(
                f'{key}: {value.value} [{value.raw}] — {value.status}'
                for key, value in readings.items()))
            return
        if not self.mem:
            self.transition_observation_text.set('Not connected to game memory.')
            return
        try:
            observation=read_transition_observation(self.mem)
            self.transition_observation_text.set(format_transition_observation(observation))
        except (OSError,ValueError,RuntimeError) as exc:
            self.transition_observation_text.set(f'Unable to read scene context: {exc}')

    def _capture_japan_probe(self, stage):
        if self._jp_probe_busy:
            self.state_probe_status.set('A Japanese capture is already running.')
            return
        reader = getattr(self, 'jp_rdram', None)
        if reader is None or getattr(self, 'game_pid', None) is None:
            self.state_probe_status.set('Connect to verified Japan-0 emulator RDRAM first.')
            return
        if stage == 'C' and 'B' not in self.state_captures:
            self.state_probe_status.set('Capture A and B before optional C.')
            return
        identity = ('japan-0', self.game_pid, reader.base, reader.endian, id(reader))
        scope = self.state_probe_scope.get()
        label = self.state_probe_kind.get() + ' ' + stage
        self._jp_probe_generation += 1
        generation = self._jp_probe_generation
        self._jp_probe_busy = True
        results = queue.SimpleQueue()
        self.state_probe_status.set(
            f'Reading Japan-0 {scope} snapshot {stage} in the background (read-only)...')

        def worker():
            try:
                capture = capture_japan_memory(reader, label, scope=scope, identity=identity)
                results.put((capture, None))
            except Exception as exc:
                results.put((None, str(exc)))

        def poll():
            if generation != self._jp_probe_generation:
                return
            try:
                capture, error = results.get_nowait()
            except queue.Empty:
                self.root.after(70, poll)
                return
            self._jp_probe_busy = False
            current = getattr(self, 'jp_rdram', None)
            if (not self._state_is_japan() or current is not reader
                    or getattr(self, 'game_pid', None) != identity[1]
                    or reader.base != identity[2] or reader.endian != identity[3]):
                self.state_probe_status.set('Japanese connection changed; capture discarded.')
                return
            if error is not None:
                self.state_probe_status.set(f'Japanese {stage} capture failed: {error}')
                return
            if stage == 'A':
                self.state_captures.clear()
            elif 'A' not in self.state_captures:
                self.state_probe_status.set('A was cleared; recapture A first.')
                return
            self.state_captures[stage] = capture
            if stage == 'B':
                self.state_captures.pop('C', None)
            self.state_report = None
            self.state_probe_status.set(
                f'Japan {stage} captured: {scope}, map {capture.map_id}, '
                f'character {capture.character if capture.character is not None else "unknown"}; '
                f'present: {", ".join(sorted(self.state_captures))}. '
                'All memory reads only.')

        threading.Thread(target=worker, daemon=True,
                         name='GoemonJapanABCReadOnly').start()
        self.root.after(70, poll)

    def capture_state_probe(self,stage):
        if self._state_is_japan():
            self._capture_japan_probe(stage)
            return
        if not self.mem:
            self.state_probe_status.set('Connect to Goemon64Recomp before capturing memory.')
            return
        try:
            scope=self.state_probe_scope.get()
            label=self.state_probe_kind.get()+' '+stage
            capture=capture_state(self.mem,label,scope=scope,
                                  snapshot=self.current if isinstance(self.current,dict) else None)
            self.state_captures[stage]=capture
            self.state_report=None
            regions=', '.join(r.name for r in capture.regions)
            self.state_probe_status.set(f'{stage} captured for character {capture.character if capture.character is not None else "unavailable"}, '
                                        f'map {capture.map_id}; {regions}. '
                                        f'A/B/C captured: {", ".join(sorted(self.state_captures))}')
        except (OSError,ValueError,RuntimeError) as exc:
            self.state_probe_status.set(f'{stage} capture failed: {exc}')

    def compare_state_probes(self):
        if 'A' not in self.state_captures or 'B' not in self.state_captures:
            self.state_probe_status.set('Capture A and B first.')
            return
        try:
            if self._jp_probe_busy:
                self.state_probe_status.set('Finish the current Japanese snapshot first.')
                return
            if self._state_is_japan():
                report = compare_japan_memory(
                    self.state_captures['A'], self.state_captures['B'],
                    self.state_captures.get('C'))
            else:
                report = compare_captures(
                    self.state_captures['A'], self.state_captures['B'],
                    self.state_captures.get('C'))
            self.state_report=report
            self.state_probe_table.heading('returned', text='C matched A?')
            self.state_probe_table.column('before', width=95)
            self.state_probe_table.column('after', width=95)
            self.state_probe_table.delete(*self.state_probe_table.get_children())
            for i,row in enumerate(report['candidates']):
                self.state_probe_table.insert('','end',iid=str(i),values=(
                    row['address'],row['region'],row['before'],row['after'],
                    row['xor_mask'],'yes' if row['reverted'] else '—',row['kind']))
            counts=report['counts']
            event_count=len(report.get('event_flag_changes',[]))
            note = ('Japanese event banks are unmapped. ' if self._state_is_japan()
                    else f'{event_count} changed saved event-flag bytes. ')
            self.state_probe_status.set(
                f"Compared {counts['regions_compared']} regions; "
                f"{counts['observed_changes']} byte changes; "
                f"{counts['candidate_count']} candidates (showing {counts['reported_candidates']}); "
                + note + 'No candidate has been validated as an actual game flag.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.state_probe_status.set(f'Comparison failed: {exc}')

    def find_japan_xyz_from_captures(self):
        """Rank read-only Japanese float triples from three full-RAM snapshots.

        Captures must be A stationary, B walked elsewhere, C stationary at B.
        This is a heuristic and never validates an address for memory writing.
        """
        if not self._state_is_japan():
            self.state_probe_status.set('XYZ candidate research is Japan-only.')
            return
        if self._jp_probe_busy:
            self.state_probe_status.set('Finish the current Japanese capture/research first.')
            return
        if any(stage not in self.state_captures for stage in ('A', 'B', 'C')):
            self.state_probe_status.set(
                'Capture WIDE A (stationary), B (after moving), C (stationary at B).')
            return
        a, b, c = (self.state_captures[stage] for stage in ('A', 'B', 'C'))
        if any(getattr(snapshot, 'scope', None) != 'wide' for snapshot in (a, b, c)):
            self.state_probe_status.set('XYZ candidate research requires three WIDE captures.')
            return
        reader = getattr(self, 'jp_rdram', None)
        if reader is None or getattr(self, 'game_pid', None) is None:
            self.state_probe_status.set('Reconnect to Japan-0 RDRAM before XYZ research.')
            return
        identity = ('japan-0', self.game_pid, reader.base, reader.endian, id(reader))
        if any(snapshot.identity != identity for snapshot in (a, b, c)):
            self.state_probe_status.set('Japanese connection changed; recapture all XYZ snapshots.')
            return
        self._jp_probe_generation += 1
        generation = self._jp_probe_generation
        self._jp_probe_busy = True
        self.state_probe_status.set('Ranking wide Japanese XYZ float triples in the background; read-only.')
        results = queue.SimpleQueue()

        def worker():
            try:
                results.put((find_japan_xyz_candidates(a, b, c), None))
            except Exception as exc:
                results.put((None, str(exc)))

        def poll():
            if generation != self._jp_probe_generation:
                return
            try:
                report, error = results.get_nowait()
            except queue.Empty:
                self.root.after(70, poll)
                return
            self._jp_probe_busy = False
            if (not self._state_is_japan() or getattr(self, 'jp_rdram', None) is not reader
                    or getattr(self, 'game_pid', None) != identity[1]):
                self.state_probe_status.set('Japanese connection changed; XYZ results discarded.')
                return
            if error is not None:
                self.state_probe_status.set(f'XYZ research rejected: {error}')
                return
            self.state_report = report
            self.state_probe_table.delete(*self.state_probe_table.get_children())
            self.state_probe_table.heading('returned', text='C stable at B?')
            self.state_probe_table.column('before', width=205)
            self.state_probe_table.column('after', width=205)
            for i, row in enumerate(report['candidates']):
                self.state_probe_table.insert('', 'end', iid=str(i), values=(
                    row['address'], row['region'], row['before'], row['after'],
                    row['xor_mask'], 'yes' if row['c_stable_at_b'] else '—', row['kind']))
            counts = report['counts']
            self.state_probe_status.set(
                f"XYZ candidates: {counts['candidate_count']} moving/settled float "
                f"triples; showing {counts['reported_candidates']}. "
                'These can describe NPCs or other objects. Watch and test across '
                'multiple scenes before identifying the player. No writes.')

        threading.Thread(target=worker, daemon=True,
                         name='GoemonJapanXYZReadOnly').start()
        self.root.after(70, poll)

    def _export_all_japan_xyz_candidates(self):
        """Stream all matching XYZ rows, never just the 200-row table preview."""
        if self._jp_probe_busy:
            self.state_probe_status.set('Finish current Japan capture/export first.')
            return
        report = self.state_report
        if (not self._state_is_japan() or
                any(stage not in self.state_captures for stage in ('A', 'B', 'C'))):
            self.state_probe_status.set('XYZ snapshots are missing; recapture A/B/C.')
            return
        reader = getattr(self, 'jp_rdram', None)
        if reader is None or getattr(self, 'game_pid', None) is None:
            self.state_probe_status.set('Reconnect to Japan-0 before exporting XYZ.')
            return
        identity = ('japan-0', self.game_pid, reader.base, reader.endian, id(reader))
        captures = tuple(self.state_captures[stage] for stage in ('A', 'B', 'C'))
        if any(c.identity != identity for c in captures):
            self.state_probe_status.set('Connection changed; recapture XYZ before export.')
            return
        try:
            path = diagnostics_dir() / (
                'japan_state_probe_' +
                datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
        except OSError as exc:
            self.state_probe_status.set(f'XYZ export setup failed: {exc}')
            return
        self._jp_probe_generation += 1
        generation = self._jp_probe_generation
        self._jp_probe_busy = True
        expected = report['counts']['candidate_count']
        self.state_probe_status.set(
            f'Exporting ALL {expected} XYZ candidates (table remains top 200); '
            'scanning cached A/B/C RAM snapshots, not reading live game RAM...')
        results = queue.SimpleQueue()

        def worker():
            try:
                count = export_japan_xyz_all_candidates(
                    *captures, path, expected_count=expected,
                    cancelled=lambda: generation != self._jp_probe_generation)
                results.put((count, None))
            except Exception as exc:
                results.put((None, str(exc)))

        def poll():
            if generation != self._jp_probe_generation:
                return
            try:
                count, error = results.get_nowait()
            except queue.Empty:
                self.root.after(70, poll)
                return
            self._jp_probe_busy = False
            if (not self._state_is_japan() or
                    getattr(self, 'jp_rdram', None) is not reader or
                    getattr(self, 'game_pid', None) != identity[1] or
                    self.state_report is not report):
                path.unlink(missing_ok=True)
                self.state_probe_status.set('Japanese connection changed; XYZ export discarded.')
                return
            if error is not None:
                self.state_probe_status.set(f'XYZ full export failed: {error}')
                return
            self.state_probe_status.set(
                f'Exported ALL {count} XYZ candidates to {path}; '
                'interactive table remains limited to top 200. '
                'No raw snapshots or guest writes.')

        threading.Thread(target=worker, daemon=True,
                         name='GoemonJapanXYZFullExport').start()
        self.root.after(70, poll)

    def export_state_probe(self):
        if not self.state_report:
            self.state_probe_status.set('Compare A and B before exporting.')
            return
        if self.state_report.get('format') == 'goemon-japan-xyz-heuristic-v1':
            self._export_all_japan_xyz_candidates()
            return
        try:
            prefix = ('japan_state_probe_' if self.state_report.get('region') == 'japan-0'
                      else 'state_probe_')
            path = diagnostics_dir() / (prefix +
                datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
            path.write_text(json.dumps(self.state_report,indent=2)+'\n',encoding='utf-8')
            self.state_probe_status.set(f'Exported comparison to {path}')
        except OSError as exc:
            self.state_probe_status.set(f'Export failed: {exc}')

    def copy_state_probe_address(self):
        chosen=self.state_probe_table.selection()
        if not chosen:
            self.state_probe_status.set('Select a candidate row first.')
            return
        addr=self.state_probe_table.item(chosen[0],'values')[0]
        self.root.clipboard_clear()
        self.root.clipboard_append(addr)
        self.state_probe_status.set(f'Copied candidate address {addr}; not confirmed or enabled for editing.')

    def watch_state_probe_candidate(self):
        chosen=self.state_probe_table.selection()
        if not chosen:
            self.state_probe_status.set('Select a candidate before adding it to Live Memory.')
            return
        row=self.state_probe_table.item(chosen[0],'values')
        address=row[0]
        kind='f32' if row[6] in ('f32 candidate', 'XYZ triple candidate') else 'u8'
        if self._state_is_japan():
            if self.add_japan_custom_watch_from_search(
                    address, kind,
                    label=(f'JP XYZ candidate X {address}' if
                           row[6] == 'XYZ triple candidate' else
                           f'JP A/B/C {address}')):
                self.notebook.select(self.jp_fields_tab)
            else:
                self.state_probe_status.set(self.jp_custom_watch_status.get())
            return
        self.user_watch_name.set(f'{self.state_probe_kind.get()} {address}')
        self.user_watch_address.set(address)
        self.user_watch_type.set(kind)
        self.add_custom_watch()
        self.notebook.select(self.live_memory_tab)

    def reset_state_probes(self):
        self._jp_probe_generation += 1
        self._jp_probe_busy = False
        self.state_captures={}
        self.state_report=None
        self.state_probe_table.delete(*self.state_probe_table.get_children())
        self.state_probe_status.set('Captures cleared; no game memory was written.')

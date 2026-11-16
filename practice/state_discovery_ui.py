"""Tk interface for read-only, user-labelled A/B/C N64 state probes."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import queue
import threading
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from practice.paths import diagnostics_dir
from practice.discovery_results import DiscoveryResultsPanel
from practice.reports import create_discovery_report
from practice.state_discovery import capture_state, compare_captures
from practice.theme import PALETTE
from practice.japan_state_comparison import (
    capture_japan_memory, compare_japan_memory,
)
from practice.japan_player_position_research import (
    find_japan_xyz_candidates, export_japan_xyz_all_candidates,
)
from practice.japanese_scene_probes import read_japan_scene_probes
from practice.transition_observer import read_transition_observation, format_transition_observation



class StateDiscoveryMixin:
    def build_state_discovery_tab(self, notebook):
        tab=ttk.Frame(notebook,padding=10)
        notebook.add(tab,text='Compare memory changes')
        self.state_discovery_tab=tab
        self.state_captures={}
        self.state_report=None
        self.state_report_name = tk.StringVar(value='Memory comparison')
        # Keep old capture variable as freeform report name for compatibility.
        self.state_probe_kind = self.state_report_name
        self._jp_probe_generation = 0
        self._jp_probe_busy = False
        ttk.Label(tab,text='Find memory changes before and after an action',font=('Segoe UI Semibold',16),
                  foreground=PALETTE['gold']).pack(anchor='w',pady=(2,6))
        ttk.Label(tab,text='Best for temporary values, positions, scene changes, '
                  'timers or unknown game state. Capture A (before), B (after), '
                  'and optionally C (reverted or stable). To identify persistent '
                  'bits across repeatable events, use Investigate flags instead. '
                  'Findings are candidates, not confirmed fields.',
                  style='Muted.TLabel',wraplength=1080).pack(anchor='w',pady=(0,9))
        context=ttk.LabelFrame(tab,text='Scene / boss investigation (read-only)',padding=8)
        context.pack(fill='x',pady=(0,9))
        ttk.Label(context,text='Works without a valid player object. Capture engine and Script VM context before and after a boss phase, loading screen or scene change. Values are observations, not confirmed boss HP or safe warp targets.',style='Muted.TLabel',wraplength=1050).pack(anchor='w')
        self.transition_observation_text=tk.StringVar(value='Connect to the game, then select Read scene context.')
        ttk.Button(context,text='Read scene context',command=self.read_scene_context).pack(anchor='w',pady=(5,3))
        ttk.Label(context,textvariable=self.transition_observation_text,wraplength=1050,justify='left').pack(anchor='w')
        row=ttk.Frame(tab);row.pack(fill='x',pady=(0,6))
        # The common Results toolbar owns the single editable experiment name.
        ttk.Label(row,text='Capture scope').pack(side='left',padx=(0,6))
        self.state_probe_scope=tk.StringVar(value='focused')
        ttk.Combobox(row,textvariable=self.state_probe_scope,values=('focused','wide'),
                     width=10,state='readonly').pack(side='left')
        self.state_probe_instruction=tk.StringVar(value=(
            'The name only labels the captures and report. Focused reads '
            'selected game globals and available player memory. Wide compares '
            'full guest RAM. No preset limits the search.'))
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
        ttk.Button(row,text='Clear',command=self.reset_state_probes).pack(side='left')
        self.state_xyz_export_row = ttk.Frame(tab)
        self.state_xyz_export_row.pack(fill='x', pady=(0, 6))
        self.state_xyz_full_export_button = ttk.Button(
            self.state_xyz_export_row,
            text='Export all XYZ candidates (advanced JSON)',
            command=self._export_all_japan_xyz_candidates)
        self.state_xyz_full_export_note = ttk.Label(
            self.state_xyz_export_row,
            text='Exhaustive cached A/B/C analysis; may create a large legacy JSON file.',
            wraplength=790)
        # Normally hidden, since the standard Save report handles ordinary A/B/C.
        self.state_xyz_full_export_button.pack_forget()
        self.state_probe_status=tk.StringVar(value='No captures. Name an investigation and connect to the game.')
        ttk.Label(tab,textvariable=self.state_probe_status,wraplength=1060).pack(anchor='w',pady=(0,10))
        self.state_probe_results = DiscoveryResultsPanel(
            self, tab, tree=lambda: self.state_probe_table,
            status=self.state_probe_status,
            report_name=self.state_report_name,
            label='Memory comparison', save=self.export_state_probe)
        self.state_probe_export_button = self.state_probe_results.save_button
        self.state_probe_selector = self.state_probe_results.report_entry
        self.state_probe_results.controls.pack_configure(before=context)
        headings=('address','type','live','raw','region','before','after','bitmask','returned')
        frame=ttk.Frame(tab);frame.pack(fill='both',expand=True)
        self.state_probe_table=ttk.Treeview(
            frame,columns=headings,show='headings',selectmode='extended',height=15)
        for key,heading,width in (
                ('address','N64 address',145),('type','Type',135),
                ('live','Live value',140),('raw','Live hex',145),
                ('region','Region',130),('before','A: before',95),
                ('after','B: after',95),('bitmask','XOR mask',85),
                ('returned','C matched A?',125)):
            self.state_probe_table.heading(key,text=heading)
            self.state_probe_table.column(key,width=width,stretch=key=='region')
        bar=ttk.Scrollbar(frame,orient='vertical',command=self.state_probe_table.yview)
        self.state_probe_table.configure(yscrollcommand=bar.set)
        self.state_probe_table.pack(side='left',fill='both',expand=True)
        bar.pack(side='right',fill='y')
        ttk.Label(tab,text='A/B comparisons identify hypotheses, not proven game fields. '
                  'Live updates do not alter A/B/C evidence.',style='Muted.TLabel',
                  wraplength=1050).pack(anchor='w',pady=(6,0))

    def _state_is_japan(self):
        return getattr(getattr(self, 'active_version', None), 'key', 'usa') == 'japan'

    def _set_state_probe_instruction(self):
        # Legacy API: the experiment name does not change the search policy.
        self.state_probe_instruction.set(
            'Report name is a label only. Capture A before and B after. '
            'Optional C retains only changes that revert to A; skip C for '
            'irreversible or persistent events. For Japan XYZ research, '
            'capture wide A still, B moved and C still at B, then use '
            'Find XYZ triples.')

    def configure_state_probe_region(self):
        # Never reset a user's investigation name on a game-region change.
        self._set_state_probe_instruction()
        self.state_probe_capture_buttons['C'].configure(
            text='Capture C: Optional')
        if self._state_is_japan():
            self.state_xyz_button.pack(side='left', padx=(0, 7))
        else:
            self.state_xyz_button.pack_forget()
            self.state_xyz_full_export_button.pack_forget()
            self.state_xyz_full_export_note.pack_forget()
        self.state_probe_scope_hint.set(
            'Japan focused: two 4 KiB engine/save candidate ranges (not '
            'confirmed saved-event banks). Wide: full 4/8 MiB Japanese RDRAM. '
            'XYZ search requires wide A still, B moved, C still at B.'
            if self._state_is_japan() else
            'USA focused: global state and available player/task regions. '
            'Wide: full 4 MiB guest RAM. Snapshot labels do not filter addresses.')

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
            self.state_xyz_full_export_button.pack_forget()
            self.state_xyz_full_export_note.pack_forget()
            self.state_probe_export_button.configure(text='Save report')
            self.state_probe_table.heading('returned', text='C matched A?')
            self.state_probe_table.column('before', width=95)
            self.state_probe_table.column('after', width=95)
            self.state_probe_table.delete(*self.state_probe_table.get_children())
            for i,row in enumerate(report['candidates']):
                self.state_probe_table.insert('','end',iid=str(i),values=(
                    row['address'],row['kind'],'—','—',row['region'],
                    row['before'],row['after'],row['xor_mask'],
                    'yes' if row['reverted'] else '—'))
            self.state_probe_results.label = (
                'JP A/B/C' if self._state_is_japan() else 'Memory comparison')
            self.state_probe_results.refresh_now()
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
            self.state_probe_export_button.configure(text='Save report')
            self.state_xyz_full_export_button.pack(side='left', padx=(0, 10))
            self.state_xyz_full_export_note.pack(side='left')
            self.state_probe_table.delete(*self.state_probe_table.get_children())
            self.state_probe_table.heading('returned', text='C stable at B?')
            self.state_probe_table.column('before', width=205)
            self.state_probe_table.column('after', width=205)
            for i, row in enumerate(report['candidates']):
                self.state_probe_table.insert('', 'end', iid=str(i), values=(
                    row['address'], row['kind'], '—', '—', row['region'],
                    row['before'], row['after'], row['xor_mask'],
                    'yes' if row['c_stable_at_b'] else '—'))
            self.state_probe_results.label = 'JP XYZ candidate'
            self.state_probe_results.refresh_now()
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
            self.state_probe_status.set('Capture and compare A/B first.')
            return
        if self._jp_probe_busy:
            self.state_probe_status.set('Finish the current Japanese operation first.')
            return
        try:
            report = self.state_report
            counts = report.get('counts', {})
            rows = list(report.get('candidates', []))
            region = 'japan' if self._state_is_japan() else 'usa'
            source_capture_info = {}
            for label, capture in self.state_captures.items():
                source_capture_info[label] = {
                    'label': capture.label,
                    'captured_utc': capture.utc,
                    'map_id': capture.map_id,
                    'character': capture.character,
                    'scope': capture.scope,
                    'regions': [
                        {'name': reg.name,
                         'guest_start': f'0x{reg.address:08X}',
                         'byte_count': len(reg.data),
                         'sha256': hashlib.sha256(reg.data).hexdigest()}
                        for reg in capture.regions
                    ],
                }
            xyz = report.get('format') == 'goemon-japan-xyz-heuristic-v1'
            total = counts.get('candidate_count', len(rows))
            scope = self.state_probe_scope.get()
            title = (
                f'{self.state_probe_kind.get()} - XYZ candidates'
                if xyz else self.state_probe_kind.get())
            folder = create_discovery_report(
                region=region,
                title=title,
                kind='memory-comparison',
                candidates=rows,
                candidate_total=total,
                evidence={
                    'analysis': report,
                    'capture_provenance': source_capture_info,
                },
                metadata={
                    'comparison': ('A vs B vs C' if 'C' in self.state_captures
                                   else 'A vs B'),
                    'scope': scope,
                    'capture_count': len(self.state_captures),
                    'method': 'XYZ float triple ranking' if xyz else 'RAM snapshot comparison',
                    'analyzed_changes': counts.get('observed_changes', None),
                    'regions_compared': counts.get('regions_compared', None),
                },
                notes=[
                    'Full captured RAM is not duplicated into these reports. '
                    'Each captured region has an address, length and SHA-256 '
                    'fingerprint; observed candidate values are saved.',
                    'The underlying comparison may limit its ranked candidates '
                    'to a preview. Counts in the manifest disclose omitted rows.',
                    'Only correlations were found, not original MIPS readers/writers.',
                    'Wide Japanese XYZ research has a separate exhaustive export '
                    'that may be large.' if xyz else
                    'For repeated stable event bits use Investigate flags.',
                ])
            if hasattr(self, 'refresh_reports'):
                self.refresh_reports(select_path=folder)
            self.state_probe_status.set(
                f'Saved {len(rows)}/{total} candidate rows and '
                f'{len(source_capture_info)} capture records. Open Reports.')
            if xyz:
                # The original exhaustive XYZ file is still available as a
                # specialist advanced export, not silently substituted for the
                # standard investigation report.
                self.state_probe_status.set(
                    f'Saved XYZ report ({len(rows)}/{total} ranked rows). '
                    'Use the separate exhaustive XYZ function for all triples.')
        except (OSError, ValueError, TypeError, KeyError) as exc:
            self.state_probe_status.set(f'Save report failed: {exc}')

    def copy_state_probe_address(self):
        self.state_probe_results.copy_address()
        self.state_probe_status.set(self.state_probe_results.live_status.get())

    def watch_state_probe_candidate(self):
        self.state_probe_results.watch_selected()
        self.state_probe_status.set(self.state_probe_results.live_status.get())

    def reset_state_probes(self):
        self._jp_probe_generation += 1
        self._jp_probe_busy = False
        self.state_captures={}
        self.state_report=None
        self.state_probe_export_button.configure(text='Save report')
        self.state_xyz_full_export_button.pack_forget()
        self.state_xyz_full_export_note.pack_forget()
        self.state_probe_table.delete(*self.state_probe_table.get_children())
        self.state_probe_results.invalidate()
        self.state_probe_status.set('Captures cleared; no game memory was written.')

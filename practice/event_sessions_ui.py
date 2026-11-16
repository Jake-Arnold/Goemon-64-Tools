"""Event research UI: persistent-flag sessions and nested advanced RAM probes."""
import json
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog

from practice.event_sessions import (
    EVENT_START, JAPAN_CANDIDATE_START, JAPAN_BATTERY_RESEARCH_START,
    new_session, capture_event,
    capture_japan_event, with_trial, save_session, load_session, rank_bits,
    changed_context_fields, describe_contexts,
)
from practice.checkpoints import GAMEDATA_ADDR, STATE_ADDR
from practice.paths import diagnostics_dir
from practice.discovery_results import DiscoveryResultsPanel
from practice.reports import create_discovery_report, working_investigations_dir


class EventSessionsMixin:
    def build_event_sessions_tab(self,notebook):
        # Event investigations and generic memory comparison are sibling
        # research methods, not nested pages of an ambiguously named session.
        tab=ttk.Frame(notebook,padding=10)
        notebook.add(tab,text='Investigate flags')
        self.event_sessions_tab=tab
        self.event_sections=notebook
        self.event_session=None;self.event_pending={};self.event_token=None;self.event_capture_started=None
        self.event_rows=[]
        self.event_generation=0
        self.event_monitor_started=time.monotonic()
        self.root.bind('<Destroy>',self._event_session_destroyed,add='+')
        ttk.Label(tab,text='Find bits changed by repeatable game events',
                  font=('Segoe UI Semibold',16)).pack(anchor='w')
        ttk.Label(tab,text=(
            'Use this for persistent inventory/story/unlock bits when you can repeat '
            'an action. Each trial captures a 100-byte slice before (A), after (B), '
            'and optionally reverted (C). Idle/control trials expose background '
            'changes. For temporary values, movement and broad changes use '
            'Compare memory changes instead. This method is read-only.'),
            wraplength=1080).pack(anchor='w',pady=6)
        row=ttk.Frame(tab);row.pack(fill='x')
        ttk.Label(row,text='Experiment:').pack(side='left')
        self.event_label=tk.StringVar(value='Benkei first conversation')
        ttk.Entry(row,textvariable=self.event_label,width=35).pack(side='left',padx=5)
        ttk.Label(row,text='ROM SHA-1 (optional, unverified):').pack(side='left')
        self.event_rom=tk.StringVar()
        ttk.Entry(row,textvariable=self.event_rom,width=42).pack(side='left',padx=5)
        ttk.Button(row,text='New investigation',
                   command=self.new_event_session).pack(side='left')
        ttk.Button(row,text='Open investigation',
                   command=self.open_event_session).pack(side='left',padx=5)
        row=ttk.Frame(tab);row.pack(fill='x',pady=7)
        ttk.Label(row,text='Repeat type:').pack(side='left',padx=(0,4))
        self.event_role=tk.StringVar(value='event')
        ttk.Combobox(row,textvariable=self.event_role,values=('event','idle','control'),state='readonly',width=10).pack(side='left')
        self.event_note=tk.StringVar()
        ttk.Label(row,text='Note:').pack(side='left',padx=(6,0))
        ttk.Entry(row,textvariable=self.event_note,width=40).pack(side='left',padx=5)
        for stage in ('A','B','C'):
            ttk.Button(row,text='Capture '+stage,command=lambda s=stage:self.capture_event_stage(s)).pack(side='left',padx=3)
        ttk.Button(row,text='Finish trial',command=self.record_event_trial).pack(side='left',padx=3)
        ttk.Button(row,text='Discard captures',command=self.discard_event_captures).pack(side='left',padx=3)
        self.event_status=tk.StringVar(
            value='Name the investigation, then capture A=before, B=after, C=optional. '
                  'Finish trial saves working data; Save report exports the findings.')
        region_row=ttk.Frame(tab)
        region_row.pack(fill='x', pady=(0, 4))
        ttk.Label(region_row, text='100-byte research window:').pack(side='left')
        self.event_region_start=tk.StringVar(
            value=f'0x{(JAPAN_CANDIDATE_START if self.active_version.key == "japan" else EVENT_START):08X}')
        self.event_region_entry=ttk.Entry(
            region_row, textvariable=self.event_region_start, width=15)
        self.event_region_entry.pack(side='left', padx=(6, 8))
        self.event_battery_preset_button=ttk.Button(
            region_row, text='Sasuke battery probe',
            command=self.prepare_sasuke_battery_session)
        self.event_battery_preset_button.pack(side='left', padx=(0, 8))
        self.event_region_note=tk.StringVar(value='')
        ttk.Label(region_row, textvariable=self.event_region_note,
                  wraplength=800).pack(side='left')
        ttk.Label(tab,textvariable=self.event_status,wraplength=1100).pack(anchor='w',pady=6)
        self.event_comparison=tk.StringVar(value='No pending A/B comparison. Ranked candidates appear after Record trial; only event trials create candidates.')
        ttk.Label(tab,textvariable=self.event_comparison,wraplength=1100).pack(anchor='w',pady=4)
        self.event_live=tk.StringVar(value='Starting read-only monitor...')
        ttk.Label(tab,textvariable=self.event_live,wraplength=1100).pack(anchor='w',pady=4)
        self.event_trial_summary=tk.StringVar(value='No trials')
        ttk.Label(tab,textvariable=self.event_trial_summary,wraplength=1100).pack(anchor='w')
        self.event_results = DiscoveryResultsPanel(
            self, tab, tree=lambda: self.event_table, status=self.event_status,
            report_name=self.event_label, save=self.save_event_investigation_report,
            label='Flag research')
        columns=('address','type','live','raw','mask','direction',
                 'support','opposite','absent','noise','reverted')
        result_frame=ttk.Frame(tab);result_frame.pack(fill='both',expand=True)
        self.event_table=ttk.Treeview(
            result_frame,columns=columns,show='headings',
            selectmode='extended',height=12)
        headers=(('address','N64 address',145),('type','Type',95),
                 ('live','Live value',140),('raw','Live hex',145),
                 ('mask','Bit mask',90),('direction','Direction',95),
                 ('support','Event support',125),('opposite','Opposite',95),
                 ('absent','Unchanged',95),('noise','Control overlap',135),
                 ('reverted','C reverted',110))
        for key,title,width in headers:
            self.event_table.heading(key,text=title)
            self.event_table.column(key,width=width,stretch=key in ('live','raw'))
        scroll=ttk.Scrollbar(
            result_frame,orient='vertical',command=self.event_table.yview)
        scroll.pack(side='right',fill='y')
        self.event_table.configure(yscrollcommand=scroll.set)
        self.event_table.pack(side='left',fill='both',expand=True)
        self.event_table.bind('<<TreeviewSelect>>',self.show_event_evidence)
        self.event_evidence=tk.Text(tab,height=4,wrap='word',background='#1a1d23',
                                   foreground='#f3eee5',insertbackground='#edbf6b')
        self.set_event_evidence('Select a row for exact trial IDs. Candidates are never automatically confirmed.')
        self.event_evidence.pack(fill='x',pady=6)
        self.root.after(250,self.poll_event_monitor)

    def prepare_sasuke_battery_session(self):
        """Set a Japanese-only read-only probe without replacing any saved session."""
        if self.active_version.key != 'japan':
            self.event_status.set('Sasuke battery probe is Japanese-only.')
            return
        self.event_region_start.set(f'0x{JAPAN_BATTERY_RESEARCH_START:08X}')
        self.event_label.set('Sasuke battery 1 acquisition')
        self.event_status.set(
            'Battery preset: read-only 100-byte range '
            '0x80161DC0–0x80161E23 covers candidate 0x80161DF9 '
            '(bit 0x20 UNVERIFIED). Create a new session and capture '
            'idle/control and repeated A/B trials.')

    def configure_event_region(self):
        """One event-sessions tab; region-correct 100-byte capture schema."""
        japan=self.active_version.key=='japan'
        self.event_region_entry.configure(
            state='normal' if japan else 'disabled')
        self.event_battery_preset_button.state(
            ['!disabled'] if japan else ['disabled'])
        if self.event_session is None or (
                self.event_session.get('region','usa') != (
                    'japan' if japan else 'usa')):
            self.event_session=None
            self.event_pending={}
            self.event_token=None
            self.event_capture_started=None
            # Invalidate asynchronous rank workers from the former ROM before
            # a stale USA result can repopulate the Japanese session table.
            self.event_generation+=1
            self.event_region_start.set(
                f'0x{JAPAN_CANDIDATE_START if japan else EVENT_START:08X}')
            self.event_rows=[]
            self.event_results.invalidate()
            self.event_table.delete(*self.event_table.get_children())
            self.event_trial_summary.set('No trials for current ROM region')
        self.event_region_note.set(
            'Japan-0: choose any 100-byte RAM region; this is NOT a '
            'verified saved-event bank. No Japanese event-bit meanings '
            'are assumed.' if japan
            else 'USA: fixed saved-event block; native mapped semantics.')
        self.event_status.set(
            'Japanese RAM bit evidence sessions are read-only; choose a '
            '100-byte region, create a session and capture A/B/C.'
            if japan else 'USA saved-event flag sessions: create a session '
            'and capture A/B/C; idle/control trials filter noise.')

    def refresh_pending_event_comparison(self):
        if not all(key in self.event_pending for key in ('A','B')):
            self.event_comparison.set('Capture A, perform the event, then capture B. Record trial to update ranked candidates.')
            return
        a=bytes.fromhex(self.event_pending['A']['bytes_hex'])
        b=bytes.fromhex(self.event_pending['B']['bytes_hex'])
        changes=[(i,x,y) for i,(x,y) in enumerate(zip(a,b)) if x!=y]
        bits=sum((x^y).bit_count() for _,x,y in changes)
        start=(self.event_session.get('event_start',EVENT_START)
               if self.event_session else EVENT_START)
        detail='; '.join(f'0x{start+i:08X}: {x:02X}->{y:02X}' for i,x,y in changes[:8])
        if len(changes)>8:detail+='; ...'
        if not changes:
            detail='The 100 saved event bytes are identical. Repeating an already-completed event may change nothing; use Advanced RAM comparison for temporary fields.'
        self.event_comparison.set(f'Pending A/B: {len(changes)} changed bytes, {bits} changed bits. '+detail+
                                  ' Record trial to include this pair in analysis. '
                                  + ('Context changed: '+', '.join(changed_context_fields(self.event_pending))+'. '
                                     if changed_context_fields(self.event_pending) else '')
                                  + describe_contexts(self.event_pending))

    def poll_event_monitor(self):
        now=time.monotonic()
        elapsed=now-self.event_monitor_started
        since=(f' | Since A: {now-self.event_capture_started:.1f}s'
               if self.event_capture_started is not None else '')
        prefix=f'UI clock: {elapsed:.1f}s{since}'
        try:
            if self.active_version.key == 'japan' and self.jp_rdram is not None:
                engine=self.jp_rdram.read_guest(0x800CD284,1)[0]
                map_id=int.from_bytes(
                    self.jp_rdram.read_guest(0x800CD2A2,2),'big')
                self.event_live.set(
                    f'{prefix} | Japan-0 scene: 0x{map_id:03X} | '
                    f'engine: {engine}; region-correct read-only session.')
            elif self.mem:
                state=self.mem.u8(STATE_ADDR)
                loops=self.mem.u16(0x800C7A8E)
                self.event_live.set(f'{prefix} | Game-loop counter: {loops} | State: {state}'
                                    ' | Counter may stop while paused; captures validate gameplay separately.')
            else:self.event_live.set(prefix+' | Disconnected; connect before capturing.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.event_live.set(prefix+f' | Read unavailable: {exc}')
        finally:
            self.root.after(250,self.poll_event_monitor)

    def _event_connection(self):
        if self.active_version.key == 'japan':
            ram=self.jp_rdram
            if ram is None:
                raise ValueError('No Japanese RAM reader attached. Connect from Dashboard.')
            if not self.game_pid:
                raise ValueError('Japanese RAM is attached but PID identity is missing. Reconnect from Dashboard.')
            if not self.jp_backend:
                raise ValueError('Japanese RAM is attached but its backend is unknown. Reconnect from Dashboard.')
            if self.connection_target.get() not in ('auto', self.jp_backend):
                raise ValueError('The selected backend differs from the attached Japanese game. Reconnect or choose auto.')
            return ((self.game_pid,'japan',id(ram),ram.base,ram.endian),
                    self.jp_backend)
        if not self.mem:
            raise ValueError('No USA game memory attached. Connect from Dashboard.')
        if not self.game_pid:
            raise ValueError('USA game RAM is attached but PID identity is missing. Reconnect from Dashboard.')
        import psutil
        name=psutil.Process(self.game_pid).name().lower()
        backend='project64' if name=='project64.exe' else ('recomp' if 'goemon64recomp' in name else None)
        if backend is None:raise ValueError('Unrecognized host; event-session backend cannot be identified')
        return (self.game_pid,id(self.mem),self.mem.base,self.mem.endian),backend

    def _event_session_destroyed(self,event):
        if event.widget is self.root:
            self.event_generation+=1
            # No queued Tk poll may target widgets after their root is destroyed.
            for callback in self.root.tk.call('after','info'):
                self.root.after_cancel(callback)

    def _event_path(self,session):
        return (working_investigations_dir(session.get('region', 'usa'))
                / ('event_session_' + session['id'] + '.json'))

    def new_event_session(self):
        try:
            _,backend=self._event_connection()
            japanese=self.active_version.key=='japan'
            start=int(self.event_region_start.get(),0)
            session=new_session(
                self.event_label.get(),backend,self.event_rom.get(),
                region='japan' if japanese else 'usa',event_start=start)
            save_session(self._event_path(session),session)
            self.event_session=session;self.event_pending={};self.event_token=None;self.event_capture_started=None
            self.refresh_pending_event_comparison()
            self.refresh_event_session()
            self.event_status.set(
            'Investigation created and autosaved. Capture an idle A/B control first. '
            'Use Save report to export its findings in the standard report format.')
        except (OSError,ValueError,RuntimeError) as exc:self.event_status.set(f'New session failed: {exc}')

    def open_event_session(self):
        path=filedialog.askopenfilename(
            parent=self.root, title='Open saved flag investigation',
            initialdir=str(working_investigations_dir(self.active_version.key)),
            filetypes=[('Investigation data', '*.json')])
        if not path:return
        try:
            session=load_session(path)
            expected='japan' if self.active_version.key=='japan' else 'usa'
            if session.get('region','usa') != expected:
                raise ValueError(f'Event session is for a different ROM region: '
                                 f'{session.get("region","usa")}')
            self.event_region_start.set(
                f'0x{session.get("event_start",EVENT_START):08X}')
            self.event_session=session;self.event_pending={};self.event_token=None;self.event_capture_started=None
            self.event_label.set(session['label']);self.event_rom.set(session['rom_sha1'] or '')
            self.refresh_pending_event_comparison()
            self.refresh_event_session()
            self.event_status.set(
            'Investigation reopened. New trials are autosaved internally; '
            'Save report creates a new readable research report.')
        except (OSError,ValueError) as exc:self.event_status.set(f'Open failed; current session retained: {exc}')

    def capture_event_stage(self,stage):
        try:
            if not self.event_session:raise ValueError('Create/open a session first')
            if stage not in ('A','B','C'):raise ValueError('Invalid capture stage')
            token,backend=self._event_connection()
            if backend!=self.event_session['backend']:raise ValueError('Backend differs; open a separate session')
            if stage!='A' and (not self.event_pending.get('A') or token!=self.event_token):
                raise ValueError('Connection changed or A missing; capture a fresh A')
            if stage=='C' and 'B' not in self.event_pending:raise ValueError('Capture B before optional C')
            if self.event_session.get('region','usa') != self.active_version.key:
                raise ValueError('Saved event session belongs to the other ROM region')
            capture=(capture_japan_event(
                        self.jp_rdram,
                        event_start=self.event_session['event_start'])
                     if self.active_version.key=='japan'
                     else capture_event(self.mem))
            if stage=='A':
                self.event_pending={};self.event_token=token
                self.event_capture_started=time.monotonic()
            if stage=='B':self.event_pending.pop('C',None)
            self.event_pending[stage]=capture
            self.refresh_pending_event_comparison()
            self.event_status.set(f'{stage} captured. Pending {", ".join(self.event_pending)}. Finish dialogue before B; record trial when ready.')
        except (OSError,ValueError,RuntimeError) as exc:
            self.event_pending={};self.event_token=None;self.event_capture_started=None
            self.refresh_pending_event_comparison()
            self.event_status.set(f'Capture discarded: {exc}')

    def record_event_trial(self):
        try:
            token,backend=self._event_connection()
            if token!=self.event_token or not self.event_session or backend!=self.event_session['backend']:
                raise ValueError('Connection changed; discard captures and start a fresh A')
            session=with_trial(self.event_session,self.event_role.get(),self.event_note.get(),self.event_pending)
            save_session(self._event_path(session),session)
            self.event_session=session;self.event_pending={};self.event_token=None;self.event_capture_started=None
            self.refresh_pending_event_comparison()
            self.refresh_event_session()
            self.event_status.set(
            'Trial recorded and autosaved. For another trial, restore the same '
            'pre-event game state and capture A again. Save report when ready.')
        except (OSError,ValueError,RuntimeError) as exc:self.event_status.set(f'Trial not recorded: {exc}')

    def save_event_investigation_report(self):
        session = self.event_session
        if not session:
            self.event_status.set("Create or open an investigation first.")
            return
        try:
            ranked = rank_bits(session)
            rows = ranked['candidates']
            role_counts = {
                role: sum(trial['role'] == role for trial in session['trials'])
                for role in ('event', 'idle', 'control')
            }
            folder = create_discovery_report(
                region=session.get('region', 'usa'),
                title=session['label'],
                kind='flag-investigation',
                candidates=rows,
                evidence={
                    'working_investigation': session,
                    'ranked_bit_analysis': ranked,
                    'pending_captures_not_yet_recorded': dict(self.event_pending),
                },
                metadata={
                    'backend': session['backend'],
                    'event_region_start': f"0x{session['event_start']:08X}",
                    'event_region_bytes': 100,
                    'trial_counts': role_counts,
                    'rom_sha1_user_supplied_unverified': session.get('rom_sha1'),
                    'working_investigation_id': session['id'],
                },
                notes=[
                    'Every saved trial includes original 100-byte A/B/C values '
                    'and gameplay context in session.json.',
                    'Pending A/B/C captures are included but not ranked until '
                    'the trial is finished.',
                    'Japanese candidate regions are not verified saved-event banks.'
                    if session.get('region') == 'japan'
                    else 'USA saved-event flag meanings require separate verification.',
                    'A changed bit does not establish semantic meaning or write safety.',
                ])
            if hasattr(self, 'refresh_reports'):
                self.refresh_reports(select_path=folder)
            self.event_status.set(
                f"Saved {len(rows)} bit candidates and {len(session['trials'])} "
                "completed trial(s). Open Reports to view the investigation.")
        except (OSError, ValueError, TypeError) as exc:
            self.event_status.set(f"Save report failed: {exc}")

    def discard_event_captures(self):
        self.event_pending={};self.event_token=None;self.event_capture_started=None
        self.refresh_pending_event_comparison()
        self.event_status.set('Pending captures discarded; saved trials retained. No game writes made.')

    def refresh_event_session(self):
        session=self.event_session
        self.event_rows=[]
        self.event_results.invalidate()
        self.event_generation+=1
        generation=self.event_generation
        counts={role:sum(t['role']==role for t in session['trials']) for role in ('event','idle','control')}
        changed=sum(bool(changed_context_fields(t['captures'])) for t in session['trials'])
        summary=(f'{session["label"]} | {session["backend"]} '
                 f'| {session.get("region","usa").upper()} '
                 f'| 100-byte slice 0x{session.get("event_start",EVENT_START):08X} '
                 f'| ROM identity unverified | Trials: {counts} '
                 f'| Context-changing trials: {changed}')
        self.event_trial_summary.set(summary+' | Analysing…')
        self.event_table.delete(*self.event_table.get_children())
        self.set_event_evidence('Select a row for trial IDs. No semantic meaning or write safety is established.')
        results=queue.SimpleQueue()
        def worker():
            try:results.put((True,rank_bits(session)['candidates']))
            except Exception as exc:results.put((False,str(exc)))
        def poll():
            if generation!=self.event_generation:return
            try:ok,result=results.get_nowait()
            except queue.Empty:
                self.root.after(40,poll);return
            if not ok:
                self.event_trial_summary.set(summary+' | Analysis failed: '+result);return
            self.event_rows=result
            for i,row in enumerate(result):
                self.event_table.insert('','end',iid=str(i),values=(
                    row['address'],'u8','—','—',row['mask'],row['direction'],
                    f'{len(row["support"])}/{row["event_trials"]}',
                    len(row['opposite']),len(row['absent']),
                    len(row['control_overlap']),len(row['reverted'])))
            self.event_trial_summary.set(summary+f' | {len(result)} bit candidates')
            self.event_results.refresh_now()
        threading.Thread(target=worker,daemon=True,name='GoemonEventRanking').start()
        self.root.after(40,poll)

    def set_event_evidence(self,text):
        self.event_evidence.configure(state='normal')
        self.event_evidence.delete('1.0','end');self.event_evidence.insert('1.0',text)
        self.event_evidence.configure(state='disabled')

    def show_event_evidence(self,_event=None):
        selected=self.event_table.selection()
        if selected:
            row=self.event_rows[int(selected[0])]
            related=set(row['support']+row['opposite']+row['absent']+row['control_overlap'])
            descriptions='\n'.join(f'{t["id"]}: {t["role"]} — {t["note"]} | '+describe_contexts(t['captures'])
                                    for t in self.event_session['trials'] if t['id'] in related)
            self.set_event_evidence(json.dumps(row,sort_keys=True)+'\n'+descriptions)

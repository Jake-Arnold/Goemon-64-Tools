"""Story observations and explicit edits to individual known values."""
import tkinter as tk
from tkinter import ttk
from practice.story_progress import read_story_state,story_rows,story_edit_options,write_story_value


class StoryProgressMixin:
    def build_story_progress_tab(self,notebook):
        tab=ttk.Frame(notebook,padding=10)
        notebook.insert(2,tab,text='Story progress');self.story_progress_tab=tab
        ttk.Label(tab,text='Known story flags',font=('Segoe UI Semibold',16)).pack(anchor='w')
        ttk.Label(tab,text='Live US flag observations. Summaries cover mapped conditions; location, character and actor state can affect dialogue. '
                  'Sequential samples may change during scripts/reloads. Editing flags does not execute rewards or cutscenes.',
                  wraplength=1080,style='Muted.TLabel').pack(anchor='w',pady=6)
        self.benkei_story=tk.StringVar(value='Benkei: —');self.ushiwaka_story=tk.StringVar(value='Ushiwaka: —')
        ttk.Label(tab,textvariable=self.benkei_story).pack(anchor='w')
        ttk.Label(tab,textvariable=self.ushiwaka_story).pack(anchor='w',pady=(2,7))
        filter_row=ttk.Frame(tab);filter_row.pack(fill='x',pady=(0,6))
        ttk.Label(filter_row,text='Filter flags / address / evidence:').pack(side='left')
        self.story_filter=tk.StringVar()
        ttk.Entry(filter_row,textvariable=self.story_filter,width=42).pack(side='left',padx=6)
        ttk.Label(filter_row,text='Filter “external” for the added source annotations.',style='Muted.TLabel').pack(side='left')
        self._story_row_ids=[]
        self._story_edit_key=None
        self.story_filter.trace_add('write',lambda *_:self.filter_story_progress())
        columns=('bank','address','mask','value','raw','evidence')
        frame=ttk.Frame(tab);frame.pack(fill='both',expand=True)
        self.story_table=ttk.Treeview(frame,columns=columns,show='tree headings',height=16)
        self.story_table.heading('#0',text='Known flag / watch');self.story_table.column('#0',width=300)
        for key,label,width in (('bank','Bank',130),('address','Guest address',110),('mask','Mask',60),
                                ('value','Observed state',100),('raw','Raw value',100),('evidence','Evidence',300)):
            self.story_table.heading(key,text=label);self.story_table.column(key,width=width,stretch=key=='evidence')
        scroll=ttk.Scrollbar(frame,orient='vertical',command=self.story_table.yview)
        self.story_table.configure(yscrollcommand=scroll.set)
        self.story_table.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
        horizontal=ttk.Scrollbar(tab,orient='horizontal',command=self.story_table.xview)
        self.story_table.configure(xscrollcommand=horizontal.set);horizontal.pack(fill='x')
        editor=ttk.Frame(tab);editor.pack(fill='x',pady=(5,0))
        self.story_edit_label=tk.StringVar(value='Select an individual flag or ownership word')
        ttk.Label(editor,textvariable=self.story_edit_label).pack(side='left',padx=(0,8))
        self.story_edit_choice=tk.StringVar()
        self.story_edit_combo=ttk.Combobox(editor,textvariable=self.story_edit_choice,values=(),state='disabled',width=12)
        self.story_edit_combo.pack(side='left',padx=(0,6))
        self.story_edit_button=ttk.Button(editor,text='Apply state',command=self.apply_story_edit,state='disabled')
        self.story_edit_button.pack(side='left')
        self.story_edit_status=tk.StringVar(value='Select a row to edit its state.')
        ttk.Label(tab,textvariable=self.story_edit_status,wraplength=1100).pack(anchor='w')
        self.story_table.bind('<<TreeviewSelect>>',self.select_story_edit)
        self.story_notes=tk.StringVar(value='No sample yet.')
        ttk.Label(tab,textvariable=self.story_notes,wraplength=1100).pack(anchor='w',pady=7)
        ttk.Label(tab,text='Bank A/B names identify storage, not permanent story meanings. Saved flags and inventory words are separate. '
                  'Advisories are observations; no repair is performed.',style='Muted.TLabel',wraplength=1100).pack(anchor='w')

    def refresh_story_progress(self):
        state=read_story_state(self.mem)
        self.benkei_story.set('Benkei: '+state['benkei'])
        self.ushiwaka_story.set('Ushiwaka: '+state['ushiwaka'])
        self.ushiwaka_status.set('Ushiwaka: '+state['ushiwaka'])
        # Update existing rows, retaining selection and scroll position.
        rows=story_rows(state)
        for row in rows:
            values=(row['bank'],f'0x{row["address"]:08X}',row['mask'],row['value'],row['raw'],row['source'])
            if self.story_table.exists(row['key']):self.story_table.item(row['key'],text=row['name'],values=values)
            else:self.story_table.insert('','end',iid=row['key'],text=row['name'],values=values)
        self._story_row_ids=[row['key'] for row in rows]
        self.filter_story_progress()
        if self.mem is None:notes='Disconnected. Current story values are unavailable.'
        else:
            messages=list(state['advisories'])
            if state['errors']:messages.append('Some reads are unavailable: '+', '.join(state['errors']))
            notes=' '.join(messages) if messages else 'No tracked flag/inventory discrepancy observed in this sample.'
        self.story_notes.set(notes)
        if self.mem is None and self._story_edit_key is not None:self.select_story_edit()
        return state

    def filter_story_progress(self):
        query=self.story_filter.get().strip().casefold()
        desired=[]
        for key in self._story_row_ids:
            row=self.story_table.item(key)
            if query in (row['text']+' '+' '.join(str(v) for v in row['values'])).casefold():desired.append(key)
        current=list(self.story_table.get_children())
        if current==desired:return
        wanted=set(desired)
        for key in current:
            if key not in wanted:self.story_table.detach(key)
        for position,key in enumerate(desired):self.story_table.move(key,'',position)

    def select_story_edit(self, _event=None):
        selection=self.story_table.selection()
        key=selection[0] if len(selection)==1 else None
        self._story_edit_key=key
        options=story_edit_options(key) if key else ()
        value=self.story_table.item(key,'values')[3] if options else ''
        writable=bool(options and value in options and self.mem is not None and
                      getattr(self.args,'enable_hex_edit',False) and not getattr(self.args,'read_only',False))
        self.story_edit_combo.configure(values=options,state='readonly' if writable else 'disabled')
        self.story_edit_choice.set(value if value in options else '')
        self.story_edit_button.state(['!disabled'] if writable else ['disabled'])
        self.story_edit_label.set(self.story_table.item(key,'text') if options else 'Select an individual flag or ownership word')
        if not options:self.story_edit_status.set('Aggregate bank rows are read-only.')
        elif not writable:self.story_edit_status.set('Connect with memory editing enabled and an available value.')
        else:self.story_edit_status.set('Choose the desired state, then apply it.')

    def apply_story_edit(self):
        try:
            if self.mem is None:raise ValueError('Connect to a game first')
            if getattr(self.args,'read_only',False) or not getattr(self.args,'enable_hex_edit',False):
                raise PermissionError('Memory editing is disabled')
            selection=self.story_table.selection()
            if len(selection)!=1:raise ValueError('Select one story row')
            key=selection[0]
            if key != self._story_edit_key:raise ValueError('Selection changed; select the desired state again')
            options=story_edit_options(key)
            if not options:raise ValueError('Select an individual flag or ownership word')
            values=self.story_table.item(key,'values'); raw=str(values[4])
            if not raw.startswith('0x'):raise ValueError('The observed value is unavailable; refresh first')
            expected=bytes.fromhex(raw[2:])
            target=self.story_edit_choice.get()
            changed=write_story_value(self.mem,key,target,expected)
            name=self.story_table.item(key,'text')
            if changed:
                self.append_event(f'USER STORY WRITE {name}: {target}')
                self.last_inspect_at=0.0
            self.refresh_unlocks(force=True)
            self.story_edit_status.set(f'{name}: {target}' + (' (verified)' if changed else ' (unchanged)'))
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:
            self.story_edit_status.set(f'Story write failed: {exc}')

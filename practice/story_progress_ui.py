"""Story observations and explicit edits to individual known values."""
import tkinter as tk
from tkinter import ttk
from practice.story_progress import (read_story_state,story_rows,story_edit_options,
                                     write_story_value,STORY_SECTIONS,story_section_for_key)


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
        self._story_display_region = None
        self._story_row_ids_by_section={section:[] for section in STORY_SECTIONS}
        self._story_edit_key=None
        self._story_render_cache={}
        self.story_filter.trace_add('write',lambda *_:self.filter_story_progress())
        self.story_sections=ttk.Notebook(tab)
        self.story_sections.pack(fill='both',expand=True)
        self.story_tables={}
        columns=('bank','address','mask','value','raw','evidence')
        for section in STORY_SECTIONS:
            pane=ttk.Frame(self.story_sections,padding=(2,6))
            self.story_sections.add(pane,text=section)
            frame=ttk.Frame(pane);frame.pack(fill='both',expand=True)
            table=ttk.Treeview(frame,columns=columns,show='tree headings',height=13)
            table.heading('#0',text='Known flag / watch');table.column('#0',width=300)
            for key,label,width in (('bank','Bank',130),('address','Guest address',110),('mask','Mask',60),
                                    ('value','Observed state',100),('raw','Raw value',100),('evidence','Evidence',300)):
                table.heading(key,text=label)
                table.column(key,width=width,stretch=key=='evidence')
            scroll=ttk.Scrollbar(frame,orient='vertical',command=table.yview)
            table.configure(yscrollcommand=scroll.set)
            table.pack(side='left',fill='both',expand=True);scroll.pack(side='right',fill='y')
            horizontal=ttk.Scrollbar(pane,orient='horizontal',command=table.xview)
            table.configure(xscrollcommand=horizontal.set)
            horizontal.pack(fill='x')
            table.bind('<<TreeviewSelect>>',self.select_story_edit)
            self.story_tables[section]=table
        self.story_table=self.story_tables['All']
        self.story_sections.bind('<<NotebookTabChanged>>',self.select_story_edit)
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
        self.story_notes=tk.StringVar(value='No sample yet.')
        ttk.Label(tab,textvariable=self.story_notes,wraplength=1100).pack(anchor='w',pady=7)
        ttk.Label(tab,text='Diagnostics contains raw Bank A/B samples, not interpreted permanent story meanings. Saved flags and inventory words are separate. '
                  'Advisories are observations; no repair is performed.',style='Muted.TLabel',wraplength=1100).pack(anchor='w')

    def _update_story_row(self, section, key, name, values):
        """Shared cached Treeview updater for both ROM regions."""
        table = self.story_tables[section]
        stamp = (name, tuple(values))
        slot = (section, key)
        if not table.exists(key):
            table.insert('', 'end', iid=key, text=name, values=values)
            self._story_render_cache[slot] = stamp
            return True
        if self._story_render_cache.get(slot) != stamp:
            table.item(key, text=name, values=values)
            self._story_render_cache[slot] = stamp
            return True
        return False

    def refresh_story_progress(self):
        if self.active_version.key == 'japan':
            return self.refresh_japan_story_progress()
        if self._story_display_region != 'usa':
            for table in self.story_tables.values():
                table.delete(*table.get_children())
            self._story_display_region = 'usa'
            self._story_render_cache.clear()
        state=read_story_state(self.mem)
        self.benkei_story.set('Benkei: '+state['benkei'])
        self.ushiwaka_story.set('Ushiwaka: '+state['ushiwaka'])
        rows=story_rows(state)
        grouped={section:[] for section in STORY_SECTIONS}
        changed = False
        for row in rows:
            key=row['key']
            section=story_section_for_key(key)
            values=(row['bank'],f'0x{row["address"]:08X}',row['mask'],
                    row['value'],row['raw'],row['source'])
            for target in ('All',section):
                changed = self._update_story_row(target,key,row['name'],values) or changed
                grouped[target].append(key)
        self._story_row_ids=[row['key'] for row in rows]
        self._story_row_ids_by_section=grouped
        if changed:
            self.filter_story_progress()
        if self.mem is None:notes='Disconnected. Current story values are unavailable.'
        else:
            messages=list(state['advisories'])
            if state['errors']:messages.append('Some reads are unavailable: '+', '.join(state['errors']))
            notes=' '.join(messages) if messages else 'No tracked flag/inventory discrepancy observed in this sample.'
        self.story_notes.set(notes)
        if self.mem is None and self._story_edit_key is not None:self.select_story_edit()
        return state

    def refresh_japan_story_progress(self):
        """Show confirmed Japanese inventory progress, not invented event bits."""
        from practice.region_views import japan_story_fields, japan_story_crosswalk_rows
        from practice.japanese_fields import read_japan_field
        from practice.japan_story_progress import (
            JAPAN_PROGRESS_ITEMS, japan_progress_row)
        from practice.region_unlocks import japan_unlock_lead
        region_switched = self._story_display_region != 'japan'
        if region_switched:
            for table in self.story_tables.values():
                table.delete(*table.get_children())
            self._story_display_region = 'japan'
            self._story_edit_key = None
            self._story_render_cache.clear()
        self.benkei_story.set('Benkei: Japanese story flag not mapped')
        self.ushiwaka_story.set('Ushiwaka: Japanese story flag not mapped')
        grouped={section:[] for section in STORY_SECTIONS}
        changed = False
        for item in JAPAN_PROGRESS_ITEMS.values():
            record = japan_progress_row(item, self.jp_rdram)
            key = record['key']
            values = (record['bank'], f'0x{record["address"]:08X}',
                      record['mask'], record['value'],
                      record['raw'], record['source'])
            for target in ('All', record['section']):
                changed = self._update_story_row(target,key,record['name'],values) or changed
                grouped[target].append(key)
        # Older raw Japan field cards are still useful for map and bonus
        # research, but skip duplicates already present as live-verified
        # named rows above.
        seen_addresses = {
            japan_unlock_lead(item).address
            for item in JAPAN_PROGRESS_ITEMS.values()
        }
        for field in japan_story_fields():
            if field.address in seen_addresses:
                continue
            key='jp_'+field.key
            if self.jp_rdram is not None:
                result=read_japan_field(self.jp_rdram,field)
                value,raw,status=result.value,result.raw,result.status
            else:
                value,raw,status='—','—','Disconnected'
            section=('Collectibles & Miracles'
                     if field.group=='Items' else
                     'Other story' if field.group=='World map'
                     else 'Diagnostics')
            row=(field.group, f'0x{field.address:08X}', '—',
                 value, '0x'+raw if raw!='—' else '—',
                 f'Japan-0 {field.key}; {status}; NOT USA story bit')
            for target in ('All',section):
                changed = self._update_story_row(target,key,field.label,row) or changed
                grouped[target].append(key)
        # Crosswalk saved-event and Plasma flag addresses belong in the
        # existing Story Progress table, not a Japan-only diagnostic panel.
        # Selecting these research rows cannot enable the inventory editor.
        for record in japan_story_crosswalk_rows(self.jp_rdram):
            key = record['key']
            row = (record['bank'], f'0x{record["address"]:08X}',
                   record['mask'], record['value'], record['raw'],
                   record['source'])
            for target in ('All', record['section']):
                changed = self._update_story_row(target,key,record['name'],row) or changed
                grouped[target].append(key)
        self._story_row_ids=grouped['All']
        self._story_row_ids_by_section=grouped
        if changed or region_switched:
            self.filter_story_progress()
        if region_switched:
            self.select_story_edit()
        self.story_notes.set(
            f'{len(JAPAN_PROGRESS_ITEMS)} user-verified inventory/party progress '
            'rows plus Japanese map/bonus research fields. '
            'Named progress rows can be edited. Cross-region story/Plasma '
            'bit candidates are read-only research and not verified events.')
        return {'region':'japan', 'mapped_inventory_rows':len(JAPAN_PROGRESS_ITEMS),
                'mapped_candidates':len(grouped['All'])}

    def _active_story_table(self):
        section=self.story_sections.tab(self.story_sections.select(),'text')
        return self.story_tables[section]

    def filter_story_progress(self):
        query=self.story_filter.get().strip().casefold()
        for section,table in self.story_tables.items():
            desired=[]
            for key in self._story_row_ids_by_section[section]:
                row=table.item(key)
                if query in (row['text']+' '+' '.join(str(v) for v in row['values'])).casefold():
                    desired.append(key)
            current=list(table.get_children())
            if current==desired:continue
            wanted=set(desired)
            for key in current:
                if key not in wanted:table.detach(key)
            for position,key in enumerate(desired):table.move(key,'',position)

    def select_story_edit(self, _event=None):
        table=self._active_story_table()
        selection=table.selection()
        key=selection[0] if len(selection)==1 else None
        self._story_edit_key=key
        if self.active_version.key == 'japan':
            from practice.japan_story_progress import (
                JAPAN_PROGRESS_ITEMS, japan_progress_edit_options)
            slug = key.removeprefix('jp_unlock_') if key else None
            item = (JAPAN_PROGRESS_ITEMS.get(slug)
                    if key and key.startswith('jp_unlock_') else None)
            options = japan_progress_edit_options(item) if item else ()
            value = table.item(key, 'values')[3] if options else ''
            writable = bool(
                options and value in options and
                self._japan_unlock_controls_ready())
            self.story_edit_combo.configure(
                values=options, state='readonly' if writable else 'disabled')
            self.story_edit_choice.set(value if writable else '')
            self.story_edit_button.state(
                ['!disabled'] if writable else ['disabled'])
            self.story_edit_label.set(
                table.item(key, 'text') if item else
                'Japanese saved-event bits and research fields: read-only')
            self.story_edit_status.set(
                'Choose a verified Japanese inventory value, then Apply state.'
                if writable else
                'Only live-verified Japanese inventory fields are editable here.')
            return
        options=story_edit_options(key) if key else ()
        value=table.item(key,'values')[3] if options else ''
        writable=bool(options and value in options and self.mem is not None and
                      getattr(self.args,'enable_hex_edit',False) and not getattr(self.args,'read_only',False))
        self.story_edit_combo.configure(values=options,state='readonly' if writable else 'disabled')
        self.story_edit_choice.set(value if value in options else '')
        self.story_edit_button.state(['!disabled'] if writable else ['disabled'])
        self.story_edit_label.set(table.item(key,'text') if options else 'Select an individual flag or ownership word')
        if not options:self.story_edit_status.set('Aggregate bank rows are read-only.')
        elif not writable:self.story_edit_status.set('Connect with memory editing enabled and an available value.')
        else:self.story_edit_status.set('Choose the desired state, then apply it.')

    def apply_story_edit(self):
        if self.active_version.key == 'japan':
            from practice.japan_story_progress import (
                JAPAN_PROGRESS_ITEMS, japan_progress_edit_options)
            from practice.region_unlocks import japan_unlock_lead
            try:
                table = self._active_story_table()
                selection = table.selection()
                if len(selection) != 1:
                    raise ValueError('Select one Japanese progress row')
                key = selection[0]
                if key != self._story_edit_key or not key.startswith('jp_unlock_'):
                    raise ValueError('Select a verified Japanese progress entry first')
                item = JAPAN_PROGRESS_ITEMS.get(key.removeprefix('jp_unlock_'))
                if item is None or not self._japan_unlock_controls_ready():
                    raise PermissionError('Connect Japanese write-enabled RDRAM first')
                target_text = self.story_edit_choice.get()
                if target_text not in japan_progress_edit_options(item):
                    raise ValueError('Select a valid Japanese progress state')
                shown = str(table.item(key, 'values')[4])
                if not shown.startswith('0x'):
                    raise RuntimeError('Progress value unavailable; refresh')
                lead = japan_unlock_lead(item)
                before = self.jp_rdram.read_guest(lead.address, lead.width)
                if before != bytes.fromhex(shown[2:]):
                    raise RuntimeError('Japanese progress changed; refresh before editing')
                changed, _ = self.apply_japan_unlocks(
                    ((item, int(target_text, 16)),))
                self.refresh_story_progress()
                self.refresh_unlocks(force=True)
                self.story_edit_status.set(
                    f'{item.label}: {target_text} ' +
                    ('(written)' if changed else '(unchanged)'))
            except (OSError, ValueError, RuntimeError, PermissionError) as exc:
                self.story_edit_status.set(f'Japanese progress edit blocked: {exc}')
            return
        try:
            if self.mem is None:raise ValueError('Connect to a game first')
            if getattr(self.args,'read_only',False) or not getattr(self.args,'enable_hex_edit',False):
                raise PermissionError('Memory editing is disabled')
            table=self._active_story_table()
            selection=table.selection()
            if len(selection)!=1:raise ValueError('Select one story row')
            key=selection[0]
            if key != self._story_edit_key:raise ValueError('Selection changed; select the desired state again')
            options=story_edit_options(key)
            if not options:raise ValueError('Select an individual flag or ownership word')
            values=table.item(key,'values'); raw=str(values[4])
            if not raw.startswith('0x'):raise ValueError('The observed value is unavailable; refresh first')
            expected=bytes.fromhex(raw[2:])
            target=self.story_edit_choice.get()
            changed=write_story_value(self.mem,key,target,expected)
            name=table.item(key,'text')
            if changed:
                self.append_event(f'USER STORY WRITE {name}: {target}')
                self.last_inspect_at=0.0
            self.refresh_unlocks(force=True)
            self.story_edit_status.set(f'{name}: {target}' + (' (verified)' if changed else ' (unchanged)'))
        except (OSError,ValueError,RuntimeError,PermissionError) as exc:
            self.story_edit_status.set(f'Story write failed: {exc}')

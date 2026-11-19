"""USA/Japan region and persistent ROM-library UI for the Dialogue tab.

Mixin precedes DialogueMixin in the Toolkit MRO; the established USA editor,
layout and builder remain the unmodified fallback on USA operations.
"""
from __future__ import annotations

from pathlib import Path
import queue
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from practice.dialogue_rom import (load_usa_image, extract_dialogue,
    validate_flexible_replacement, export_index, save_patched_image)
from practice.dialogue_repack import save_retail_rom
from practice.dialogue_layout import font_widths_from_rom
from practice.dialogue_japan import (load_japan_image, extract_japan_dialogue,
    validate_japan_replacement, encode_japan_text, export_japan_index,
    save_japan_patched, save_japan_retail_rom)
from practice.dialogue_store import (import_rom, verify_stored,
    build_directory, open_directory, drop_paths)
from practice.dialogue_kana import (
    decode_japan_kana_preview, inferred_kana_count, japanese_query_matches,
)


class DialogueRegionMixin:
    def build_dialogue_tab(self, notebook):
        self.dialogue_region_choice = tk.StringVar(value=(
            'japan' if getattr(getattr(self,'active_version',None),'key','usa')=='japan' else 'usa'))
        self.dialogue_last_build_dir = None
        super().build_dialogue_tab(notebook)
        old_top = self.dialogue_tab.winfo_children()[0]
        old_top.pack_forget()
        header = ttk.Frame(self.dialogue_tab)
        header.pack(fill='x',pady=(0,6),before=self.dialogue_tab.winfo_children()[1])
        ttk.Label(header,text='Dialogue ROM').pack(side='left',padx=(0,5))
        self.dialogue_region_box = ttk.Combobox(
            header,textvariable=self.dialogue_region_choice,
            values=('usa','japan'),state='readonly',width=8)
        self.dialogue_region_box.pack(side='left',padx=(0,8))
        ttk.Button(header,text='Import original ROM',command=self._dialogue_open).pack(side='left',padx=(0,6))
        ttk.Button(header,text='Export index',command=self._dialogue_export).pack(side='left',padx=(0,6))
        ttk.Button(header,text='Build decompressed',command=self._dialogue_build).pack(side='left',padx=(0,6))
        self.dialogue_retail_build_button = ttk.Button(
            header,text='Build retail .z64',command=self._dialogue_build_retail)
        self.dialogue_retail_build_button.pack(side='left',padx=(0,6))
        ttk.Button(header,text='Open built ROM directory',command=self._dialogue_open_built_dir).pack(side='left')
        dropbar=ttk.Frame(self.dialogue_tab)
        self.dialogue_dropbar=dropbar
        dropbar.pack(fill='x',pady=(0,5),after=header)
        self.dialogue_drop_text=tk.StringVar(value='Drop a verified USA / Japanese ROM onto this window, or click Import original ROM.')
        ttk.Label(dropbar,textvariable=self.dialogue_drop_text).pack(anchor='w')
        # TkDND is optional at import time; never advertise an inert drop target.
        if hasattr(self.root,'drop_target_register') and hasattr(self.root,'dnd_bind'):
            try:
                self.root.drop_target_register('DND_Files')
                self.root.dnd_bind('<<Drop>>',self._dialogue_drop)
            except (tk.TclError,RuntimeError) as exc:
                self.dialogue_drop_text.set('Drag-and-drop unavailable: ' + str(exc) + '. Use Import original ROM.')
        else:
            self.dialogue_drop_text.set('Drag-and-drop requires tkinterdnd2. Use Import original ROM.')
        # Keep speculative Unicode in a separate read-only preview; never send
        # it to the Japanese encoder or ROM patcher.
        self.dialogue_kana_hypothesis_enabled=tk.BooleanVar(value=False)
        self.dialogue_kana_panel=ttk.LabelFrame(self.dialogue_tab,
            text='Experimental Japanese kana ordering — screenshot comparison ONLY',padding=5)
        ttk.Checkbutton(self.dialogue_kana_panel,
            text='Show inferred kana (unverified) in record list and preview',
            variable=self.dialogue_kana_hypothesis_enabled,
            command=self._dialogue_toggle_kana_hypothesis).pack(anchor='w')
        self.dialogue_kana_note=tk.StringVar(value=(
            'Hypothesis: hiragana tokens 14–59, katakana tokens 94–139 (+80). '
            'Only screenshot-confirmed glyphs are editable as Unicode.'))
        ttk.Label(self.dialogue_kana_panel,text=(
            'When enabled, search Japanese kana or romaji (pu, pura, purazuma). '
            'Use resource:112 to inspect a whole dialogue resource; '
            'resource:112 pu searches within it. Unverified glyphs are not searchable as romaji.'),
            wraplength=1040).pack(fill='x',anchor='w')
        ttk.Label(self.dialogue_kana_panel,textvariable=self.dialogue_kana_note,
                  wraplength=1040).pack(fill='x',anchor='w')
        self.dialogue_kana_text=tk.Text(self.dialogue_kana_panel,height=3,wrap='word',
                                       state='disabled',undo=False)
        self.dialogue_kana_text.pack(fill='x',expand=False)
        kana_buttons=ttk.Frame(self.dialogue_kana_panel)
        kana_buttons.pack(fill='x')
        ttk.Button(kana_buttons,text='Show selected resource',
                   command=self._dialogue_show_selected_resource).pack(side='left')
        ttk.Button(kana_buttons,text='Copy hypothesis preview',
                   command=self._dialogue_copy_kana_preview).pack(side='right')
        self.dialogue_region_box.bind('<<ComboboxSelected>>',lambda _event:self._dialogue_region_changed())
        self.root.after_idle(self._dialogue_region_changed)

    def _dialogue_region_changed(self):
        """Re-verify stored originals on every selection, discard cross-region edits."""
        if getattr(self,'dialogue_build_running',False):
            # Prevent switching displayed regions while the worker builds.
            if hasattr(self,'dialogue_build_region'):
                self.dialogue_region_choice.set(self.dialogue_build_region)
            return
        region=self.dialogue_region_choice.get()
        if region=='japan':
            self.dialogue_kana_panel.pack(fill='x',pady=(0,5),after=self.dialogue_dropbar)
        else:
            self.dialogue_kana_panel.pack_forget()
        self.dialogue_path=None
        self.dialogue_retail_path=verify_stored(region,'retail')
        self.dialogue_records=[]
        self.dialogue_by_key={}
        self.dialogue_staged.clear()
        self.dialogue_line_break_approved.clear()
        self.dialogue_selected_key=None
        self.dialogue_window_context=None
        self.dialogue_original_image=None
        self.dialogue_font_widths=None
        self.dialogue_editor.delete('1.0','end')
        self.dialogue_query.set('')
        self._dialogue_filter()
        path=verify_stored(region,'decompressed')
        if path is None:
            self.dialogue_status.set(f'No verified {region.upper()} original stored. Import or drop a ROM once; it will be copied into your local ROM library.')
            self.dialogue_layout_summary.set('No ROM loaded.')
            return
        try:
            image=load_usa_image(path) if region=='usa' else load_japan_image(path)
            records=extract_dialogue(image) if region=='usa' else extract_japan_dialogue(image)
            widths=font_widths_from_rom(image) if region=='usa' else None
        except (OSError,ValueError) as exc:
            self.dialogue_status.set(f'Stored {region} ROM failed validation: {exc}')
            return
        self.dialogue_path=path
        self.dialogue_original_image=image if region=='usa' else None
        self.dialogue_records=records
        self.dialogue_by_key={r.key:r for r in records}
        self.dialogue_font_widths=widths
        if region=='japan':
            self.dialogue_layout_mode.set('Measure only')
            self.dialogue_wrap_button.state(['disabled'])
            self.dialogue_mode_selector.state(['disabled'])
        else:
            self.dialogue_mode_selector.state(['!disabled','readonly'])
            self.dialogue_wrap_button.state(['!disabled'])
            self.dialogue_layout_mode.set('Native (auto when traced)')
        self._dialogue_mode_changed()
        self._dialogue_filter()
        note=('Some screenshot-verified Japanese glyphs display as Unicode; unknown IDs remain <token:N>. '
              'Japanese font widths and automatic wrapping are still unverified. '
              if region=='japan' else '')
        self.dialogue_status.set(f'{region.upper()}: {len(records)} candidate records indexed from persistent verified ROM. '
                                 f'Retail source: {"stored" if self.dialogue_retail_path else "not yet imported"}. {note}')

    def _dialogue_import_file(self,path):
        if self.dialogue_build_running:
            messagebox.showerror('ROM build running',
                'Do not change source ROMs while a build is in progress.',parent=self.dialogue_tab)
            return
        try:
            region,kind,_=import_rom(path)
        except (OSError,ValueError,RuntimeError) as exc:
            messagebox.showerror('ROM import rejected',str(exc),parent=self.dialogue_tab)
            return
        if self.dialogue_region_choice.get()!=region:
            self.dialogue_region_choice.set(region)
        self._dialogue_region_changed()
        self.dialogue_status.set(
            f'Imported verified {region.upper()} {kind} ROM to persistent app storage; '
            'verified images will reopen automatically. '+self.dialogue_status.get())

    def _dialogue_open(self):
        chosen=filedialog.askopenfilename(title='Import original USA or Japan ROM',
                    filetypes=[('Nintendo 64 ROM','*.z64 *.n64 *.v64'),('All files','*.*')])
        if chosen:self._dialogue_import_file(Path(chosen))

    def _dialogue_open_retail(self):
        # Legacy hidden control still routes to verified persistent import.
        self._dialogue_open()

    def _dialogue_drop(self,event):
        # Root-level TkDND callback: only import when Dialogue tab is selected.
        try:
            if str(self.notebook.select())!=str(self.dialogue_tab):
                return
            file=drop_paths(self.root,event.data)
        except (ValueError,tk.TclError) as exc:
            messagebox.showerror('Invalid dropped ROM',str(exc),parent=self.dialogue_tab)
            return
        self._dialogue_import_file(file)

    def _dialogue_filter(self):
        """Optionally make the table searchable via *unverified* kana guesses."""
        if (not hasattr(self,'dialogue_kana_hypothesis_enabled') or
            not self.dialogue_kana_hypothesis_enabled.get() or
            self.dialogue_region_choice.get()!='japan' or
            not hasattr(self,'dialogue_tree')):
            return super()._dialogue_filter()
        query=self.dialogue_query.get().strip().casefold()
        # Exact resource filters avoid accidentally matching 1112 when the
        # user wants resource 112. An optional second term is also supported.
        resource_filter=None
        resource_match=re.fullmatch(r'resource:(\d+)(?:\s+(.+))?',query)
        if resource_match:
            resource_filter=int(resource_match.group(1))
            query=(resource_match.group(2) or '').strip()
        tree=self.dialogue_tree
        for item in tree.get_children():tree.delete(item)
        filtered=[]
        for record in self.dialogue_records:
            if resource_filter is not None and record.resource_id!=resource_filter:
                continue
            staged=self.dialogue_staged.get(record.key)
            try:
                tokens=encode_japan_text(staged) if staged is not None else record.tokens
                preview=decode_japan_kana_preview(tokens)
            except ValueError:
                tokens=record.tokens
                preview=record.text
            if (not query or query in preview.casefold() or query in record.text.casefold()
                or japanese_query_matches(tokens,query) or
                (resource_filter is None and
                 (query in str(record.resource_id) or query in f'0x{record.text_offset:x}'))):
                filtered.append((record,preview))
        self.dialogue_filtered=[record for record,_ in filtered]
        for record,preview in filtered[:800]:
            tree.insert('','end',iid=record.key,values=(
                record.resource_id,f'0x{record.text_offset:X}',
                len(record.references),preview.replace('\n',' / ')[:200]))
        if self.dialogue_records:
            self.dialogue_status.set(
                f'{len(filtered)} candidate matches (first {min(800,len(filtered))} displayed); '
                f'{len(self.dialogue_staged)} staged. Kana/romaji search includes '
                'HYPOTHETICAL readings; not a verified translation.')

    def _dialogue_show_selected_resource(self):
        key=getattr(self,'dialogue_selected_key',None)
        if key not in self.dialogue_by_key:
            return
        record=self.dialogue_by_key[key]
        self.dialogue_query.set(f'resource:{record.resource_id}')
        self._dialogue_filter()
        if record.key in self.dialogue_tree.get_children():
            self.dialogue_tree.selection_set(record.key)
            self.dialogue_tree.see(record.key)

    def _dialogue_toggle_kana_hypothesis(self):
        self._dialogue_filter()
        self._dialogue_refresh_kana_preview()

    def _dialogue_refresh_kana_preview(self):
        if not hasattr(self,'dialogue_kana_text'):
            return
        key=getattr(self,'dialogue_selected_key',None)
        content=''
        if self.dialogue_region_choice.get()=='japan' and key in self.dialogue_by_key:
            record=self.dialogue_by_key[key]
            try:
                tokens=encode_japan_text(self.dialogue_editor.get('1.0','end-1c'))
                if self.dialogue_kana_hypothesis_enabled.get():
                    content=decode_japan_kana_preview(tokens)
                    self.dialogue_kana_note.set(
                        f'UNVERIFIED gojuon-order guesses: {inferred_kana_count(tokens)} of '
                        f'{sum(t>=0 for t in tokens)} glyph tokens. Screenshot-verified IDs '
                        'remain separate. Copy/compare this preview; do not paste guesses into the editor.')
                else:
                    content='Enable inferred kana to compare this record against your screenshot.'
                    self.dialogue_kana_note.set(
                        'Hypothesis OFF. Basic hiragana 14–59 and katakana 94–139 (+80) '
                        'are not yet validated against gameplay.')
            except ValueError as exc:
                content=f'Preview unavailable: {exc}'
        self.dialogue_kana_text.configure(state='normal')
        self.dialogue_kana_text.delete('1.0','end')
        self.dialogue_kana_text.insert('1.0',content)
        self.dialogue_kana_text.configure(state='disabled')

    def _dialogue_copy_kana_preview(self):
        if not self.dialogue_kana_hypothesis_enabled.get():return
        text=self.dialogue_kana_text.get('1.0','end-1c')
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)

    def _dialogue_select(self,event=None):
        # The original USA window-style analyser is not applicable to JP.
        if self.dialogue_region_choice.get()=='japan':
            original=self.dialogue_original_image
            self.dialogue_original_image=None
            try:return super()._dialogue_select(event)
            finally:
                self.dialogue_original_image=original
                self._dialogue_refresh_kana_preview()
        return super()._dialogue_select(event)

    def _dialogue_analyze(self):
        if self.dialogue_region_choice.get()=='usa':
            return super()._dialogue_analyze()
        key=getattr(self,'dialogue_selected_key',None)
        if not key or key not in self.dialogue_by_key:
            self.dialogue_layout_summary.set('JP glyph atlas and font-width limits are not yet decoded. Select a token record.')
            return
        try:
            tokens=encode_japan_text(self.dialogue_editor.get('1.0','end-1c'))
            controls=tuple(x for x in tokens if x<0)
            self.dialogue_layout_summary.set(
                f'Japan-0 token mode: {sum(x>=0 for x in tokens)} glyph IDs, '
                f'{controls.count(-60)+1} explicit lines, {len(controls)} controls. '
                'Glyph widths and automatic wrapping not yet verified for Japanese script. '
                'Retain original control order; type only verified Unicode or numeric <token:N> IDs.')
        except ValueError as exc:
            self.dialogue_layout_summary.set(f'Japanese token encoding invalid: {exc}')
        self._dialogue_refresh_kana_preview()

    def _dialogue_wrap(self):
        if self.dialogue_region_choice.get()=='japan':
            messagebox.showerror('Japanese wrap not validated',
              'Native Japanese font widths are not mapped; automatic wrapping is disabled.',parent=self.dialogue_tab)
            return
        return super()._dialogue_wrap()

    def _dialogue_stage(self):
        if self.dialogue_region_choice.get()=='usa':
            return super()._dialogue_stage()
        key=self.dialogue_selected_key
        if key not in self.dialogue_by_key:return
        record=self.dialogue_by_key[key]
        replacement=self.dialogue_editor.get('1.0','end-1c')
        try:tokens=validate_japan_replacement(record,replacement)
        except ValueError as exc:
            messagebox.showerror('Invalid Japanese edit',str(exc),parent=self.dialogue_tab)
            return
        if tokens==record.tokens:self.dialogue_staged.pop(key,None)
        else:self.dialogue_staged[key]=replacement
        self._dialogue_filter()
        self._dialogue_analyze()

    def _dialogue_export(self):
        if not self.dialogue_records:return
        if self.dialogue_region_choice.get()=='usa':return super()._dialogue_export()
        path=filedialog.asksaveasfilename(title='Export Japan token index',defaultextension='.json',
                         filetypes=[('JSON index','*.json'),('CSV table','*.csv')])
        if path:
            try:export_japan_index(self.dialogue_records,path)
            except (OSError,ValueError) as exc:
                messagebox.showerror('Export failed',str(exc),parent=self.dialogue_tab)
                return
            self.dialogue_status.set(f'Exported Japanese token index: {path}')

    def _dialogue_output_path(self,retail):
        region=self.dialogue_region_choice.get()
        return filedialog.asksaveasfilename(
            title=f'Build {region.upper()} {"16 MiB retail" if retail else "32 MiB decompressed"} .z64',
            defaultextension='.z64',filetypes=[('Nintendo 64 ROM','*.z64')],
            initialdir=str(build_directory()),
            initialfile=(f'goemon-{region}-dialogue-hack.z64' if retail else
                         f'goemon-{region}-dialogue-hack.decompressed.z64'))

    def _dialogue_build(self):
        if self.dialogue_path is None or not self.dialogue_staged:
            messagebox.showinfo('Nothing to build','Load and stage a dialogue edit first.',parent=self.dialogue_tab)
            return
        path=self._dialogue_output_path(False)
        if not path:return
        try:
            if self.dialogue_region_choice.get()=='japan':
                digest=save_japan_patched(self.dialogue_path,path,self.dialogue_records,self.dialogue_staged)
            else:
                digest=save_patched_image(self.dialogue_path,path,self.dialogue_records,self.dialogue_staged,
                        allow_line_breaks_for=frozenset(self.dialogue_line_break_approved))
        except (OSError,ValueError) as exc:
            messagebox.showerror('ROM build rejected',str(exc),parent=self.dialogue_tab)
            return
        self.dialogue_last_build_dir=Path(path).parent
        self.dialogue_status.set(f'Built decompressed ROM: {path} SHA-1 {digest}; test in emulator.')

    def _dialogue_build_retail(self):
        if self.dialogue_build_running:return
        if self.dialogue_path is None or not self.dialogue_staged:
            messagebox.showinfo('Nothing to build','Load and stage a dialogue edit first.',parent=self.dialogue_tab)
            return
        if self.dialogue_retail_path is None:
            messagebox.showinfo('Retail input missing','Import the original 16 MiB retail ROM for this region.',parent=self.dialogue_tab)
            return
        path=self._dialogue_output_path(True)
        if not path:return
        self.dialogue_build_region=self.dialogue_region_choice.get()
        self.dialogue_pending_build_dir=Path(path).parent
        self.dialogue_build_running=True
        self.dialogue_region_box.state(['disabled'])
        self.dialogue_retail_build_button.state(['disabled'])
        self.dialogue_status.set(f'Building {self.dialogue_build_region.upper()} retail ROM...')
        self.root.after(100,self._dialogue_poll_retail_build)
        threading.Thread(target=self._dialogue_retail_worker,
                         args=(self.dialogue_path,self.dialogue_retail_path,Path(path),
                               list(self.dialogue_records),dict(self.dialogue_staged),
                               frozenset(self.dialogue_line_break_approved)),daemon=True).start()

    def _dialogue_retail_worker(self,source,retail,destination,records,staged,allowed_breaks=frozenset()):
        try:
            if self.dialogue_build_region=='japan':
                digest=save_japan_retail_rom(source,retail,destination,records,staged)
            else:
                digest=save_retail_rom(source,retail,destination,records,staged,
                                        allow_line_breaks_for=allowed_breaks)
            self.dialogue_build_queue.put((True,str(destination),digest))
        except Exception as exc:
            self.dialogue_build_queue.put((False,str(exc),''))

    def _dialogue_poll_retail_build(self):
        if not self.dialogue_build_running:return
        try:success,detail,digest=self.dialogue_build_queue.get_nowait()
        except queue.Empty:
            self.root.after(100,self._dialogue_poll_retail_build)
            return
        self.dialogue_build_running=False
        self.dialogue_region_box.state(['!disabled','readonly'])
        self.dialogue_retail_build_button.state(['!disabled'])
        if success:
            self.dialogue_last_build_dir=self.dialogue_pending_build_dir
            self.dialogue_status.set(f'Built {self.dialogue_build_region.upper()} retail .z64: {detail} SHA-1 {digest}. Test in emulator.')
        else:
            self.dialogue_status.set('Retail ROM build failed; inputs remain unmodified.')
            messagebox.showerror('Build failed',detail,parent=self.dialogue_tab)

    def _dialogue_open_built_dir(self):
        try:open_directory(self.dialogue_last_build_dir or build_directory())
        except OSError as exc:messagebox.showerror('Could not open folder',str(exc),parent=self.dialogue_tab)

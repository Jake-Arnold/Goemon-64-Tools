"""ROM-free debugger regression: canonical guest bytes and honest CPU limits."""
import unittest

from practice.pj64_debugger import (DebuggerSession, disassembly, guest_address,
                                    hex_bytes, memory_rows, mips_instruction, search_guest)


class FakeRAM:
    def __init__(self, size=0x800000):
        self.data=bytearray(size)
        self.writes=0
    def read_guest(self, addr, length):
        off=addr & 0x1FFFFFFF
        return bytes(self.data[off:off+length])
    def write_guest(self, addr, data):
        off=addr & 0x1FFFFFFF
        self.data[off:off+len(data)]=data
        self.writes += 1


class DebuggerTests(unittest.TestCase):
    def test_address_validation_and_kseg_alias(self):
        self.assertEqual(guest_address('0x80001234',4),0x80001234)
        self.assertEqual(guest_address('A0001234',1),0xA0001234)
        for addr in ('0x00001234','0x80800000','0xA0800000','0xBFC00000','garbage'):
            with self.subTest(addr=addr), self.assertRaises(ValueError):guest_address(addr)
        with self.assertRaises(ValueError):guest_address(0x807FFFFF,2)
        with self.assertRaises(ValueError):guest_address(0x80001002,4,alignment=4)
        with self.assertRaises(ValueError):guest_address(True)

    def test_byte_parser_and_rejection(self):
        self.assertEqual(hex_bytes('0x12 34 AB'),b'\x12\x34\xAB')
        for value in ('F','0x','12 G0','ZZ',''):
            with self.subTest(value=value),self.assertRaises(ValueError):hex_bytes(value)

    def test_page_big_endian_and_ascii(self):
        ram=FakeRAM()
        ram.write_guest(0x80001000,b'Goemon!\x00'+bytes(range(8)))
        row=memory_rows(ram,0x80001006,1)[0]
        self.assertEqual(row[0],0x80001000)
        self.assertEqual(row[1].split()[:4],['47','6F','65','6D'])
        self.assertEqual(row[2],'Goemon!..' + ''.join('.' for _ in range(7)))
        self.assertEqual(memory_rows(ram,0x807FFFFF,1)[0][0],0x807FFFF0)

    def test_disassembly_branches_jump_and_fallback(self):
        self.assertEqual(mips_instruction(0x80001000,0),'nop')
        self.assertEqual(mips_instruction(0x80001000,0x2408000D),'addiu $t0, $zero, 13')
        self.assertEqual(mips_instruction(0x80001000,0x1100FFFE),'beq $t0, $zero, 0x80000FFC')
        self.assertEqual(mips_instruction(0x80001000,0x08000400),'j 0x80001000')
        self.assertEqual(mips_instruction(0x80001000,0x00000008),'jr $zero')
        self.assertEqual(mips_instruction(0x80001000,0x70000000),'.word 0x70000000')
        ram=FakeRAM();ram.write_guest(0x80001000,b'\x24\x08\x00\x0D\x00\x00\x00\x00')
        rows=disassembly(ram,0x80001000,2)
        self.assertEqual(rows[0],(0x80001000,'2408000D','addiu $t0, $zero, 13'))
        self.assertEqual(rows[1][2],'nop')
        with self.assertRaises(ValueError):disassembly(ram,0x80001001)

    def test_overlapping_scan_and_chunk_crossing(self):
        ram=FakeRAM()
        ram.write_guest(0x80001006,b'ABABA')
        self.assertEqual(search_guest(ram,b'ABA',0x80001000,16,chunk_size=4),[0x80001006,0x80001008])
        self.assertEqual(search_guest(ram,b'ABA',0x80001007,8,chunk_size=4),[0x80001008])
        self.assertEqual(search_guest(ram,b'ABA',0x80001000,16,limit=1,chunk_size=4),[0x80001006])

    def test_poll_change_events_no_write_and_reconnect_reset(self):
        ram=FakeRAM();ram.write_guest(0x80002000,b'\x00\x01\x02\x03')
        s=DebuggerSession();s.attach(ram);s.add_watch(0x80002000,4)
        self.assertEqual(s.poll(),[])
        ram.write_guest(0x80002000,b'\x00\x01\x02\x04')
        events=s.poll()
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].export()['address'],'0x80002000')
        self.assertEqual(events[0].before,'00010203')
        self.assertEqual(events[0].after,'00010204')
        self.assertEqual(s.poll(),[])
        s.attach(FakeRAM());self.assertEqual(s.events,[]);self.assertEqual(s.watches,{})

    def test_raw_write_is_fail_closed(self):
        ram=FakeRAM();s=DebuggerSession();s.attach(ram)
        with self.assertRaises(PermissionError):s.write(0x80003000,b'\x00',b'\x01',writable=False)
        self.assertEqual(ram.writes,0)
        with self.assertRaises(RuntimeError):s.write(0x80003000,b'\xFF',b'\x01',writable=True)
        self.assertEqual(ram.writes,0)
        with self.assertRaises(ValueError):s.write(0x80003000,b'\x00',b'\x01\x02\x03',writable=True)
        self.assertTrue(s.write(0x80003000,b'\x00',b'\x01',writable=True))
        self.assertEqual(ram.read_guest(0x80003000,1),b'\x01')
        self.assertFalse(s.write(0x80003000,b'\x01',b'\x01',writable=True))
        self.assertEqual(ram.writes,1)

    def test_watch_limit(self):
        ram=FakeRAM();s=DebuggerSession();s.attach(ram)
        for n in range(64):s.add_watch(0x80010000+n,1)
        with self.assertRaises(ValueError):s.add_watch(0x80020000,1)
        s.remove_watch(0x80010000);s.add_watch(0x80020000,1)


if __name__=='__main__':unittest.main()

class DebuggerUiSmokeTests(unittest.TestCase):
    def test_frame_page_read_only_and_script_export(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from unittest.mock import patch
        from practice.pj64_debugger_ui import PJ64DebuggerMixin
        try: root = tk.Tk()
        except tk.TclError as exc: self.skipTest(str(exc))
        try:
            class Stub(PJ64DebuggerMixin): pass
            app = Stub(); app.root = root; app.args = Namespace(read_only=True, enable_hex_edit=False)
            app.notebook = ttk.Notebook(root)
            app.build_pj64_debugger_tab(app.notebook)
            self.assertEqual(app.notebook.tab(app.frame_inspector_tab, 'text'), 'Frame Inspector')
            self.assertIn('Project64', [app.frame_backend_pages.tab(t, 'text') for t in app.frame_backend_pages.tabs()])
            self.assertIn('Frame control (PJ64)', [app.debug_pages.tab(t, 'text') for t in app.debug_pages.tabs()])
            self.assertEqual(app.frame_backend_pages.tab(app.frame_native_page, 'state'), 'disabled')
            self.assertIsNone(app._ensure_native_frame_ui())
            self.assertTrue(all('disabled' in b.state() for b in app.frame_controls))
            with patch('practice.pj64_frame_ui.request') as request, patch('practice.pj64_frame_ui.filedialog.asksaveasfilename') as dialog:
                app._frame_request('pause'); app._frame_export()
                request.assert_not_called(); dialog.assert_not_called()
            self.assertIn('read-only', app.frame_status.get())
            # Existing shutdown cancels root-owned callbacks before destroying widgets.
            for callback in root.tk.call('after', 'info'):
                root.after_cancel(callback)
        finally: root.destroy()

    def test_frame_inspector_trace_and_comparison(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from unittest.mock import patch
        from practice.pj64_frame_ui import PJ64FrameUiMixin
        try: root=tk.Tk()
        except tk.TclError as exc:self.skipTest(str(exc))
        try:
            class Stub(PJ64FrameUiMixin):pass
            app=Stub();app.root=root;app.args=Namespace(read_only=False)
            app._build_pj64_frame_page(ttk.Notebook(root))
            def row(step,phase,word):return dict(step=step,phase=phase,input=None,polls=1,words=[word])
            status=dict(region='usa',mode='execution-hook',pc=0x80001000,watches=[dict(name='action',kind='u16',address=0x80002000)],trap=None,hit=None,error='',epoch=1,generation=1,batchGeneration=1,pending=False,ready=True,valid=True,count=0,polls=0,trace=[])
            app.frame_last=status
            app._frame_toggle_record();self.assertTrue(app.frame_recording)
            end=dict(status,generation=2,batchGeneration=2,count=1,trace=[row(0,'baseline',0x000D0000),row(1,'update',0x008F0000)])
            app.frame_results.put((end,None));app._frame_drain()
            self.assertEqual(len(app.frame_capture['trace']),2)
            items=app.frame_table.get_children();self.assertEqual(len(items),2)
            self.assertIn('changed',app.frame_table.item(items[1],'tags'))
            app.frame_reference=dict(end,trace=[row(0,'baseline',0x000D0000),row(1,'update',0x00000000)])
            app._frame_render_trace(app.frame_capture)
            items=app.frame_table.get_children();self.assertIn('different',app.frame_table.item(items[1],'tags'))
            self.assertIn('first difference at relative row 1',app.frame_comparison.get())
            app._frame_stop_record();self.assertFalse(app.frame_recording)
            for callback in root.tk.call('after','info'):root.after_cancel(callback)
        finally:root.destroy()

    def test_tab_uses_existing_rdram_and_clears_stale_session(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from practice.pj64_debugger_ui import PJ64DebuggerMixin
        try:root=tk.Tk()
        except tk.TclError as exc:self.skipTest(f'No graphical display: {exc}')
        try:
            class Stub(PJ64DebuggerMixin):pass
            app=Stub();app.root=root;app.args=Namespace(enable_hex_edit=False)
            app.mem=FakeRAM();app.jp_rdram=None;app.game_pid=123
            app.active_version=type('Version',(),{'key':'usa'})()
            app.notebook=ttk.Notebook(root);app.notebook.pack()
            app.build_pj64_debugger_tab(app.notebook)
            self.assertEqual(app.notebook.tab(app.pj64_debugger_tab,'text'),'Debugger')
            app.debug_refresh_memory()
            self.assertEqual(len(app.debug_memory_tree.get_children()),16)
            app.debug_code_addr.set('0x80000000');app.debug_refresh_disasm()
            self.assertEqual(len(app.debug_disasm_tree.get_children()),64)
            app.debug_watch_addr.set('0x80000100');app.debug_add_watch()
            self.assertEqual(len(app.debug_session.watches),1)
            self.assertIn('disabled',app.debug_write_button.state())
            app.mem=FakeRAM();app.poll_pj64_debugger(5.0)
            self.assertEqual(len(app.debug_session.watches),0)
            self.assertEqual(app.debug_original.get(),'—')
        finally:root.destroy()


class MainlineRegionRegressionTests(unittest.TestCase):
    def test_japan_reader_is_used_not_stale_usa_memory(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from practice.pj64_debugger_ui import PJ64DebuggerMixin
        try: root=tk.Tk()
        except tk.TclError as exc:self.skipTest('No graphical display: '+str(exc))
        try:
            class App(PJ64DebuggerMixin):pass
            app=App();app.root=root;app.args=Namespace(enable_hex_edit=False)
            app.active_version=type('Version',(),{'key':'japan'})()
            app.mem=FakeRAM();app.jp_rdram=FakeRAM();app.game_pid=999
            app.mem.write_guest(0x80000000,b'USA!')
            app.jp_rdram.write_guest(0x80000000,b'JP!!')
            app.notebook=ttk.Notebook(root);app.notebook.pack()
            app.build_pj64_debugger_tab(app.notebook)
            app.debug_refresh_memory()
            first=app.debug_memory_tree.item('80000000')['values'][0]
            self.assertIn('4A 50 21 21',first)
            self.assertNotIn('55 53 41 21',first)
            app.debug_watch_addr.set('0x80000100');app.debug_add_watch()
            self.assertEqual(len(app.debug_session.watches),1)
            # Changing region while retaining PID must invalidate old watches.
            app.active_version.key='usa'
            app.poll_pj64_debugger(99.0)
            self.assertEqual(len(app.debug_session.watches),0)
            self.assertIs(app.debug_session.ram,app.mem)
        finally:root.destroy()

    def test_pid_change_resets_debug_session_even_same_memory_reader(self):
        import tkinter as tk
        from tkinter import ttk
        from argparse import Namespace
        from practice.pj64_debugger_ui import PJ64DebuggerMixin
        try:root=tk.Tk()
        except tk.TclError as exc:self.skipTest('No graphical display: '+str(exc))
        try:
            class App(PJ64DebuggerMixin):pass
            app=App();app.root=root;app.args=Namespace(enable_hex_edit=False)
            app.active_version=type('Version',(),{'key':'usa'})()
            app.mem=FakeRAM();app.jp_rdram=None;app.game_pid=9
            app.notebook=ttk.Notebook(root);app.notebook.pack()
            app.build_pj64_debugger_tab(app.notebook)
            app.debug_add_watch()
            self.assertEqual(len(app.debug_session.watches),1)
            app.game_pid=10
            app.poll_pj64_debugger(98.0)
            self.assertEqual(app.debug_session.watches,{})
        finally:root.destroy()

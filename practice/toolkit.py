"""Goemon Practice Toolkit v0.9.9 — external Windows UI for US Goemon64Recomp.

Observes original-game RDRAM state and manages position bookmarks, route
calibration, and experimental logical progression checkpoints. Memory writes
require --enable-teleport or --enable-state-restore. This is not a savestate
and is not an in-game N64 ROM patch.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import time
import tkinter as tk
import platform
import ctypes
from tkinter import ttk, messagebox
import sys

from autosplitter.bridge import find_pid
from autosplitter.memory import WindowsProcess, Rdram, discover_rdram
from autosplitter.engine import load_route, save_route
from practice.checkpoints import (capture_checkpoint, restore_checkpoint,
                                  load_checkpoint_file, save_checkpoint_file)
from practice.ui_extension import InspectorMixin
from practice.paths import resource_root, practice_data_dir
from practice.native_character import (
    prepare_character_swap, undo_character_preparation,
    ready_after_native_swap, press_native_c_down, IDLE_ACTIONS,
)

ROOT = resource_root()
BOOKMARKS_FILE = practice_data_dir() / "bookmarks.json"
CHECKPOINTS_FILE = practice_data_dir() / "checkpoints.json"


ASSETS_DIR = ROOT / "assets"
APP_ICON_ICO = ASSETS_DIR / "goemon_tools_logo.ico"
APP_ICON_PNG = ASSETS_DIR / "goemon_tools_logo.png"


def configure_window_branding(root: tk.Tk) -> None:
    """Apply a real app identity/icon when available.

    On Windows this improves the taskbar entry so the toolkit shows its own
    icon rather than a generic Python one when launched from the source tree.
    The helper is best-effort and silently falls back if the assets or Win32
    APIs are unavailable.
    """
    try:
        if platform.system() == "Windows":
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "JakeArnold.GoemonSpeedrunTools"
                )
            except Exception:
                pass
            if APP_ICON_ICO.exists():
                try:
                    root.iconbitmap(default=str(APP_ICON_ICO))
                    return
                except Exception:
                    pass
        if APP_ICON_PNG.exists():
            try:
                icon_image = tk.PhotoImage(file=str(APP_ICON_PNG))
                root._goemon_icon_image = icon_image
                root.iconphoto(True, icon_image)
            except Exception:
                pass
    except Exception:
        pass


class Toolkit(InspectorMixin):
    def __init__(self, root, args):
        self.root, self.args = root, args
        root.title("Goemon Practice Toolkit v0.9.9 · USA Recomp")
        root.geometry("1180x770")
        configure_window_branding(root)
        root.attributes("-topmost", True)
        self.mem, self.process = None, None
        self.game_pid = None
        self.pending_restore = None
        self.native_key_release = None
        self.last, self.last_t = None, None
        self.current = None
        self.route_path = Path(args.route) if args.route else None
        self.route = load_route(str(self.route_path)) if self.route_path and self.route_path.exists() else None
        self.bookmarks = json.loads(BOOKMARKS_FILE.read_text()) if BOOKMARKS_FILE.exists() else []
        self.checkpoints = load_checkpoint_file(CHECKPOINTS_FILE)
        self.status = tk.StringVar(value="Disconnected. Start US Goemon64Recomp, then Connect.")
        self.pos_text = tk.StringVar(value="X: —    Y: —    Z: —")
        self.speed_text = tk.StringVar(value="Speed: —")
        self.misc_text = tk.StringVar(value="Character: —   Action: —   Loading: —")
        notebook=ttk.Notebook(root)
        notebook.pack(fill="both",expand=True)
        frm = ttk.Frame(notebook,padding=12)
        notebook.add(frm,text="Practice / checkpoints")
        ttk.Label(frm,textvariable=self.status,wraplength=635).pack(anchor="w")
        ttk.Button(frm,text="Connect to Goemon64Recomp",command=self.connect).pack(fill="x",pady=8)
        ttk.Label(frm,textvariable=self.pos_text,font=("Consolas",14)).pack(anchor="w")
        ttk.Label(frm,textvariable=self.speed_text,font=("Consolas",12)).pack(anchor="w")
        ttk.Label(frm,textvariable=self.misc_text,font=("Consolas",10)).pack(anchor="w",pady=(0,8))
        ttk.Separator(frm).pack(fill="x",pady=7)
        ttk.Label(frm,text="Position bookmarks (practice only)").pack(anchor="w")
        self.bookmarks_box = ttk.Combobox(frm,state="readonly",values=self.bookmark_labels())
        self.bookmarks_box.pack(fill="x",pady=3)
        self.bookmark_name = ttk.Entry(frm)
        self.bookmark_name.insert(0,"Practice checkpoint")
        self.bookmark_name.pack(fill="x",pady=3)
        row = ttk.Frame(frm)
        row.pack(fill="x",pady=4)
        ttk.Button(row,text="Save position bookmark",command=self.save_bookmark).pack(side="left",expand=True,fill="x")
        self.teleport_btn=ttk.Button(row,text="Restore position (unsafe)",command=self.restore_bookmark)
        self.teleport_btn.pack(side="left",expand=True,fill="x",padx=6)
        if not args.enable_teleport: self.teleport_btn.state(["disabled"])
        ttk.Separator(frm).pack(fill="x",pady=6)
        ttk.Label(frm,text="Logical checkpoints: N64 game flags + resources + position (EXPERIMENTAL)").pack(anchor="w")
        self.checkpoints_box = ttk.Combobox(frm,state="readonly",values=self.checkpoint_labels())
        self.checkpoints_box.pack(fill="x",pady=3)
        state_buttons = ttk.Frame(frm)
        state_buttons.pack(fill="x",pady=4)
        ttk.Button(state_buttons,text="Capture logical checkpoint",command=self.capture_full_checkpoint).pack(side="left",expand=True,fill="x")
        self.restore_state_btn = ttk.Button(state_buttons,text="Restore logical checkpoint (experimental)",command=self.restore_full_checkpoint)
        self.restore_state_btn.pack(side="left",expand=True,fill="x",padx=6)
        if not args.enable_state_restore: self.restore_state_btn.state(["disabled"])
        self.cancel_restore_btn=ttk.Button(frm,text="Cancel pending native-character restore",command=self.cancel_pending_restore)
        self.cancel_restore_btn.pack(fill="x",pady=(0,3))
        self.cancel_restore_btn.state(["disabled"])
        ttk.Separator(frm).pack(fill="x",pady=6)
        ttk.Label(frm,text="Calibrate the NEXT route segment (enter from outside checkpoint radius)").pack(anchor="w")
        row = ttk.Frame(frm)
        row.pack(fill="x",pady=5)
        self.segment_index = tk.IntVar(value=1)
        self.radius = tk.StringVar(value="45")
        ttk.Label(row,text="Segment #").pack(side="left")
        ttk.Entry(row,textvariable=self.segment_index,width=5).pack(side="left",padx=5)
        ttk.Label(row,text="Radius").pack(side="left",padx=4)
        ttk.Entry(row,textvariable=self.radius,width=8).pack(side="left",padx=4)
        ttk.Button(row,text="Capture split trigger here",command=self.capture_trigger).pack(side="left",padx=6)
        ttk.Label(frm,text="All experimental functions are on when launched via Run.bat. Use disposable saves; never use these tools in competitive runs.",wraplength=640).pack(anchor="w",pady=8)
        self.build_inspector_tabs(notebook)
        root.after(100,self.tick)

    def bookmark_labels(self):
        return [f"{i+1}. {x['name']} ({x['x']:.1f}, {x['y']:.1f}, {x['z']:.1f})" for i,x in enumerate(self.bookmarks)]

    def connect(self):
        self.cancel_pending_restore(quiet=True)
        self.pending_direct_warp=None
        try:
            if self.process: self.process.close()
            pid = self.args.pid or find_pid()
            self.process=WindowsProcess(pid, writable=(self.args.enable_teleport or self.args.enable_state_restore or self.args.enable_debug_menu or self.args.enable_scene_warp or self.args.enable_hex_edit))
            if self.args.base:
                base, endian = int(self.args.base, 0), ("wordswapped" if self.args.endian == "auto" else self.args.endian)
            else:
                base, endian = discover_rdram(self.process, self.args.endian)
            candidate=Rdram(self.process,base,endian)
            sample=candidate.snapshot()
            if sample["x"] is None or sample["action"] is None:
                raise ValueError("Player not loaded; enter gameplay and reconnect")
            self.mem=candidate
            self.game_pid=pid
            self.status.set(f"Validated PID {pid}, RAM 0x{base:X}, format {endian}. Move to verify updates.")
            self.current=sample
        except Exception as e:
            self.game_pid=None
            self.mem=None
            self.current=None
            self.last=None
            self.last_t=None
            self.pos_text.set("X: —    Y: —    Z: —")
            self.speed_text.set("Speed: —")
            self.misc_text.set("Character: —    Action: —    Loading: —")
            if self.process:
                self.process.close()
                self.process=None
            self.status.set(f"Connection failed: {e}")

    def tick(self):
        if self.mem:
            try:
                now=time.monotonic()
                # During the ORIGINAL debug menu the player objects may not exist.
                # Do not disconnect the inspector just because snapshot() cannot
                # read an active player. The menu itself must remain inspectable.
                state=self.mem.u8(0x800C7A94)
                self.refresh_native_watch(now)
                self.poll_direct_warp(now)
                if state==10 or (self.pending_native_warp and state!=13):
                    self.refresh_inspector({})
                    self.poll_native_warp_menu(now)
                    self.root.after(170,self.tick)
                    return
                self.poll_native_warp_menu(now)
                s=self.mem.snapshot()
                now=time.monotonic()
                if s["x"] is not None:
                    self.pos_text.set(f"X: {s['x']:10.2f}    Y: {s['y']:10.2f}    Z: {s['z']:10.2f}")
                    if self.last is not None and self.last_t is not None and s["player_ptr"]==self.last["player_ptr"]:
                        dt=now-self.last_t
                        if dt>0:
                            v=math.sqrt(sum((s[a]-self.last[a])**2 for a in ("x","y","z")))/dt
                            self.speed_text.set(f"Observed displacement: {v:9.2f} units/s (not internal velocity)")
                    self.last, self.last_t=s,now
                self.misc_text.set(f"Character: {s['character']}    Action: {s['action']}    Loading: {s['loading']}")
                self.current=s
                self.refresh_inspector(s)
                self.refresh_checkpoint_diff()
                self.poll_pending_restore(s, now)
            except (OSError,ValueError) as e:
                self.status.set(f"Memory read failed: {e}")
                self.cancel_pending_restore(quiet=True)
                self.mem=None
        self.root.after(170,self.tick)

    def save_bookmark(self):
        s=self.current
        if not s or s["x"] is None:
            messagebox.showerror("Not connected","Read a valid player position first")
            return
        entry={"name":self.bookmark_name.get() or "Checkpoint",
               "x":s["x"],"y":s["y"],"z":s["z"],"character":s["character"],
               "action":s["action"],
               "map_id":self.mem.u16(0x800C7AB2) if self.mem else None}
        self.bookmarks.append(entry)
        BOOKMARKS_FILE.write_text(json.dumps(self.bookmarks,indent=2)+"\n")
        self.bookmarks_box["values"]=self.bookmark_labels()
        self.bookmarks_box.current(len(self.bookmarks)-1)
        self.status.set(f"Saved bookmark: {entry['name']}")

    def restore_bookmark(self):
        idx=self.bookmarks_box.current()
        if not self.args.enable_teleport or idx<0 or not self.mem or not self.current:
            return
        b=self.bookmarks[idx]
        if self.current["loading"] or self.current["x"] is None:
            messagebox.showerror("Blocked","Restore only in stable gameplay")
            return
        if self.current["character"]!=b["character"]:
            messagebox.showerror("Blocked","Bookmark character doesn't match the active character")
            return
        if b.get("map_id") is None:
            messagebox.showerror("Blocked","Legacy bookmark has no recorded map ID. Recapture this bookmark in v0.4 before restoring.")
            return
        if self.mem.u16(0x800C7AB2)!=b["map_id"]:
            messagebox.showerror("Blocked","Bookmark map differs. Use the original debug menu to reach that map first.")
            return
        if not messagebox.askyesno("Unsafe practice teleport",
                "This writes N64 object coordinates and can softlock, crash, or corrupt game state. "
                "It does not restore the full scene or physics state. Use only within the same room. Continue?"):
            return
        try:
            obj=self.current["player_ptr"]
            if not obj: raise ValueError("No player object")
            for i,k in enumerate(("x","y","z")):
                self.mem.write_f32(obj+8+i*4,float(b[k]))
            self.status.set(f"Moved to saved coordinates: {b['name']} (practice mode only)")
        except Exception as e:
            messagebox.showerror("Teleport failed",str(e))

    def checkpoint_labels(self):
        labels=[]
        for i, cp in enumerate(self.checkpoints):
            p=cp["payload"]
            stats=p["summary"]
            labels.append(f"{i+1}. {p['name']} (map {p['map_id']}, {stats['health']}/{stats['max_health']} HP, {stats['ryo']} Ryo, {stats['lives']} lives)")
        return labels

    def capture_full_checkpoint(self):
        if not self.mem or not self.current:
            messagebox.showerror("Not connected","Connect to Goemon64Recomp first")
            return
        try:
            cp=capture_checkpoint(self.mem,self.bookmark_name.get())
            self.checkpoints.append(cp)
            save_checkpoint_file(CHECKPOINTS_FILE,self.checkpoints)
            self.checkpoints_box["values"]=self.checkpoint_labels()
            self.checkpoints_box.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_options()
            self.diff_cp.current(len(self.checkpoints)-1)
            self.refresh_checkpoint_diff(force=True)
            self.status.set("Captured original N64 progress flags, stats, unlocks and position. Experimental in-room restore available.")
        except Exception as e:
            messagebox.showerror("Checkpoint capture blocked",str(e))

    def _restore_now(self, checkpoint):
        """Original logical restore; the game has already finished any native swap."""
        summary=restore_checkpoint(self.mem,checkpoint)
        self.last=None
        self.last_t=None
        p=checkpoint['payload']
        self.status.set(f"Restored logical checkpoint: {p['name']} | "
                        f"{summary['health']}/{summary['max_health']} HP, "
                        f"{summary['ryo']} Ryo, {summary['lives']} lives. Verify in-game.")
        self.refresh_checkpoint_diff(force=True)

    def _release_native_key(self):
        release=self.native_key_release
        self.native_key_release=None
        if release is not None:
            try:release()
            except Exception:pass

    def cancel_pending_restore(self, quiet=False):
        pending=self.pending_restore
        self.pending_restore=None
        self._release_native_key()
        if getattr(self,'cancel_restore_btn',None):self.cancel_restore_btn.state(['disabled'])
        if getattr(self,'restore_state_btn',None) and self.args.enable_state_restore:
            self.restore_state_btn.state(['!disabled'])
        if pending and self.mem:
            try:
                note=undo_character_preparation(self.mem,pending.get('party_patch'),
                                                pending['checkpoint']['payload']['character'])
                if not quiet:self.status.set('Checkpoint restore cancelled; '+note)
            except (OSError,ValueError) as exc:
                if not quiet:self.status.set(f'Cancelled; temporary party state could not be reverted: {exc}')
        elif pending and not quiet:
            self.status.set('Checkpoint restore cancelled')

    def _request_native_character_swap(self, pending, now):
        # Optional host adapter for the *original game's* C-Down switch. Never
        # modify the global/per-task character ID or bypass its model loader.
        pending['last_press']=now
        pending['attempts']+=1
        try:
            self.native_key_release=press_native_c_down(self.game_pid)
            self.root.after(180,self._release_native_key)
            self.status.set(f"Native C-Down sent ({pending['attempts']}/4); "
                            f"waiting for game to rebuild character {pending['target']}.")
        except (OSError,RuntimeError) as exc:
            pending['manual_only']=True
            self.status.set(f"Automatic C-Down unavailable: {exc}. "
                            f"Switch to character {pending['target']} in-game; restore will finish automatically.")

    def poll_pending_restore(self, snapshot, now=None):
        """Don't restore into an old avatar while the engine loads another."""
        pending=self.pending_restore
        if not pending or not self.mem:return
        if now is None:now=time.monotonic()
        if now-pending['started']>45:
            self.cancel_pending_restore()
            self.status.set('Character swap timed out after 45 seconds; checkpoint not restored.')
            return
        try:
            p=pending['checkpoint']['payload']
            if self.mem.u16(0x800C7AB2)!=p['map_id']:
                self.cancel_pending_restore()
                self.status.set('Map changed during character swap. Restore cancelled to avoid writing into wrong scene.')
                return
            if snapshot['character']==pending['target']:
                if ready_after_native_swap(self.mem,pending['checkpoint']):
                    pending['stable']+=1
                    if pending['stable']>=3:
                        # Never retry a partially failed multi-region write at
                        # 6Hz. An error is terminal for this restore attempt.
                        try:
                            self._restore_now(pending['checkpoint'])
                        except Exception as exc:
                            self.cancel_pending_restore(quiet=True)
                            self.status.set(f'Native swap completed, but checkpoint write failed: {exc}')
                            messagebox.showerror('Logical restore failed',str(exc))
                            return
                        self.pending_restore=None
                        self.cancel_restore_btn.state(['disabled'])
                        self.restore_state_btn.state(['!disabled'])
                        return
                else:
                    pending['stable']=0
                    self.status.set(f"Character {pending['target']} selected; "
                                    'waiting for native model/texture swap to finish.')
                return
            pending['stable']=0
            if snapshot['action'] not in IDLE_ACTIONS or snapshot['loading']:
                self.status.set('Waiting for character-swap animation / ordinary gameplay to finish.')
                return
            # Once idle again, pulse C-Down if needed to cycle party. No more
            # than four attempts; if keyboard bindings differ, manual switching
            # remains available and is observed automatically.
            if (not pending['manual_only'] and pending['attempts']<4 and
                    now-pending['last_press']>=2.0 and self.native_key_release is None):
                self._request_native_character_swap(pending,now)
            elif pending['attempts']>=4:
                pending['manual_only']=True
                self.status.set('Could not reach saved character automatically. '
                                f"Switch to character {pending['target']} in-game; restore is armed.")
        except (OSError,ValueError) as exc:
            # A brief gameplay gate failure during native swap is normal.
            # Never force a restore during that window.
            pending['stable']=0
            self.status.set(f'Waiting for safe native character state: {exc}')

    def restore_full_checkpoint(self):
        i=self.checkpoints_box.current()
        if not self.args.enable_state_restore or i<0 or not self.mem or not self.current:return
        if self.pending_restore:
            self.status.set('A checkpoint restore is already pending; cancel it first.')
            return
        cp=self.checkpoints[i]
        p=cp['payload']
        if not messagebox.askyesno('EXPERIMENTAL logical restore (practice only)',
             'Restore game flags/inventory, resources, character, and position?\n\n'
             'If the saved character differs, the toolkit will try the original game C-Down switch '
             '(default keyboard mapping) and wait for the model reload; you can also switch manually.\n\n'
             'Only the SAME MAP is supported. Actors/scripts/physics are NOT savestates. '
             'A crash or softlock is possible. Never use during competitive runs. Continue?'):
            return
        try:
            from practice.checkpoints import validate_checkpoint, _ensure_capture_safe, MAP_ADDR
            validate_checkpoint(cp)
            before=_ensure_capture_safe(self.mem)
            if self.mem.u16(MAP_ADDR)!=p['map_id']:
                raise ValueError('Checkpoint map differs; select the saved scene first')
            if before['character']==p['character']:
                self._restore_now(cp)
                return
            patch=prepare_character_swap(self.mem,cp)
            self.pending_restore={'checkpoint':cp,'target':p['character'],
                    'party_patch':patch,'started':time.monotonic(),
                    'last_press':0.0,'attempts':0,'stable':0,'manual_only':False}
            self.restore_state_btn.state(['disabled'])
            self.cancel_restore_btn.state(['!disabled'])
            self.status.set(f"Restore armed: saved character {p['character']}, "
                            f"current {before['character']}. Using original-game character switch.")
            self.poll_pending_restore(before)
        except Exception as exc:
            self.cancel_pending_restore(quiet=True)
            messagebox.showerror('Logical restore failed',str(exc))

    def capture_trigger(self):
        if not self.route or not self.route_path:
            messagebox.showerror("No route","Launch with --route route.json after importing an .lss file")
            return
        if not self.current or self.current["x"] is None:
            messagebox.showerror("Not connected","Read a valid position first")
            return
        try:
            index=self.segment_index.get()-1
            radius=float(self.radius.get())
            if not (0<=index<len(self.route["segments"])) or not (0<radius<10000):
                raise ValueError("Invalid segment number or radius")
            s=self.current
            self.route["segments"][index]["trigger"]={"type":"position_enter",
                "x":round(s["x"],3),"y":round(s["y"],3),"z":round(s["z"],3),
                "radius":radius,"character":s["character"]}
            save_route(self.route,str(self.route_path))
            self.status.set(f"Calibrated segment {index+1}: {self.route['segments'][index]['name']}")
            self.segment_index.set(index+2)
        except Exception as e:
            messagebox.showerror("Calibration failed",str(e))


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pid",type=int)
    ap.add_argument("--base",help="RDRAM host base 0x...; bypasses experimental auto-discovery")
    ap.add_argument("--endian",choices=["auto","wordswapped","big"],default="auto")
    ap.add_argument("--route",help="route.json from autosplitter import-splits")
    ap.add_argument("--enable-teleport",action="store_true",help="UNSAFE: opt in to writing game coordinates")
    ap.add_argument("--enable-state-restore",action="store_true",help="EXPERIMENTAL: opt in to writing original-game progress flags and resources")
    ap.add_argument("--enable-debug-menu",action="store_true",help="EXPERIMENTAL: allow entering original game debug menu state 10")
    ap.add_argument("--enable-hex-edit",action="store_true",help="Opt in to confirmed double-click hex edits")
    ap.add_argument("--enable-scene-warp",action="store_true",help="DISABLED: v0.9.7 direct scene writes triggered title screen; never used")
    args=ap.parse_args(argv)
    root=tk.Tk(); app=Toolkit(root,args)
    try:
        root.mainloop()
    finally:
        app.stop_transition_trace()
        app.cancel_pending_restore(quiet=True)
        if getattr(app,'native_key_release',None):app._release_debug_key()
        if app.process: app.process.close()

if __name__=="__main__": main()

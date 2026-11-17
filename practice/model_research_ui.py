"""Explicit-ROM geometry research preview; not a verified actor model or RT64.

Real model rendering remains in Goemon64Recomp/RT64. This window permits a
bounded, read-only preview of vertex-colour geometry from user-chosen F3DEX
resource spans, without treating those spans as a selected actor's model.
"""
from __future__ import annotations

import math
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog

from practice.model_research import extract_rom_probe


class ModelResearchDialog:
    def __init__(self, parent, *, region, stage=None, actor_id=None, actor_name=None):
        if region not in ('usa', 'japan_0'):
            raise ValueError('Unknown ROM region')
        self.region, self.stage, self.actor_id = region, stage, actor_id
        self.rom_path = None
        self.mesh = None
        self.result_queue = queue.SimpleQueue()
        self.loading = False
        self.yaw, self.pitch, self.zoom = 0.68, -0.32, 1.0
        self.drag_origin = None
        self.window = tk.Toplevel(parent)
        self.window.title(f'{region}: F3DEX geometry research (unverified)')
        self.window.geometry('920x720')
        self.window.minsize(640, 450)
        body = ttk.Frame(self.window, padding=10)
        body.pack(fill='both', expand=True)
        if actor_id is None:
            association = 'No actor selected.'
        else:
            association = f'Selected ROM placement: stage {stage}, actor 0x{actor_id:03X} ({actor_name or "unidentified"}).'
        ttk.Label(body, text=association).pack(anchor='w')
        ttk.Label(body, text='NO VERIFIED ACTOR → MODEL MAPPING. File/offset inputs below are manual research only; the geometry shown is not asserted to belong to the selected actor.', wraplength=850).pack(anchor='w', pady=(3, 8))
        toolbar = ttk.Frame(body)
        toolbar.pack(fill='x', pady=(0, 5))
        ttk.Button(toolbar, text='Select local ROM…', command=self.choose_rom).pack(side='left')
        self.rom_note = tk.StringVar(value=f'No {region} ROM selected. No file path is stored.')
        ttk.Label(toolbar, textvariable=self.rom_note).pack(side='left', padx=8)
        inputs = ttk.Frame(body)
        inputs.pack(fill='x', pady=(0, 7))
        ttk.Label(inputs, text='Resource file ID:').pack(side='left')
        self.file_id = tk.StringVar()
        ttk.Entry(inputs, width=8, textvariable=self.file_id).pack(side='left', padx=(4, 12))
        ttk.Label(inputs, text='Start offset:').pack(side='left')
        self.start = tk.StringVar()
        ttk.Entry(inputs, width=12, textvariable=self.start).pack(side='left', padx=(4, 12))
        ttk.Label(inputs, text='End offset:').pack(side='left')
        self.end = tk.StringVar()
        ttk.Entry(inputs, width=12, textvariable=self.end).pack(side='left', padx=(4, 12))
        self.decode_button = ttk.Button(inputs, text='Decode research mesh', command=self.decode)
        self.decode_button.pack(side='left', padx=4)
        ttk.Button(inputs, text='Reset view', command=self.reset_view).pack(side='left')
        self.status = tk.StringVar(value='Select your own ROM and an explicit resource command span. No guessed actor resources are supplied.')
        ttk.Label(body, textvariable=self.status, wraplength=860).pack(anchor='w', pady=(0, 6))
        self.canvas = tk.Canvas(body, background='#171a23', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Configure>', lambda _e: self.render())
        self.canvas.bind('<ButtonPress-1>', self.begin_drag)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<MouseWheel>', self.wheel)
        self.canvas.bind('<Button-4>', lambda _e: self.zoom_by(1.13))
        self.canvas.bind('<Button-5>', lambda _e: self.zoom_by(1/1.13))
        ttk.Label(body, text='Drag to orbit. Mouse wheel to zoom. Geometry is untextured and ignores N64 matrices, animations and RDP materials. RT64 is the reference renderer.', wraplength=860).pack(anchor='w', pady=(6, 0))

    def choose_rom(self):
        name = filedialog.askopenfilename(parent=self.window, title='Choose your verified regional ROM', filetypes=[('N64 ROM', '*.z64 *.n64 *.v64'), ('All files', '*.*')])
        if name:
            self.rom_path = Path(name)
            self.rom_note.set(f'Local ROM selected ({self.region}); path not cached')

    def decode(self):
        if self.loading:
            return
        try:
            if self.rom_path is None:
                raise ValueError('Choose the original ROM first')
            file_id = int(self.file_id.get().strip(), 0)
            start = int(self.start.get().strip(), 0)
            end = int(self.end.get().strip(), 0)
            if not (1 <= file_id <= 1310):
                raise ValueError('File ID must be 1..1310')
        except ValueError as exc:
            self.status.set(f'Research input error: {exc}')
            return
        self.loading = True
        self.decode_button.state(['disabled'])
        self.status.set('Decoding original ROM resource; no guest-memory writes…')
        def work():
            try:
                result = extract_rom_probe(self.rom_path.read_bytes(), self.region, file_id, start, end)
                self.result_queue.put(('ok', result))
            except (OSError, ValueError) as exc:
                self.result_queue.put(('error', str(exc)))
        threading.Thread(target=work, daemon=True).start()
        self.window.after(60, self.poll_result)

    def poll_result(self):
        if not self.window.winfo_exists():
            return
        try:
            kind, result = self.result_queue.get_nowait()
        except queue.Empty:
            self.window.after(60, self.poll_result)
            return
        self.loading = False
        self.decode_button.state(['!disabled'])
        if kind != 'ok':
            self.status.set(f'Resource probe failed: {result}')
            return
        report, self.mesh = result
        self.reset_view()
        self.status.set(f'RESEARCH ONLY — {self.region} file {report["file_id"]}, {report["triangles"]} triangles, {report["commands"]} commands, {len(report["warnings"])} limitations/warnings. Not linked to actor ID.')

    def reset_view(self):
        self.yaw, self.pitch, self.zoom = 0.68, -0.32, 1.0
        self.render()

    def begin_drag(self, event):
        self.drag_origin = (event.x, event.y)

    def drag(self, event):
        if self.drag_origin is None:
            return
        dx, dy = event.x - self.drag_origin[0], event.y - self.drag_origin[1]
        self.drag_origin = (event.x, event.y)
        self.yaw += dx * 0.009
        self.pitch = max(-1.5, min(1.5, self.pitch + dy * 0.009))
        self.render()

    def wheel(self, event):
        self.zoom_by(1.13 if event.delta > 0 else 1/1.13)

    def zoom_by(self, factor):
        self.zoom = max(0.25, min(8.0, self.zoom*factor))
        self.render()

    def render(self):
        self.canvas.delete('all')
        mesh = self.mesh
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if mesh is None or not mesh.triangles or width < 10 or height < 10:
            self.canvas.create_text(max(10,width//2),max(10,height//2), text='No F3DEX geometry loaded', fill='#aeb8c5')
            return
        bounds = mesh.bounds
        center = tuple((a+b)*0.5 for a,b in zip(*bounds))
        extent = max(b-a for a,b in zip(*bounds)) or 1.0
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        scale = min(width, height) * self.zoom * 0.72 / extent
        faces = mesh.triangles
        # Limit Tk canvas load without claiming this is an exhaustive render.
        step = max(1, (len(faces)+3999)//4000)
        order = []
        for i in range(0, len(faces), step):
            triangle = faces[i]
            projected = []
            z_values = []
            for x,y,z in triangle:
                x,y,z = x-center[0], y-center[1], z-center[2]
                rx, rz = x*cy+z*sy, -x*sy+z*cy
                ry, rz = y*cp-rz*sp, y*sp+rz*cp
                # Orthographic visualization; matrices intentionally omitted.
                projected.extend((width*0.5 + rx*scale, height*0.5 - ry*scale))
                z_values.append(rz)
            order.append((sum(z_values)/3, i, projected))
        order.sort(key=lambda item: item[0])
        for _z, index, xy in order:
            rgb = mesh.rgb[index]
            color = '#%02x%02x%02x' % rgb
            self.canvas.create_polygon(*xy, fill=color, outline='#35404a', width=1)

/* Goemon Oedo silver key and door, Japan rev-0, read-only Project64 interpreter tracer.
 * Original MIPS event IDs 0x113 (lock) and 0x114 (collected key).
 * No timers, global CPU hooks, memory edits, debugger pauses or file writes.
 */
(function () {
    'use strict';
    var region = 'japan_0';
    var bank = 0x80161DF8;
    var sceneAddress = 0x800CD2A2;
    var eventByte = (bank + (0x113 >>> 3)) >>> 0;
    var entry = {SET: 0x80023CF8, CLEAR: 0x80023D48, TEST: 0x80023D9C};
    var counts = {SET: 0, CLEAR: 0, TEST: 0, READ: 0, WRITE: 0};
    function hex(v, digits) {
        if (typeof v !== 'number' || !isFinite(v)) return '?';
        var s = (v >>> 0).toString(16).toUpperCase();
        return '0x' + ('00000000' + s).slice(-digits);
    }
    function reg(name, index) {
        try {
            if (typeof gpr !== 'undefined' && gpr !== null) {
                if (typeof gpr[name] === 'number') return gpr[name] >>> 0;
                if (typeof gpr[index] === 'number') return gpr[index] >>> 0;
            }
            if (typeof cpu !== 'undefined' && cpu && cpu.gpr) {
                if (typeof cpu.gpr[name] === 'number') return cpu.gpr[name] >>> 0;
                if (typeof cpu.gpr[index] === 'number') return cpu.gpr[index] >>> 0;
            }
        } catch (ignored) {}
        return -1;
    }
    function pc(e) {
        if (e && typeof e.pc === 'number') return e.pc >>> 0;
        try {
            if (typeof gpr !== 'undefined' && typeof gpr.pc === 'number') return gpr.pc >>> 0;
            if (typeof cpu !== 'undefined' && typeof cpu.pc === 'number') return cpu.pc >>> 0;
        } catch (ignored) {}
        return -1;
    }
    function byte() { try { return mem.u8[eventByte] >>> 0; } catch (ignored) { return -1; } }
    function scene() { try { return mem.u16[sceneAddress] >>> 0; } catch (ignored) { return -1; } }
    function out(kind, detail) {
        counts[kind]++;
        if (counts[kind] > (kind === 'READ' ? 64 : 100)) return;
        console.log('[GOEMON ' + region + ' OEDO] ' + kind + ' ' + detail +
            ' scene=' + hex(scene(), 3) + ' saved=' + hex(byte(), 2));
    }
    function hook(name) {
        events.onexec(entry[name], function (e) {
            var id = reg('a0', 4);
            if (id !== 0x113 && id !== 0x114) return;
            out(name, 'pc=' + hex(pc(e), 8) + ' id=' + hex(id, 4) +
                ' mask=' + hex(1 << (id & 7), 2) + ' callerRA=' + hex(reg('ra', 31), 8));
        });
    }
    hook('SET'); hook('CLEAR'); hook('TEST');
    events.onread(eventByte, function (e) {
        out('READ', 'pc=' + hex(pc(e), 8));
    });
    events.onwrite(eventByte, function (e) {
        var p = pc(e), source = -1;
        try {
            if (p >= 0) {
                var inst = mem.u32[p] >>> 0;
                if ((inst >>> 26) === 40) source = reg('', (inst >>> 16) & 31);
            }
        } catch (ignored) {}
        out('WRITE', 'pc=' + hex(p, 8) + ' newByteCandidate=' +
            (source >= 0 ? hex(source & 255, 2) : '?'));
    });
    console.log('[GOEMON ' + region + ' OEDO] READY: event byte ' + hex(eventByte, 8) +
        '; interpreter core required; stop other debug scripts first.');
})();

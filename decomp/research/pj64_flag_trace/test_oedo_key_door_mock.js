/* ROM-free Project64 API compatibility and read-only behavioural tests. */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

function run(region, legacy, bank, sceneAddr, setPc, clearPc, testPc) {
    const file = path.join(__dirname, 'oedo_key_door_' + region + '.js');
    const js = fs.readFileSync(file, 'utf8');
    const calls = {exec: {}, read: {}, write: {}};
    const logs = [];
    const eventByte = (bank + (0x113 >>> 3)) >>> 0;
    const bytes = {[eventByte]: 0x10};
    const halfwords = {[sceneAddr]: 0x00D};
    const words = {[setPc]: ((40 << 26) | (4 << 21) | (13 << 16) | 8) >>> 0};
    const gpr = {a0: 0x114, ra: 0x08000610, pc: setPc, 13: 0x18};
    const noWrites = source => new Proxy(source, {
        set() { throw new Error('Trace modified N64 memory'); }
    });
    const host = {
        events: {
            onexec: (addr, f) => { assert.notStrictEqual(typeof addr, 'object'); calls.exec[addr >>> 0] = f; },
            onread: (addr, f) => { calls.read[addr >>> 0] = f; },
            onwrite: (addr, f) => { calls.write[addr >>> 0] = f; }
        },
        mem: {u8: noWrites(bytes), u16: noWrites(halfwords), u32: noWrites(words)},
        console: {log: s => logs.push(String(s))}
    };
    if (legacy) host.gpr = gpr;
    else host.cpu = {gpr, pc: setPc};
    vm.runInNewContext(js, host, {timeout: 1000});
    assert.deepStrictEqual(Object.keys(calls.exec).map(Number).sort(), [setPc, clearPc, testPc].sort());
    assert(calls.read[eventByte] && calls.write[eventByte]);
    assert(logs.some(s => s.includes('READY')));
    calls.exec[setPc]({pc: setPc});
    assert(logs.some(s => s.includes('SET') && s.includes('id=0x0114') && s.includes('callerRA=0x08000610')));
    gpr.a0 = 0x113;
    gpr.ra = 0x0800106C;
    if (!legacy) host.cpu.pc = testPc;
    else gpr.pc = testPc;
    calls.exec[testPc]({pc: testPc});
    assert(logs.some(s => s.includes('TEST') && s.includes('id=0x0113') && s.includes('mask=0x08')));
    gpr.a0 = 0x082;
    const length = logs.length;
    calls.exec[clearPc]({pc: clearPc});
    assert.strictEqual(logs.length, length, 'unrelated ID was logged');
    if (!legacy) host.cpu.pc = 0x80023D44;
    else gpr.pc = 0x80023D44;
    words[0x80023D44] = ((40 << 26) | (4 << 21) | (13 << 16) | 8) >>> 0;
    calls.read[eventByte](legacy ? eventByte : {pc: 0x80023DB8, address: eventByte});
    calls.write[eventByte](legacy ? eventByte : {pc: 0x80023D44, address: eventByte});
    assert(logs.some(s => s.includes('READ')));
    assert(logs.some(s => s.includes('WRITE') && s.includes('newByteCandidate=0x18')));
    assert(!js.includes('ADDR_ANY') && !js.includes('setInterval(') && !js.includes('debug.breakhere('));
    process.stdout.write('PASS ' + region + ' ' + (legacy ? 'legacy-gpr' : 'modern-cpu') + '\n');
}
for (const [region, bank, scene, setPc, clearPc, testPc] of [
    ['usa', 0x8015C608, 0x800C7AB2, 0x80024038, 0x80024088, 0x800240DC],
    ['japan_0', 0x80161DF8, 0x800CD2A2, 0x80023CF8, 0x80023D48, 0x80023D9C]
]) {
    run(region, true, bank, scene, setPc, clearPc, testPc);
    run(region, false, bank, scene, setPc, clearPc, testPc);
}

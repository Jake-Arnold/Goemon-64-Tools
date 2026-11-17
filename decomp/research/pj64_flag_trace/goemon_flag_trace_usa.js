/* Goemon 64 read-only, region-pinned Project64 debug trace.
 * Run with Project64 interpreter core and original usa retail ROM.
 * No RAM writes, no save edits, no network or filesystem actions.
 * Install under Project64/Scripts and start through Debugger > Scripts.
 * Unverified against a live Project64 build: synthetic host tests only.
 */
(function () {
  'use strict';
  var region = 'usa';
  var base = 0x8015C608;
  var setterWritePc = 0x80024084;
  var watched = [0x19A, 0x19B, 0x19C, 0x104];
  var counts = {};
  var directCounts = {};
  function hex(value) {
    var text = (value >>> 0).toString(16).toUpperCase();
    return '0x' + ('00000000' + text).slice(-8);
  }
  function trace(kind, flagId, target, extra) {
    var key = kind + ':' + flagId + ':' + target;
    var n = counts[key] || 0;
    if (n >= 3) { return; }
    counts[key] = n + 1;
    console.log('[GOEMON ' + region + '] ' + kind +
      ' flag=' + (flagId === null ? 'UNKNOWN' : hex(flagId)) +
      ' byte=' + hex(target) +
      ' PC=' + hex(cpu.pc) +
      ' A0=' + hex(cpu.gpr.a0) +
      ' RA=' + hex(cpu.gpr.ra) +
      ' S0=' + hex(cpu.gpr.s0) +
      ' V0=' + hex(cpu.gpr.v0) +
      ' oldByte=' + hex(mem.u8[target]) +
      ' ' + (extra || ''));
    debug.breakhere();
  }
  // Executed immediately before the SB in the native packed-bit setter.
  // A0 is the flag ID; RA returns to the calling actor/script function.
  events.onexec(setterWritePc, function (event) {
    var flagId = cpu.gpr.a0 >>> 0;
    if (watched.indexOf(flagId) < 0) { return; }
    var byteAddr = (base + (flagId >>> 3)) >>> 0;
    trace('NATIVE_SET', flagId, byteAddr,
      'mask=' + hex(1 << (flagId & 7)) + ' callerJalr=' + hex((cpu.gpr.ra - 8) >>> 0));
  });
  function monitorDirect(byteAddr) {
    events.onwrite(byteAddr, function (event) {
      // Native SB is already covered above; avoid two stops for one write.
      if ((event.pc >>> 0) === setterWritePc) { return; }
      var key = String(byteAddr >>> 0);
      var n = directCounts[key] || 0;
      if (n >= 4) { return; }
      directCounts[key] = n + 1;
      trace('OTHER_WRITE', null, byteAddr,
        'writeAddress=' + hex(event.address) +
        ' rawValue=' + hex(event.value) +
        ' valueType=' + String(event.valueType));
    });
  }
  // Bytes for torch flags 0x19A/19B/19C and Mr Arrow 0x104.
  monitorDirect((base + 0x33) >>> 0);
  monitorDirect((base + 0x20) >>> 0);
  console.log('[GOEMON ' + region + '] Read-only trace ready. ' +
    'Start the script after loading the target scene.');
})();

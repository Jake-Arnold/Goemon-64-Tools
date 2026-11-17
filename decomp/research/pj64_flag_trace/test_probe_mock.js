/* Synthetic Project64 debugger API tests; no original ROM or save needed. */
const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const path = require('path');

function run(region, base, pc) {
  const program = fs.readFileSync(path.join(__dirname, 'goemon_flag_trace_' + region + '.js'), 'utf8');
  const hooks = {exec: {}, write: {}}, logs = [], breaks = [], bytes = {};
  bytes[(base + 0x33) >>> 0] = 0;
  bytes[(base + 0x20) >>> 0] = 0;
  const gpr = {a0: 0x19a, ra: 0x80001238, s0: 0x80200000, v0: (base + 0x33) >>> 0};
  const host = {
    events: {
      onexec: (addr, fn) => {hooks.exec[addr >>> 0] = fn;},
      onwrite: (addr, fn) => {hooks.write[addr >>> 0] = fn;}
    },
    console: {log: value => logs.push(value)},
    debug: {breakhere: () => breaks.push(true)},
    cpu: {gpr, pc},
    mem: {u8: new Proxy(bytes, {set() {throw Error('Unexpected RAM write');}})}
  };
  vm.runInNewContext(program, host, {timeout: 500});
  assert(hooks.exec[pc >>> 0]);
  assert(hooks.write[(base + 0x33) >>> 0]);
  assert(hooks.write[(base + 0x20) >>> 0]);
  for (const flag of [0x19a, 0x19b, 0x19c, 0x104]) {
    gpr.a0 = flag;
    hooks.exec[pc >>> 0]({pc});
  }
  assert.strictEqual(breaks.length, 4);
  assert(logs[0].includes('NATIVE_SET flag=0x0000019A'));
  assert(logs[0].includes('callerJalr=0x80001230'));
  assert(logs[3].includes('byte=0x' + ((base + 0x20) >>> 0).toString(16).toUpperCase()));
  gpr.a0 = 0x73;
  hooks.exec[pc >>> 0]({pc});
  assert.strictEqual(breaks.length, 4);
  host.cpu.pc = 0x80201014;
  hooks.write[(base + 0x33) >>> 0]({pc: 0x80201014, address: (base + 0x33) >>> 0, value: 4, valueType: 0});
  assert.strictEqual(breaks.length, 5);
  assert(logs[4].includes('OTHER_WRITE'));
  host.cpu.pc = pc;
  hooks.write[(base + 0x33) >>> 0]({pc, address: (base + 0x33) >>> 0, value: 4, valueType: 0});
  assert.strictEqual(breaks.length, 5);
  process.stdout.write('PASS ' + region + ' hooks, filtering, fallback and no RAM mutation\n');
}

run('usa', 0x8015C608, 0x80024084);
run('japan_0', 0x80161DF8, 0x80023D44);

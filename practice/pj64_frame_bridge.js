/* Project64 debugger script; exported by the Goemon Toolkit. ES5 / Duktape. */
(function () {
    'use strict';
    var config = __GOEMON_CONFIG__;
    var server = new Server(), count = 0, plan = [], remaining = 0;
    var armed = false, owned = false, polls = 0, lastPolls = 0;
    var error = '', epoch = 0, generation = 0, deadline = 0;
    function validRom() {
        var r = pj64.romInfo;
        return r && (r.crc1 >>> 0) === config.crc1 && (r.crc2 >>> 0) === config.crc2;
    }
    function integer(v, lo, hi) { return typeof v === 'number' && Math.floor(v) === v && v >= lo && v <= hi; }
    function clear() { plan = []; remaining = 0; armed = false; deadline = 0; }
    function invalidate() { clear(); owned = false; count = 0; polls = 0; lastPolls = 0; epoch++; generation++; }
    function halt() { clear(); owned = true; debug.breakhere(true); }
    function fail(msg) { error = msg; halt(); }
    function check() {
        if (!validRom()) { invalidate(); return false; }
        return true;
    }
    function inputWord(value) { return ((value.buttons << 16) | ((value.x & 255) << 8) | (value.y & 255)) >>> 0; }
    function poll() {
        if (!check() || (mem.u32[PIF_RAM_START] >>> 0) !== 0xFF010401) return;
        if (remaining > 0) {
            if (polls >= 8) { fail('Too many P1 polls within one update interval'); return; }
            mem.u32[PIF_RAM_START + 4] = inputWord(plan[0]);
            polls++;
            if (!config.pc) {
                count++; remaining--; plan.shift(); lastPolls = polls; polls = 0;
                if (!remaining) halt();
            }
        } else if (!config.pc && armed) {
            // Synchronize to a completed P1 PIF sample without overriding it.
            halt();
        }
    }
    function boundary() {
        if (!check()) return;
        if (remaining > 0) {
            count++; remaining--; plan.shift(); lastPolls = polls; polls = 0;
            if (!lastPolls) { fail('No P1 poll in update interval; input not consumed'); return; }
            if (!remaining) halt();
        } else if (armed) halt();
    }
    events.onpifread(poll);
    if (config.pc) events.onexec(config.pc, boundary);
    events.onstatechange(function (e) {
        if (e.state === EMU_RESETTING || e.state === EMU_RESET || e.state === EMU_STOPPED || e.state === EMU_LOADED_ROM) invalidate();
        else if (e.state === EMU_DEBUG_RESUMED && owned) invalidate();
        else if (e.state === EMU_PAUSED || (e.state === EMU_DEBUG_PAUSED && !owned)) {
            invalidate(); error = 'External pause; resynchronize at a bridge boundary';
        }
    });
    setInterval(function () {
        if (deadline && Date.now() > deadline) {
            clear(); owned = false; generation++; error = 'Boundary timeout; queued input cleared';
        }
    }, 250);
    function status() {
        return {version:1, mode:config.pc ? 'execution-hook' : 'controller-poll', pc:config.pc,
                region:config.region, valid:!!validRom(), epoch:epoch, generation:generation,
                count:count, paused:!!debug.paused, ready:owned && !!debug.paused,
                pending:armed || remaining > 0 || (owned && !debug.paused), remaining:remaining, polls:lastPolls, error:error};
    }
    function command(q) {
        if (!q || q.token !== config.token || q.version !== 1) throw Error('Unauthorized or incompatible request');
        if (q.op === 'status') return status();
        if (!check()) throw Error('Expected Goemon retail ROM is not loaded');
        if (q.op === 'pause') {
            if (owned && debug.paused) return status();
            if (debug.paused) throw Error('Resume the existing debugger break first');
            if (remaining || armed) throw Error('Operation already pending');
            error = ''; armed = true; owned = false; count = 0; epoch++; generation++; deadline = Date.now() + 30000;
        } else if (q.op === 'step') {
            if (!owned || !debug.paused || remaining || armed || q.epoch !== epoch || q.count !== count || q.generation !== generation)
                throw Error('Synchronize to a fresh bridge pause first');
            if (!Array.isArray(q.inputs) || q.inputs.length < 1 || q.inputs.length > 60) throw Error('Expected 1..60 input samples');
            q.inputs.forEach(function (v) {
                if (!v || !integer(v.buttons,0,0xFFFF) || (v.buttons & 0x00C0) || !integer(v.x,-80,80) || !integer(v.y,-80,80)) throw Error('Invalid N64 input');
            });
            plan = q.inputs.slice(); remaining = plan.length; polls = 0; owned = false; error = ''; generation++; deadline = Date.now() + 30000;
            debug.resume();
        } else if (q.op === 'resume') {
            if (!owned || !debug.paused) throw Error('Not paused by this bridge');
            clear(); owned = false; generation++; debug.resume();
        } else if (q.op === 'cancel') {
            // No ongoing input override after cancellation. Do not resume another debugger break.
            clear(); owned = owned && !!debug.paused; generation++;
        } else throw Error('Unknown operation');
        return status();
    }
    // Local-only, authenticated, one bounded request per connection. No eval or arbitrary RAM commands.
    server.on('connection', function (socket) {
        var buffer = '', done = false;
        socket.on('error', function () {});
        socket.on('data', function (data) {
            if (done) return;
            buffer += data.toString();
            if (buffer.length > 16384) { done = true; socket.close(); return; }
            var end = buffer.indexOf('\n');
            if (end < 0) return;
            done = true;
            var response;
            try { response = {ok:true, status:command(JSON.parse(buffer.slice(0,end)))}; }
            catch (e) { response = {ok:false, error:String(e)}; }
            socket.end(JSON.stringify(response) + '\n');
        });
    });
    server.on('error', function (e) { console.log('Goemon frame bridge: ' + e); });
    server.listen(config.port, '127.0.0.1');
    console.log('Goemon frame bridge listening on localhost:' + config.port);
}());

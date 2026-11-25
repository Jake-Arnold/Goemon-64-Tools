// Execute the exported Project64 script against a synchronous API mock, not an emulator.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const template = fs.readFileSync('practice/pj64_frame_bridge.js', 'utf8');
function setup(pc) {
    let connect, onPoll, onExec, onState, timers=[];
    const config={token:'a'.repeat(32), port:47651, region:'usa',crc1:0xFCBCCB21,crc2:0x72903C6B,pc};
    const mem={u32:{0:0xFF010401,4:0}}, debug={paused:false,breakhere(){this.paused=true;onState({state:7});},resume(){this.paused=false;onState({state:8});}};
    const pj64={romInfo:{crc1:config.crc1,crc2:config.crc2}};
    const context={Server:function(){this.on=(name,f)=>{if(name==='connection')connect=f};this.listen=(port,host)=>assert.equal(host,'127.0.0.1');},
        events:{onpifread:f=>onPoll=f,onexec:(addr,f)=>{assert.equal(addr,pc);onExec=f;},onstatechange:f=>onState=f},
        mem,debug,pj64,PIF_RAM_START:0,EMU_RESETTING:1,EMU_RESET:2,EMU_STOPPED:3,EMU_LOADED_ROM:4,EMU_PAUSED:5,EMU_DEBUG_PAUSED:7,EMU_DEBUG_RESUMED:8,console:{log(){}},setInterval:f=>timers.push(f)};
    vm.runInNewContext(template.replace('__GOEMON_CONFIG__',JSON.stringify(config)),context);
    function command(op,fields={}){let handlers={},out;connect({on:(n,f)=>handlers[n]=f,end:s=>out=JSON.parse(s),close(){}});handlers.data(Buffer.from(JSON.stringify({version:1,token:config.token,op,...fields})+'\n'));return out;}
    return {command,poll:()=>onPoll(),exec:()=>onExec(),state:n=>onState({state:n}),mem,debug,pj64};
}
const A={buttons:0x8000,x:-80,y:80}, neutral={buttons:0,x:0,y:0};
function step(b,s,inputs){return b.command('step',{epoch:s.epoch,count:s.count,generation:s.generation,inputs});}
for(const pc of [0,0x80001000]){
    const b=setup(pc), boundary=pc?b.exec:b.poll;
    assert.equal(b.command('pause',{token:'wrong'}).ok,false);
    assert.equal(b.command('pause').status.pending,true);
    boundary(); let s=b.command('status').status;
    assert.equal(s.ready,true); assert.equal(s.count,0);
    assert.equal(step(b,s,[A,neutral]).ok,true);
    b.poll();assert.equal(b.mem.u32[4],0x8000B050);
    if(pc){b.poll();assert.equal(b.mem.u32[4],0x8000B050);b.exec();}
    assert.equal(b.command('status').status.count,1);
    b.poll();assert.equal(b.mem.u32[4],0);
    if(pc)b.exec();
    let end=b.command('status').status;assert.equal(end.count,2);assert.equal(end.ready,true);
    assert.equal(step(b,s,[A]).ok,false); // stale epoch/count/generation
    assert.equal(step(b,end,[A]).ok,true);b.state(1);b.mem.u32[4]=123;b.poll();assert.equal(b.mem.u32[4],123);
    b.pj64.romInfo.crc1=0;assert.equal(b.command('pause').ok,false);
}
const b=setup(0x80001000);b.command('pause');b.exec();let s=b.command('status').status;step(b,s,[A]);b.exec();assert.match(b.command('status').status.error,/No P1 poll/);
console.log('PJ64 script mock: poll, update hook, exact P1 word, stale state, wrong ROM, reset and missing poll PASS');

from pathlib import Path
import itertools
p=Path(__file__).parent/'sources';s=(p/'usa_scale.c').read_text();d='D_8020C860_5C8770'; t='D_801FC604_5B8514';old=f'    {t}->field5c={d};\n    {d}[0]=0;\n    for(i=1;i<49;i++) {{}}';
# Change expression and lifetime one axis at a time; C89 local declarations before statements.
forms=[f'{t}->field5c={d};', f'q={d}; {t}->field5c=q;',f'{t}->field5c=q={d};', f'task={t}; task->field5c={d};', f'task={t}; q={d}; task->field5c=q;']
loops=[f'for(i=0;i<49;i++) {{ {d}[0]=0; }}',f'for(i=0;i<49;i++) {{ *{d}=0; }}',f'for(i=0;i<49;i++) {{ *q=0; }}',f'for(i=0;i<49;i++) {{ *((int *){t}->field5c)=0; }}',f'{d}[0]=0; for(i=1;i<49;i++) {{ {d}[0]=0; }}',f'{d}[0]=0; for(i=1;i<49;i++) {{}}',f'*q=0; for(i=1;i<49;i++) {{}}',f'for(i=0;i<49;i++) {{ if(i==0) {d}[0]=0; }}',f'for(i=0;i<49;i++) {{ {d}[i-i]=0; }}',f'for(i=0;i<49;i++) {{ {d}[0]=i-i; }}',f'for(i=0;i<49;i++) {{ {d}[0] &= 0; }}',f'for(i=0;i<49;i++) {{ {d}[0] = 0; }}']
for k,(form,loop) in enumerate(itertools.product(forms,loops)):
 if 'q' in loop and 'q=' not in form:continue
 base=s.replace('    int i;', '    int i;\n    int *q;\n    Task *task;')
 v=base.replace(old,'    '+form+'\n    '+loop);(p/f'usa_w{k:03}.c').write_text(v)
# Change declaration order of live locals and call/result form.
call=s[s.index('    D_801FC604_5B8514=func_'):s.index('\n    D_801FC604_5B8514->field5c')]
body=call.split('=',1)[1].rstrip(';');
pre=['float scale = D_8020A6DC_5C65EC;\n    Pending *p=(Pending *)(D_8015C5C8_15D1C8+0x38000);\n    int i;','int i;\n    float scale = D_8020A6DC_5C65EC;\n    Pending *p=(Pending *)(D_8015C5C8_15D1C8+0x38000);','register int i;\n    float scale = D_8020A6DC_5C65EC;\n    Pending *p=(Pending *)(D_8015C5C8_15D1C8+0x38000);','float scale; Pending *p; int i;\n    scale=D_8020A6DC_5C65EC; p=(Pending *)(D_8015C5C8_15D1C8+0x38000);']
for k,(decl,form) in enumerate(itertools.product(pre,range(7))):
 v=s.replace(pre[0],decl);v=v.replace('    '+decl,'    Task *task; int *q;\n    '+decl)
 if form==0: v=v.replace(call,f'    task={body};\n    {t}=task;').replace(f'{t}->field5c={d};',f'task->field5c={d};')
 if form==1:v=v.replace(call,f'    task={t}={body};').replace(f'{t}->field5c={d};',f'task->field5c={d};')
 if form==2:v=v.replace(call,f'    {t}=task={body};').replace(f'{t}->field5c={d};',f'task->field5c={d};')
 if form==3:v=v.replace(call,f'    {t}=task={body};').replace(f'{t}->field5c={d};',f'task->field5c=q={d};').replace(f'{d}[0]=0;', '*q=0;')
 if form==4:v=v.replace(call,f'    {t}=task={body};').replace(f'{t}->field5c={d};',f'q={d}; task->field5c=q;').replace(f'{d}[0]=0;', '*q=0;')
 if form==5:v=v.replace(f'{t}->field5c={d};',f'q={d}; {t}->field5c=q;').replace(f'{d}[0]=0;', '*q=0;')
 if form==6:v=v.replace(f'{t}->field5c={d};',f'{t}->field5c=q={d};').replace(f'{d}[0]=0;', '*q=0;')
 (p/f'usa_x{k:03}.c').write_text(v)

from pathlib import Path
import re,itertools
p=Path(__file__).parent/'sources'; s=(p/'usa_scale.c').read_text(); m='D_8020C860_5C8770'; old=f'    D_801FC604_5B8514->field5c={m};\n    {m}[0]=0;\n    for(i=1;i<49;i++) {{}}'; assert old in s
loops=['for(i=1;i<49;i++) {}','for(i=1;i!=49;i++) {}','for(i=1;i<=48;i++) {}','for(i=1;i<49;i+=4) {}','for(i=1;i!=49;i+=4) {}','i=1; while(i<49) i++;','i=1; do {i++;} while(i<49);','for(i=0;i<48;i++) {}','for(i=1;i<49;i++) { (void)i; }','for(i=1;i<49;i++) { if(0) break; }']
forms=[f'D_801FC604_5B8514->field5c={m};\n    {m}[0]=0;',f'int *q={m};\n    D_801FC604_5B8514->field5c=q;\n    q[0]=0;',f'int *q;\n    D_801FC604_5B8514->field5c=q={m};\n    *q=0;',f'D_801FC604_5B8514->field5c={m};\n    *((int *)D_801FC604_5B8514->field5c)=0;',f'int *q={m};\n    D_801FC604_5B8514->field5c=q;\n    *q++=0;',f'D_801FC604_5B8514->field5c={m};\n    *{m}=0;',f'{{ int *q={m}; D_801FC604_5B8514->field5c=q; *q=0; }}',f'{{ Task *t=D_801FC604_5B8514; t->field5c={m}; {m}[0]=0; }}']
for k,(form,loop) in enumerate(itertools.product(forms,loops)):
 t=s.replace(old,'    '+form+'\n    '+loop); (p/f'usa_v{k:03}.c').write_text(t)
for k,t in enumerate(['unsigned int','short','unsigned short','long','unsigned long','char','unsigned char']):
 (p/f'usa_type{k}.c').write_text(s.replace('    int i;',f'    {t} i;'))

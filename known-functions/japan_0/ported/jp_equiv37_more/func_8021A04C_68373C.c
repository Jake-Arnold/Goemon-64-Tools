typedef unsigned char u8;
void func_8021A04C_68373C(u8*o,float v){float *p=(float*)(o+92);u8*sub;float ref;float d;p[7]=v;sub=*(u8**)(o+24);ref=*(float*)(sub+36);if(v<ref){d=-(p[7]-ref);}else{d=p[7]-ref;}p[8]=d/p[0];}


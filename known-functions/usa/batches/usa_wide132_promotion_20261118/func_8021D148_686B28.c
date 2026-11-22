typedef unsigned char u8;
void func_8021D148_686B28(u8*o,float v){float *p=(float*)(o+92);u8*sub;float ref;float d;p[6]=v;sub=*(u8**)(o+24);ref=*(float*)(sub+36);if(v<ref){d=-(p[6]-ref);}else{d=p[6]-ref;}p[5]=d/p[1];}

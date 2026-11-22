int func_801EE330_5AA240(unsigned char* a,unsigned char value,unsigned char limit){unsigned char*p=(unsigned char*)a;if (value < (*p - limit)) {*p = *p - value;return 0;}*p = limit;return 1;}

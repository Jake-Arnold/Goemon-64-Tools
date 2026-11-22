int func_801EE2EC_5AA1FC(unsigned char* a,unsigned char value,unsigned char limit){unsigned char*p=(unsigned char*)a;if (value < (limit - *p)) {*p = *p + value;return 0;}*p = limit;return 1;}

extern void __osSpSetStatus(int); void osSpTaskYield(void){__osSpSetStatus(0x400);}

extern char func_80014840_15440;
extern char D_0A00C980;
int func_08001228_6AE5E8(void) {
    int x = ((int(*)(void*,unsigned))&func_80014840_15440)(&D_0A00C980,0x152);
    if (x == -1) return 0;
    return x;
}

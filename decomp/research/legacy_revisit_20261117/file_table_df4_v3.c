extern unsigned int func_80001E50_2A50(unsigned int);
extern unsigned int D_80054AC4_556C4[][2];
unsigned int func_80001DF4_29F4(unsigned int arg0) {
    unsigned int result;
    if (func_80001E50_2A50(arg0) != 17) {
        if (arg0 == 0) result = 0;
        else result = D_80054AC4_556C4[arg0][0] & 0x40000000;
    } else result = 0x40000000;
    return result;
}

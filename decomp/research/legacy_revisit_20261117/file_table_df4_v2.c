extern unsigned int func_80001E50_2A50(unsigned int);
extern unsigned int D_80054AC4_556C4[][2];
unsigned int func_80001DF4_29F4(unsigned int arg0) {
    unsigned int result = 0;
    if (func_80001E50_2A50(arg0) == 17) {
        result = 0x40000000;
        goto done;
    }
    if(arg0) result = D_80054AC4_556C4[arg0][0] & 0x40000000;
done:
    return result;
}

typedef unsigned char u8;
typedef short s16;
typedef int s32;
extern char D_801C7780_1C8380[];
extern char D_8007CF60_7DB60[];
extern s32 D_801C7740_1C8340;
extern char *D_801C779C_1C839C;
extern s16 D_801C77A8_1C83A8[];
extern s16 *D_801C77DC_1C83DC;
extern s32 D_801C7754_1C8354;
extern int sprintf(char *, const char *, ...);
extern void func_8003EB34_3F734(s32);
void func_8003F480_40080(void) {
    s16 *dest;
    u8 ch;
    sprintf(D_801C7780_1C8380, D_8007CF60_7DB60, D_801C7740_1C8340);
    D_801C779C_1C839C = D_801C7780_1C8380;
    dest = D_801C77A8_1C83A8;
    if (*D_801C7780_1C8380) { do { *dest++ = (u8)*D_801C779C_1C839C++ - 0x30; } while (*D_801C779C_1C839C); }
    *dest = -1;
    D_801C77DC_1C83DC = dest;
    func_8003EB34_3F734(D_801C7754_1C8354);
}

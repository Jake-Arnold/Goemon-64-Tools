typedef signed int s32;
typedef signed short s16;
typedef unsigned char u8;
extern s32 sprintf(char *, const char *, ...);
extern char D_801C7780_1C8380[];
extern const char D_8007CF60_7DB60[];
extern s32 D_801C7740_1C8340;
extern char *D_801C779C_1C839C;
extern s16 D_801C77A8_1C83A8[];
extern s16 *D_801C77DC_1C83DC;
extern s32 D_801C7754_1C8354;
extern void func_8003EB34_3F734(s32);
void func_8003F480_40080(void) {
    char *src;
    s16 *dst;
    s32 value;
    char *format;
    value = D_801C7740_1C8340;
    format = (char *)D_8007CF60_7DB60;
    sprintf(D_801C7780_1C8380, format, value);
    D_801C779C_1C839C = D_801C7780_1C8380;
    src = D_801C779C_1C839C;
    dst = D_801C77A8_1C83A8;
    if (*src != 0) {
        do {
            *dst++ = (u8)*src++ - 0x30;
        } while (*src != 0);
        D_801C779C_1C839C = src;
    }
    *dst = -1;
    D_801C77DC_1C83DC = dst;
    func_8003EB34_3F734(D_801C7754_1C8354);
}

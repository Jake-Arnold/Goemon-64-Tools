typedef unsigned char u8; typedef unsigned short u16; typedef int s32;
#define F(p,t,o) (*(t *)((u8 *)(p)+(o)))
extern s32 func_801E864C_5A455C(void *);
extern void func_80038BC8_397C8(s32);
s32 func_801DD114_599024(void *arg0) {
    u8 temp_v0;
    u8 temp_v0_2;
    s32 temp_v1;
    void *temp_v0_3;

    temp_v0 = F(arg0,u8,0x60);
    switch (temp_v0) {
    case 1:
        if (func_801E864C_5A455C(arg0) == 0) {
            func_80038BC8_397C8(0x3AC);
            goto block_24;
        }
        if ((F(F(arg0,void *,0x5C),u16,0x86) == 0xFFFF) && (F(arg0,u8,0xCC) == 0x42) && (F(arg0,s32,0x38) == 0)) {
            temp_v0 = 1; goto end;
        }
    case 0:
    case 2:
        if (F(F(arg0,void *,0x5C),u16,0x86) == 0xFFFF) {
            temp_v0_2 = F(arg0,u8,0xCC);
            if (((s32) temp_v0_2 >= 0) && ((s32) temp_v0_2 < 4) && (F(arg0,s32,0x38) == 0)) {
                temp_v0 = 1; goto end;
            }
        }
block_24:
        temp_v0 = 0; goto end;
    case 3:
        temp_v0_3 = F(arg0,void *,0x5C);
        if (F(temp_v0_3,u16,0x86) != 0xFFFF) {
            temp_v0 = 0; goto end;
        }
        if ((F(arg0,u8,0xCC) == 0xAE) && ((temp_v1 = F(temp_v0_3,u8,0x59), ((temp_v1 & 0x80) != 0)) || (temp_v1 == 0)) && (F(arg0,s32,0x38) == 0)) {
            temp_v0 = 1; goto end;
        }
        break;
    default:
        goto end;
    }
    temp_v0 = 0;
end:
    return temp_v0;
}

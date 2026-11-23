typedef unsigned char u8; typedef unsigned int u32; typedef int s32;
typedef struct {u32 w0,w1;} Gfx;
typedef struct {u8 pad[0x5C];u8 field5C,field5D;} VmState;
extern u8 D_80076148_76D48;
extern u8 D_800777F0_783F0;
extern VmState *D_80077860_78460;
extern Gfx *D_8015C5CC_15D1CC;

void func_8003EBAC_3F7AC(s32 arg0, s32 arg1) {
    Gfx *temp_v0;
    Gfx *temp_v0_10;
    Gfx *temp_v0_2;
    Gfx *temp_v0_3;
    Gfx *temp_v0_4;
    Gfx *temp_v0_5;
    Gfx *temp_v0_6;
    Gfx *temp_v0_7;
    Gfx *temp_v0_9;
    Gfx *temp_v0_8;

    temp_v0 = D_8015C5CC_15D1CC++;
    temp_v0->w0 = 0x06000000; temp_v0->w1 = &D_800777F0_783F0;
    temp_v0_2 = D_8015C5CC_15D1CC++;
    temp_v0_2->w0 = 0xFD100000; temp_v0_2->w1 = &D_80076148_76D48;
    temp_v0_3 = D_8015C5CC_15D1CC++;
temp_v0_3->w0 = 0xF5100000;     temp_v0_3->w1 = 0x07000000;
    temp_v0_4 = D_8015C5CC_15D1CC++;
    temp_v0_4->w1 = 0;
    temp_v0_4->w0 = 0xE6000000;
    temp_v0_5 = D_8015C5CC_15D1CC++;
temp_v0_5->w0 = 0xF3000000;     temp_v0_5->w1 = 0x077FF100;
    temp_v0_6 = D_8015C5CC_15D1CC++;
    temp_v0_6->w1 = 0;
    temp_v0_6->w0 = 0xE7000000;
    temp_v0_7 = D_8015C5CC_15D1CC++;
    temp_v0_7->w1 = 0;
    temp_v0_7->w0 = 0xF5101000;
    temp_v0_8 = D_8015C5CC_15D1CC++;
temp_v0_8->w0 = 0xF2000000;     temp_v0_8->w1 = 0x7C0FC;
    temp_v0_9 = D_8015C5CC_15D1CC++;
    arg1 = (s32)((u32)arg1 - 2U);
    temp_v0_9->w0 = (s32) ((((((((u32)arg0 + 15) << 2)) & 0xFFF) << 0xC) | 0xE4000000 | ((((((u32)arg1 + 15)) << 2)) & 0xFFF)));
    temp_v0_9->w1 = (s32) ((((((u32)arg0 << 2)) & 0xFFF) << 0xC) | ((((u32)arg1 << 2)) & 0xFFF));
    temp_v0_10 = D_8015C5CC_15D1CC++;
    temp_v0_10->w0 = 0xB4000000;
    temp_v0_10->w1 = (s32) ((((D_80077860_78460->field5C & 3) << 9) & 0xFFFF) | ((D_80077860_78460->field5C & 4) << 0x17));
    temp_v0_10 = D_8015C5CC_15D1CC++;
    temp_v0_10->w0 = 0xB3000000; temp_v0_10->w1 = 0x10000400;
}

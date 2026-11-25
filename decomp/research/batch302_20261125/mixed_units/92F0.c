#include "common.h"
void func_8000A344_AF44(void);
void func_8000A430_B030(void);
void func_8000A4F8_B0F8(void);
void func_8000A5C4_B1C4(void *);
void func_8000A480_B080(CLS_GBG_W *);

const unsigned int D_8007AAA0_7B6A0[] = {
    0x00000000,
    0x00008000,
    0x0000C000,
    0x0000C000,
    0x00008000
};

const unsigned int D_8007AAB4_7B6B4[] = {
    0x00000000,
    0x00000002,
    0x00000003,
    0x00000004,
    0x00000001
};

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_800086F0_92F0.s")

/* Original native C for func_80008798_9398 */
typedef struct{u32 w0,w1;} Iso233Gfx; extern Iso233Gfx *D_8015C5CC_15D1CC;extern u8 D_8006D600_6E200[];void func_80008798_9398(void){Iso233Gfx *p=D_8015C5CC_15D1CC++; p->w0=0x06000000; p->w1=(u32)D_8006D600_6E200;}

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_800087C4_93C4.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_80008920_9520.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_80009408_A008.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_80009548_A148.s")

void func_8000A130_AD30(void);
/* Original native C for func_8000A0F0_ACF0 */
void func_8000A0F0_ACF0(void) {
    func_8000A130_AD30();
    func_8000A4F8_B0F8();
    func_8000A344_AF44();
    func_8000A430_B030();
    func_8000A614_B214();
}


#define BATCH302_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
extern void func_8000A18C_AD8C(void);
extern s32 func_8000A228_AE28(s32 *);
extern s32 D_8014FA54_150654;
void func_8000A130_AD30(void) {
    s32 *var_s0;
    s32 var_s1;

    var_s0 = &D_8014FA54_150654;
    var_s1 = 0;
    do {
        func_8000A228_AE28(var_s0);
        var_s1 += 1;
        var_s0 += 0x10;
        BATCH302_FIELD(var_s0, s32 *, -4) = 0;
    } while (var_s1 != 0x18);
    func_8000A18C_AD8C();
}
#undef BATCH302_FIELD

/* Original native C for func_8000A18C_AD8C */
#include "common.h"

/* Offsets are original machine-code data offsets, not invented field semantics. */
typedef struct {
    u8 pad[0x5D06];
    s16 field_5D06;
    s16 field_5D08;
    s16 field_5D0A;
    s16 field_5D0C;
    s32 field_5D10;
} File92State;

extern File92State D_8014CCC0_14D8C0;

void func_8000A18C_AD8C(void) {
    D_8014CCC0_14D8C0.field_5D0C = 255;
    D_8014CCC0_14D8C0.field_5D10 = 0;
    D_8014CCC0_14D8C0.field_5D0A = D_8014CCC0_14D8C0.field_5D0C;
    D_8014CCC0_14D8C0.field_5D08 = D_8014CCC0_14D8C0.field_5D0A;
    D_8014CCC0_14D8C0.field_5D06 = D_8014CCC0_14D8C0.field_5D08;
}


#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A1BC_ADBC.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A228_AE28.s")

#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A2C8_AEC8.s")

/* Original native C for func_8000A344_AF44 */
extern s32 D_800C8328_C8F28;
void func_8000A344_AF44(void) {
    u8 *var_s0;
    s32 var_s1;

    var_s0 = (u8*)&D_800C8328_C8F28;
    var_s1 = 0;
    do {
        func_8000A394_AF94(var_s0);
        var_s1 += 1;
        var_s0 += 0x250;
    } while (var_s1 != 2);
}


#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A394_AF94.s")

/* Original native C for func_8000A430_B030 */
extern s32 D_801487C8_1493C8;
void func_8000A430_B030(void) {
    u8 *var_s0;
    s32 var_s1;

    var_s0 = (u8*)&D_801487C8_1493C8;
    var_s1 = 0;
    do {
        func_8000A480_B080(var_s0);
        var_s1 += 1;
        var_s0 += 0x44;
    } while (var_s1 != 2);
}


void func_8000A480_B080(CLS_GBG_W *arg0) 
{
    arg0->header.kind = 0x85;
    arg0->header.pri = 0;
    arg0->header.s_pri = 0;
    arg0->unk_8 = 0;
    arg0->texture_data = 0;
    arg0->palette_data = 0;
    arg0->wave_no = 0;
    arg0->flags = 0x8009;
    arg0->texture_width = 320;
    arg0->texture_height = 240;
    arg0->min_x = 0;
    arg0->min_y = 0;
    arg0->max_x = 319;
    arg0->max_y = 239;
    arg0->bits_per_pixel = 8;
    arg0->u = 0.0f;
    arg0->v = 0.0f;
    arg0->x = 0.0f;
    arg0->y = 0.0f;
    arg0->w = 0.0f;
    arg0->h = 0.0f;
}

/* Original native C for func_8000A4F8_B0F8 */
extern s32 D_80148850_149450;
void func_8000A4F8_B0F8(void) {
    u8 *var_s0;
    s32 var_s1;

    var_s0 = (u8*)&D_80148850_149450;
    var_s1 = 0;
    do {
        func_8000A5C4_B1C4(var_s0);
        var_s1 += 1;
        var_s0 += 0x98;
    } while (var_s1 != 0xC0);
}


/* Original native C for func_8000A548_B148 */
#include "common.h"
void func_8000A5C4_B1C4(void*);
void func_8000A548_B148(s32 start,s32 end) {
 s32 i;
 u8* p=(u8*)&D_8008CCC0_8D8C0+0xBBB90+start*0x98;
 for(i=start;i<end+1;i++) {
 func_8000A5C4_B1C4(p);
 p+=0x98;
 }
}


/* Original native C for func_8000A5C4_B1C4 */
#include "common.h"
typedef struct { u32 words[38]; } A5C4Struct;
extern A5C4Struct D_8005B974_5C574;
void func_8000A5C4_B1C4(void *arg0) {
    A5C4Struct *p = arg0;
    u32 old_word0 = p->words[0];
    *p = D_8005B974_5C574;
    p->words[0] = old_word0;
}


#pragma GLOBAL_ASM("asm/usa/nonmatchings/92F0/func_8000A614_B214.s")

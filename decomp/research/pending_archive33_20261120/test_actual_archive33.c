/* Test actual, individually original-IDO verified C sources, not reimplementations.
   Run under GCC ASan+UBSan with safe aligned test structures. */
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stddef.h>
typedef int s32; typedef short s16; typedef unsigned short u16; typedef float f32;
typedef int M2C_UNK;
typedef union { max_align_t align; unsigned char b[512]; } B;
#define F(o,x) (*(float*)((o).b+(x)))
#define S(o,x) (*(short*)((o).b+(x)))
#define I(o,x) (*(int*)((o).b+(x)))
#define P(o,x) (*(void**)((o).b+(x)))
extern void func_80012470_13070(void *arg0);
extern void func_80047850_48450(void);
extern void func_80047990_48590(void);
extern void func_80222548_5DDA18(s32 arg0, M2C_UNK arg1, M2C_UNK arg2, M2C_UNK arg3);
extern void func_801D620C_6015EC(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_801CE61C_63D46C(void *arg0, M2C_UNK arg1);
extern void func_801D1630_640480(void *arg0, s16 *arg1);
extern void func_801D1790_6405E0(void *arg0, s16 *arg1);
extern void func_801D3BE0_642A30(void *arg0);
extern void func_801D3BF0_642A40(void *arg0);
extern void func_801D4400_643250(void *arg0, M2C_UNK arg1);
extern s32 func_80214304_6732B4(s32 arg0);
extern void func_801CBC80_69D3F0(void *arg0, s32 arg1, s32 arg2);
extern void func_0800B38C_6BE62C(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_08000298_6BF9E8(void *arg0, M2C_UNK arg1);
extern void func_08001CC4_6EAE14(void *arg0, void *arg1);
extern void func_0800606C_6F954C(void *arg0, void *arg1);
extern void func_08000FA8_7089E8(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_080009E4_70AA24(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_08000D18_7215E8(void *arg0, f32 arg1, f32 arg2, f32 arg3, u16 arg4);
extern void func_08000F2C_72A4CC(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_08001058_72C8A8(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_0800148C_72CCDC(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_0800105C_7308EC(void *arg0);
extern void func_08001328_730BB8(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_0800134C_730BDC(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4);
extern void func_08001860_7310F0(void *arg0, s32 arg1);
extern void func_080012A4_7341D4(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_080012C8_7341F8(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4);
extern void func_08001634_734564(void *arg0, s32 arg1);
extern void func_08000DDC_7394AC(void *arg0, f32 arg1, f32 arg2, f32 arg3, u16 arg4);
extern void func_080007A8_73C3A8(void *arg0, f32 arg1, f32 arg2, f32 arg3);
extern void func_08000460_73CA70(void *arg0, f32 arg1, f32 arg2, f32 arg3, f32 arg4);

int main(void) {
    for (int trial=1;trial<=1000;trial++) {
        B o={0}, target={0}, control={0};
        s16 flags=0;
        /* simple scheduler resets and genuinely empty original bodies */
        I(o,0x7C)=99; F(o,0x9C)=8.0f; S(o,0xCA)=7;
        func_80012470_13070(o.b);
        assert(I(o,0x7C)==0 && F(o,0x9C)==0.0f && S(o,0xCA)==0);
        func_80047850_48450(); func_80047990_48590();
        func_80222548_5DDA18(11,12,13,14);
        F(o,8)=1.0f; F(o,12)=2.0f;F(o,16)=3.0f;
        func_801D620C_6015EC(o.b,1.0f,2.0f,3.0f);
        assert(F(o,8)==2.0f && F(o,12)==4.0f && F(o,16)==6.0f);
        func_801CE61C_63D46C(o.b,0);
        assert(o.b[0x9D]==1 && o.b[0xC4]==0 && I(o,0xB4)==10000);
        o.b[0xA2]=1;
        func_801D1630_640480(o.b,&flags);
        assert(o.b[0xA2]==0 && o.b[0x9E]==2 && (flags & 0x4000));
        func_801D1790_6405E0(o.b,&flags);
        assert(o.b[0xA0]==1 && o.b[0xC5]==2 && (flags & 0x400));
        func_801D3BE0_642A30(o.b);
        assert(o.b[0x9C]==0 && I(o,0xA0)==-20000);
        func_801D3BF0_642A40(o.b);
        assert(o.b[0x9C]==1 && S(o,0xA4)==30);
        func_801D4400_643250(o.b,0);
        assert(o.b[0x9D]==1 && S(o,0xB6)==8);
        assert(func_80214304_6732B4(0)==0);
        /* Host pointer at offset 0x5C: offset object base +4 to preserve 8-byte alignment. */
        P(control,0x60)=target.b;
        func_801CBC80_69D3F0(control.b+4,7,8);
        assert(F(target,0x1C)==7.0f && F(target,0x20)==8.0f);
        P(o,0x18)=target.b;
        P(o,0xD0)=target.b;
        /* Exact original callbacks: nested actor position fields. */
        #define V3(fn) do { F(target,8)=0;F(target,12)=0;F(target,16)=0;           fn(o.b,2.0f,3.0f,4.0f);           assert(F(target,8)==2.0f && F(target,12)==3.0f && F(target,16)==4.0f); } while(0)
        V3(func_0800B38C_6BE62C);
        V3(func_08000FA8_7089E8);
        V3(func_080009E4_70AA24);
        V3(func_08000F2C_72A4CC);
        V3(func_08001058_72C8A8);
        V3(func_0800148C_72CCDC);
        V3(func_08001328_730BB8);
        V3(func_080012A4_7341D4);
        V3(func_080007A8_73C3A8);
        #undef V3
        func_08000D18_7215E8(o.b,2.0f,3.0f,4.0f,123);
        assert(F(target,8)==2.0f && F(target,12)==3.0f && F(target,16)==4.0f && S(target,0x16)==123);
        func_08000DDC_7394AC(o.b,5.0f,6.0f,7.0f,321);
        assert(F(target,8)==5.0f && F(target,12)==6.0f && F(target,16)==7.0f && S(target,0x16)==321);
        /* Field-only flags, setup, positioning and normalized angles. */
        I(o,0x68)=0x8000;
        func_08000298_6BF9E8(o.b,0);
        assert(I(o,0x60)==32);
        I(o,0xD0)=1; S(control,0x16)=0;
        func_08001CC4_6EAE14(o.b,control.b);
        assert(S(control,0x16)==2);
        control.b[0x7C]=2;
        I(o,0x60)=3; I(o,0x68)=0;
        func_0800606C_6F954C(o.b,control.b);
        assert((I(o,0x60)&1)==0 && (I(o,0x68)&2)==2);
        I(o,0x60)=0;
        func_0800105C_7308EC(o.b);
        assert(o.b[0x75]==10 && I(o,0xD4)==1);
        P(o,0xD0)=target.b;
        func_0800134C_730BDC(o.b,5.0f,6.0f,7.0f,8.0f);
        assert(I(target,0x10)==1 && F(target,0x14)==5.0f && F(target,0x20)==8.0f);
        func_080012C8_7341F8(o.b,6.0f,7.0f,8.0f,9.0f);
        assert(I(target,0x10)==1 && F(target,0x14)==6.0f && F(target,0x20)==9.0f);
        I(o,0xD4)=4;
        func_08001860_7310F0(o.b,8);
        assert(I(o,0xE0)==4 && F(o,0xE4)==8.0f && F(o,0xE8)==2.0f);
        I(o,0xD4)=4;
        func_08001634_734564(o.b,8);
        assert(I(o,0xDC)==4 && F(o,0xE0)==8.0f && F(o,0xE4)==2.0f);
        func_08000460_73CA70(o.b,1.0f,2.0f,3.0f,4.0f);
        assert(o.b[0xD2]==1 && F(o,0xD4)==1.0f && F(o,0xE0)==4.0f);
    }
    return 0;
}

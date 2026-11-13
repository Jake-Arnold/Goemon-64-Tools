/* Synthetic C mock calls only; no real game execution or original MIPS run. */
#define GOEMON_DECOMP_HOST_TEST
#include <stddef.h>
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "candidates/vm_setup_f37c.c"

VmControlF37C D_8015CC30_15D830;
s32 D_801C7740_1C8340;
u32 D_801C7750_1C8350;
float D_8007D108_7DD08;
u8 D_8006D920_6E520[8];
static u8 obj[0x100];
static u8 before_obj[sizeof obj];
static u8 before_control[sizeof(VmControlF37C)];
static unsigned call_number;
static unsigned allocator_calls;
static u32 expected_control, expected_actor, expected_scale_bits;
static u8 expected_slot;
static u32 float_bits(float value) {
    u32 bits;
    memcpy(&bits, &value, sizeof bits);
    return bits;
}
static float float_from_bits(u32 bits) {
    float value;
    memcpy(&value, &bits, sizeof value);
    return value;
}
_Static_assert(offsetof(VmControlF37C, field_8c) == 0x8C, "control word offset");
_Static_assert(offsetof(VmControlF37C, flags) == 0xD4, "existing flags offset");
_Static_assert(offsetof(VmControlF37C, byte_d8) == 0xD8, "owner slot offset");
void func_80218F30_5D4400(void *a, void *b) { (void)a; (void)b; }
void func_8021925C_5D472C(void *a, void *b) { (void)a; (void)b; }
u8 *func_80035690_36290(u32 a0,s32 a1,s32 a2,void *a3,float a4,float a5,float a6,
  u16 a7,u16 a8,u16 a9,float a10,float a11,float a12,u16 a13,u16 a14,u16 a15) {
    assert(call_number++ == 0);
    assert(a0==expected_control && (u32)a1==expected_actor && a2==0 && a3==D_8006D920_6E520);
    assert(float_bits(a4)==0 && float_bits(a5)==0 && float_bits(a6)==0);
    assert(a7==0 && a8==0 && a9==0);
    assert(float_bits(a10)==expected_scale_bits && float_bits(a11)==expected_scale_bits && float_bits(a12)==expected_scale_bits);
    assert(a13==0 && a14==0 && a15==0);
    assert(D_801C7750_1C8350==0xA5A5A5A5U);
    assert(D_8015CC30_15D830.byte_d8==expected_slot);
    allocator_calls++;
    return obj;
}
void func_80035244_35E44(u8 *p,VmTaskCallbackF37C callback) {
    assert(call_number++ == 1);
    assert(p == obj && callback == func_80218F30_5D4400);
    assert(D_801C7750_1C8350==(u32)(unsigned long)obj);
    assert(D_8015CC30_15D830.byte_d8==(u8)(expected_slot+1));
    assert(p[0x74]==expected_slot);
}
void func_80035214_35E14(u8 *p,VmTaskCallbackF37C callback) {
    assert(call_number++ == 2);
    assert(p == obj && callback == func_8021925C_5D472C);
    assert(D_801C7750_1C8350==(u32)(unsigned long)obj);
    assert(D_8015CC30_15D830.byte_d8==(u8)(expected_slot+1));
    assert(p[0x74]==expected_slot);
}
static u32 next(u32 *s) {u32 x=*s;x^=x<<13;x^=x>>17;x^=x<<5;*s=x;return x;}
int main(void) {
    u32 state=0x837c237c;
    static const u32 scale_bits[] = {
        0x00000000U, 0x80000000U, 0x3F000000U, 0x7F800000U,
        0xFF800000U, 0x7FC12345U, 0x00000001U, 0x7F7FFFFFU
    };
    for(unsigned i=0;i<300;i++){
       memset(obj,0x5A,sizeof obj);
       memcpy(before_obj,obj,sizeof obj);
       memset(&D_8015CC30_15D830,0x5A,sizeof D_8015CC30_15D830);
       expected_control=next(&state);expected_actor=next(&state);
       expected_scale_bits=(i<sizeof scale_bits/sizeof scale_bits[0]) ? scale_bits[i] : next(&state);
       expected_slot=(i==0)?0xFF:(i==1)?0:(i==2)?0x7F:(u8)next(&state);
       D_8015CC30_15D830.field_8c=expected_control;
       D_8015CC30_15D830.byte_d8=expected_slot;
       D_801C7740_1C8340=(s32)expected_actor;
       D_8007D108_7DD08=float_from_bits(expected_scale_bits);
       D_801C7750_1C8350=0xA5A5A5A5U;
       memcpy(before_control,&D_8015CC30_15D830,sizeof before_control);
       call_number=0;
       func_8003F37C_3FF7C();
       assert(call_number==3);
       assert(allocator_calls==i+1);
       assert(D_801C7750_1C8350==(u32)(unsigned long)obj);
       assert(obj[0x74]==expected_slot);
       for (size_t j=0;j<sizeof obj;j++) if(j!=0x74) assert(obj[j]==before_obj[j]);
       assert(D_8015CC30_15D830.byte_d8==(u8)(expected_slot+1));
       assert(D_8015CC30_15D830.field_8c==expected_control);
       assert(D_8015CC30_15D830.flags==0x5A5A5A5AU);
       for (size_t j=0;j<sizeof before_control;j++) if(j!=0xD8)
           assert(((u8 *)&D_8015CC30_15D830)[j]==before_control[j]);
       assert(D_801C7740_1C8340==(s32)expected_actor);
    }
    puts("VM setup F37C: 300/300 synthetic host scenarios passed");
    return 0;
}

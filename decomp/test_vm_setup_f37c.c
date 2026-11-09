/* Synthetic C mock calls only; no real game execution or original MIPS run. */
#include <stddef.h>
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include "candidates/vm_setup_f37c.c"

VmControl D_8015CC30_15D830;
u32 D_801C7740_1C8340;
u8 *D_801C7750_1C8350;
float D_8007D108_7DD08;
u8 D_8006D920_6E520[8];
static u8 obj[0x100];
static unsigned call_number;
static u32 expected_control, expected_actor;
static float expected_scale;
static unsigned verify_zero;
_Static_assert(offsetof(VmControl, control)==0x8c, "control field offset");
_Static_assert(offsetof(VmControl, slot)==0xd8, "owner slot offset");
void func_80218F30_5D4400(void) { }
void func_8021925C_5D472C(void) { }
u8 *func_80035690_36290(u32 a0,u32 a1,s32 a2,void *a3,float a4,float a5,float a6,
  s32 a7,s32 a8,s32 a9,float a10,float a11,float a12,s32 a13,s32 a14,s32 a15) {
    assert(call_number++ == 0);
    assert(a0==expected_control && a1==expected_actor && a2==0 && a3==D_8006D920_6E520);
    assert(a4==0.0f && a5==0.0f && a6==0.0f && a7==0 && a8==0 && a9==0);
    assert(a10==expected_scale && a11==expected_scale && a12==expected_scale);
    assert(a13==0 && a14==0 && a15==0);
    verify_zero++;
    return obj;
}
void func_80035244_35E44(u8 *p,void (*callback)(void)) {
    assert(call_number++ == 1);
    assert(p == obj && callback == func_80218F30_5D4400);
}
void func_80035214_35E14(u8 *p,void (*callback)(void)) {
    assert(call_number++ == 2);
    assert(p == obj && callback == func_8021925C_5D472C);
}
static u32 next(u32 *s) {u32 x=*s;x^=x<<13;x^=x>>17;x^=x<<5;*s=x;return x;}
int main(void) {
    u32 state=0x837c237c;
    for(unsigned i=0;i<300;i++){
       memset(obj,0x5A,sizeof obj);
       expected_control=next(&state);expected_actor=next(&state);
       expected_scale=(float)(s32)(next(&state)%200000)-50000.0f;
       if(i==0) expected_scale=0.0f;
       if(i==1) expected_scale=-1.0f;
       if(i==2) expected_scale=0.5f;
       D_8015CC30_15D830.control=expected_control;
       D_8015CC30_15D830.slot=(u8)next(&state);
       const u8 old=D_8015CC30_15D830.slot;
       D_801C7740_1C8340=expected_actor;
       D_8007D108_7DD08=expected_scale;
       D_801C7750_1C8350=NULL;
       call_number=verify_zero=0;
       func_8003F37C_3FF7C();
       assert(call_number==3 && verify_zero==1);
       assert(D_801C7750_1C8350==obj);
       assert(obj[0x74]==old);
       assert(obj[0x73]==0x5A && obj[0x75]==0x5A);
       assert(D_8015CC30_15D830.slot==(u8)(old+1));
    }
    puts("VM setup F37C: 300/300 synthetic host scenarios passed");
    return 0;
}

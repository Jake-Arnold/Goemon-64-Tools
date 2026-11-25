typedef unsigned char u8; typedef unsigned short u16; typedef int s32; typedef float f32;
#define F(p,t,o) (*(t *)((u8 *)(p)+(o)))
typedef struct SpeedRecord { f32 speed; u8 rest[20]; } SpeedRecord;
extern void func_801DABDC_596AEC(void *);
extern void func_801CC4C0_5883D0(void *, f32, f32);
extern void func_801CD084_588F94(void *);
extern void func_801CBBE8_587AF8(void *);
extern void func_801D9C54_595B64(void *);
extern void func_801FB1C0_5B70D0(u16, s32);
extern u8 D_800C7AE0;
extern SpeedRecord D_800C7DBC[];
void func_801CBAF8_587A08(void *arg0, void *arg1) {
    u16 temp_v0;
    void *temp_v0_2;
    if (F(F(arg0,void *,0x5C),u8,0x69) == 0) {
        func_801DABDC_596AEC(arg0);
    }
    if (!(D_800C7AE0 & 3)) {
        func_801CC4C0_5883D0(arg0,F(arg0,f32,0xE4),F(arg0,f32,0xE8));
        temp_v0 = F(arg0,u16,0xCE);
        if (temp_v0 & 0x8000) {
            F(arg0,u16,0x94) = (u16)(temp_v0 & 0x3FF);
        }
        func_801CD084_588F94(arg0);
        func_801CBBE8_587AF8(arg0);
    }
    func_801D9C54_595B64(arg0);
    func_801FB1C0_5B70D0(F(arg0,u16,0x96),F(F(arg0,void *,0x5C),s32,0x7C));
    F(arg0,s32,0x38) = 0;
    F(arg0,s32,0x34) = 0;
    F(F(arg0,void *,0x5C),u16,0x1A) = F(arg0,u16,0x94);
    temp_v0_2 = F(arg0,void *,0x5C);
    F(temp_v0_2,f32,0x28) = F(temp_v0_2,f32,0x24);
    temp_v0_2 = F(arg0,void *,0x5C);
    F(temp_v0_2,f32,0x24) = F(temp_v0_2,f32,0x20);
    F(F(arg0,void *,0x5C),f32,0x20) = D_800C7DBC[F(arg0,u8,0x90)].speed;
}

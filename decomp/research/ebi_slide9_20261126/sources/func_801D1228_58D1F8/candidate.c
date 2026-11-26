typedef unsigned char u8; typedef unsigned short u16; typedef int s32; typedef float f32;
#define F(p,t,o) (*(t *)((u8 *)(p)+(o)))
typedef struct SpeedRecord { f32 speed; u8 rest[20]; } SpeedRecord;
extern void func_801E009C_59C06C(void *);
extern void func_801D1BC0_58DB90(void *, f32, f32);
extern void func_801D2734_58E704(void *);
extern void func_801D1314_58D2E4(void *);
extern void func_801DF134_59B104(void *);
extern void func_802000D0_5BC0A0(u16, s32);
extern u8 g_system[];
void func_801D1228_58D1F8(void *arg0, void *arg1) {
    u16 temp_v0;
    void *temp_v0_2;
    if (F(F(arg0,void *,0x5C),u8,0x69) == 0) {
        func_801E009C_59C06C(arg0);
    }
    if (!(F(g_system,u8,0x3AE20) & 3)) {
        func_801D1BC0_58DB90(arg0,F(arg0,f32,0xE4),F(arg0,f32,0xE8));
        temp_v0 = F(arg0,u16,0xCE);
        if (temp_v0 != 0) {
            F(arg0,u16,0x94) = temp_v0;
        }
        func_801D2734_58E704(arg0);
        func_801D1314_58D2E4(arg0);
    }
    func_801DF134_59B104(arg0);
    func_802000D0_5BC0A0(F(arg0,u16,0x96),F(F(arg0,void *,0x5C),s32,0x7C));
    F(arg0,s32,0x38) = 0;
    F(arg0,s32,0x34) = 0;
    F(F(arg0,void *,0x5C),u16,0x1A) = F(arg0,u16,0x94);
    temp_v0_2 = F(arg0,void *,0x5C);
    F(temp_v0_2,f32,0x28) = F(temp_v0_2,f32,0x24);
    temp_v0_2 = F(arg0,void *,0x5C);
    F(temp_v0_2,f32,0x24) = F(temp_v0_2,f32,0x20);
    F(F(arg0,void *,0x5C),f32,0x20) = ((SpeedRecord *)(g_system+0x3B0FC))[F(arg0,u8,0x90)].speed;
}

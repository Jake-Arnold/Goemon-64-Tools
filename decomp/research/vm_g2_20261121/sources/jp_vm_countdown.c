typedef int s32; typedef unsigned char u8; typedef struct{u8 pad[16];s32 timer;}State;extern State D_801CCF18_1CDB18;extern s32 D_801CCF10_1CDB10;
void func_8003E2C4_3EEC4(void){if(--D_801CCF18_1CDB18.timer<=0){D_801CCF10_1CDB10=0;D_801CCF18_1CDB18.timer=0;}}

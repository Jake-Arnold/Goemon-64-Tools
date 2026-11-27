typedef void (*TransitionHandler)(void); typedef int s32; typedef unsigned char u8; typedef struct { TransitionHandler handler[18]; } TransitionHandlers;
extern TransitionHandlers D_80058908_59508;
extern u8 *D_8015C5C8_15D1C8; extern u8 D_3ADD4[];
void func_80002040_2C40(void) {
struct { TransitionHandlers table; s32 reserved[2]; } local;
local.table = D_80058908_59508;
local.table.handler[*(D_3ADD4+(unsigned int)D_8015C5C8_15D1C8)]();
}

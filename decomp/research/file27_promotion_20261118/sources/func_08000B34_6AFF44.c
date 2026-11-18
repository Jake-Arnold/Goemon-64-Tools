void func_08000BEC_6AFFFC(void*,void*);
void func_08000B90_6AFFA0(void*,void*);
void func_08000B34_6AFF44(void*,void*);
void func_08000AD8_6AFEE8(void*,void*);
void func_08000A7C_6AFE8C(void*,void*);
typedef unsigned int u32;
extern void func_080004FC_6AF90C(void*, u32);
extern char func_80221C0C_5DD0DC;
extern char func_8003521C_35E1C;
extern char func_0800059C_6AF9AC;

void func_08000B34_6AFF44(void* actor, void* ctx) {
    func_080004FC_6AF90C(actor, 0x12800761);
    ((void(*)(void*,u32,u32,u32))&func_80221C0C_5DD0DC)(actor, 0, 0x3E800000, 1);
    ((void(*)(void*))&func_8003521C_35E1C)(&func_0800059C_6AF9AC);
}

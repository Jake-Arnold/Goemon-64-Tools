void func_08000620_6AFA30(void*,void*);
void func_080005C4_6AF9D4(void*,void*);
void func_0800059C_6AF9AC(void*,void*);
extern char func_802213F4_5DC8C4;
typedef unsigned int u32;
extern void func_080004FC_6AF90C(void*, u32);
extern char func_80221C0C_5DD0DC;
extern char func_8003521C_35E1C;

void func_080005C4_6AF9D4(void* actor, void* ctx) {
    func_080004FC_6AF90C(actor, 0x10000661);
    ((void(*)(void*,u32,u32,u32))&func_80221C0C_5DD0DC)(actor, 0, 0x3E800000, 1);
    ((void(*)(void*))&func_8003521C_35E1C)(&func_0800059C_6AF9AC);
}

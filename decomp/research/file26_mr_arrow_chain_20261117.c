typedef unsigned int u32;
typedef unsigned short u16;
extern char func_80221F70_5DD440;
extern char func_8003D310_3DF10;
extern char func_80218DA8_5D4278;
extern char func_8021A22C_5D56FC;
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern char func_8021804C_5D351C;
extern char func_8003F1D8_3FDD8;
extern char func_80221FB0_5DD480;
extern char func_80034ED4_35AD4;
void func_08000174_6AE954(void*, void*);
void func_080001B4_6AE994(void*, void*);

void func_080000CC_6AE8AC(void *actor, void *ctx) {
    if (*(u32 *)((char*)actor + 0x68) & 0x200) {
        ((void (*)(void))&func_80221F70_5DD440)();
        ((void (*)(u32))&func_8003D310_3DF10)(0x6C);
        ((void (*)(void*,u32,u32,u32))&func_80218DA8_5D4278)(actor,0,0,0);
        ((void (*)(void*))&func_8021A22C_5D56FC)(actor);
        ((void (*)(u16))&func_80024038_24C38)(*(u16*)((char*)actor + 0xD0));
        *(u32 *)((char*)actor + 0x60) = 0;
        ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)(func_08000174_6AE954);
    }
}

void func_08000174_6AE954(void *actor, void *ctx) {
    ((void (*)(void*, u32))&func_8021804C_5D351C)(actor, 0);
    ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)(func_080001B4_6AE994);
}

void func_080001B4_6AE994(void *actor, void *ctx) {
    if (((int (*)(void))&func_8003F1D8_3FDD8)() == 0) {
        ((void (*)(void))&func_80221FB0_5DD480)();
        ((void (*)(void))&func_80034ED4_35AD4)();
    }
}

typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
extern char func_8000B824_C424;
extern char func_80024038_24C38;
extern char func_800240DC_24CDC;
extern char func_80034ED4_35AD4;
extern char func_8003521C_35E1C;
extern char func_80038B98_39798;
extern char func_8003D310_3DF10;
extern char func_8003F1D8_3FDD8;
extern char func_801DCD48_598C58;
extern char func_80216E1C_5D22EC;
extern char func_8021804C_5D351C;
extern char func_80218DA8_5D4278;
extern char func_80219E70_5D5340;
extern char func_8021A22C_5D56FC;
extern char func_8021A310_5D57E0;
extern char func_80221F70_5DD440;
extern char func_80221FB0_5DD480;
void func_08000000_6AE7E0(void*, void*);
void func_080000CC_6AE8AC(void*, void*);
void func_08000174_6AE954(void*, void*);
void func_080001B4_6AE994(void*, void*);
void func_08000204_6AE9E4(void*, void*);
void func_080002D0_6AEAB0(void*, void*);
void func_08000378_6AEB58(void*, void*);
void func_08000434_6AEC14(void*, void*);
void func_080004AC_6AEC8C(void*, void*);
void func_08000514_6AECF4(void*, void*);
void func_080005F8_6AEDD8(void*, void*);
void func_080006E0_6AEEC0(void*, void*);
void func_08000740_6AEF20(void*, void*);
void func_0800083C_6AF01C(void*, void*);
void func_08000740_6AEF20(void *actor, void *ctx) {
    u32 saved;
    if (((int (*)(u16))&func_800240DC_24CDC)(*(u16*)((char*)actor + 0xD0))) {
        *(u32*)((char*)actor + 0x68) |= 2;
    } else {
        *(u32*)((char*)actor + 0x60) = 0x4006E0;
        *(u8*)((char*)actor + 0x4C) = 8;
        ((void (*)(void*, u32,u32,u32))&func_80218DA8_5D4278)(actor,500,50,0);
        saved=*(u16*)((char*)actor+0x5E);
        *(u16*)((char*)actor+0x5E)=1;
        ((void (*)(void*,u32))&func_80216E1C_5D22EC)(actor,1);
        *(u16*)((char*)actor+0x5E)=saved;
        ((void (*)(void*,u32,u32))&func_80219E70_5D5340)(actor,8,0);
        ((void (*)(void*))&func_8021A310_5D57E0)(actor);
        *(void**)((char*)actor+0xE4)=((void* (*)(void*,u32))&func_8021804C_5D351C)(actor,0);
        ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)((void (*)(void*,void*))&func_0800083C_6AF01C);
    }
}

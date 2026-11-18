typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;
extern char func_80221F70_5DD440;
extern char func_8003D310_3DF10;
extern char func_80218DA8_5D4278;
extern char func_8021A22C_5D56FC;
extern char func_80024038_24C38;
extern char func_8003521C_35E1C;
extern char func_080004AC_6AEC8C;
void func_080009F4_6AF1D4(void *actor, void *ctx) {
    void *p;
    *(u16*)((char*)ctx+0x16) = (*(u16*)((char*)ctx+0x16)+4)&0x3FF;
    if (*(u32*)((char*)actor + 0x68)&0x200) {
        ((void (*)(void))&func_80221F70_5DD440)();
        ((void (*)(u32))&func_8003D310_3DF10)(0x64);
        ((void (*)(void*,u32,u32,u32))&func_80218DA8_5D4278)(actor,0,0,0);
        ((void (*)(void*))&func_8021A22C_5D56FC)(actor);
        *(u32*)((char*)actor + 0x60)=0;
        ((void (*)(u16))&func_80024038_24C38)(*(u16*)((char*)actor+0xD0));
        p=*(void**)((char*)actor+0xE4);
        if (p) *(u8*)((char*)p+0xD0)=1;
        ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)((void (*)(void*,void*))&func_080004AC_6AEC8C);
    }
}

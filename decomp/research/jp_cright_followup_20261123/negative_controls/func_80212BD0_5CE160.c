typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
extern u8 D_80162420[];
extern u32 D_8020151C;
extern u32 D_80201514;
extern void func_8021E024_5D95B4(int);
extern void func_80212090_5CD620(void*);
void func_80212BD0_5CE160(void *a0, void *a1) {
    u8 *p = D_80162420;
    *(u32*)(p + 0xC8) = *(u32*)(p + 0xC4);
    *(u16*)(p + 0) += 1;
    *(u32*)(p + 0xC4) = 0;
    func_8021E024_5D95B4(10);
    if (D_8020151C != 0) {
        *(u32*)(p + 0x130) = D_8020151C;
        *(u32*)(p + 0x12C) = D_80201514;
    }
    if (*(u32*)(p + 0x38) != 0) {
        func_80212090_5CD620(a0);
    }
}

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u16 count; u8 pad0[0x36]; u32 present; u8 pad1[0x88]; u32 pending; u32 previous; u8 pad2[0x60]; u32 saved1; u32 saved2;} Stage;
extern Stage D_80162420_163020;
extern u32 D_8020151C_5BD4EC;
extern u32 D_80201514_5BD4E4;
extern void func_8021E024_5D95B4(int);
extern void func_80212090_5CD620(void*);
void func_80212BD0_5CE160(void *a0, void *a1) {
    D_80162420_163020.previous = D_80162420_163020.pending;
    D_80162420_163020.pending = 0;
    D_80162420_163020.count++;
    func_8021E024_5D95B4(10);
    if (D_8020151C_5BD4EC != 0) {
        D_80162420_163020.saved2 = D_8020151C_5BD4EC;
        D_80162420_163020.saved1 = D_80201514_5BD4E4;
    }
    if (D_80162420_163020.present != 0) func_80212090_5CD620(a0);
}

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct {u16 count; u8 pad0[0x36]; u32 present; u8 pad1[0x88]; u32 pending; u32 previous; u8 pad2[0x60]; u32 saved1; u32 saved2;} Stage;
extern Stage D_8015CC30_15D830;
extern u32 D_801FC60C_5B851C;
extern u32 D_801FC604_5B8514;
extern void func_802192B4_5D4784(int);
extern void func_8020D2A0_5C8770(void*);
void func_8020DD78_5C9248(void *a0, void *a1) {
    D_8015CC30_15D830.previous = D_8015CC30_15D830.pending;
    D_8015CC30_15D830.pending = 0;
    D_8015CC30_15D830.count++;
    func_802192B4_5D4784(10);
    if (D_801FC60C_5B851C != 0) {
        D_8015CC30_15D830.saved2 = D_801FC60C_5B851C;
        D_8015CC30_15D830.saved1 = D_801FC604_5B8514;
    }
    if (D_8015CC30_15D830.present != 0) func_8020D2A0_5C8770(a0);
}

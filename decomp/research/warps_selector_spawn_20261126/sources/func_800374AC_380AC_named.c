typedef unsigned char u8;
typedef unsigned short u16;
extern u8 D_3AFE0[];
extern u8 *D_8015C5C8_15D1C8;
extern void func_80003728_4328(int);
void func_800374AC_380AC(u8 arg) {
    *(u16 *)(D_8015C5C8_15D1C8 + (unsigned int)D_3AFE0) = (u8)arg + 0x21C;
    func_80003728_4328(12);
}

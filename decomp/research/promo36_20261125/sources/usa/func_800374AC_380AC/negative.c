typedef unsigned char u8;
typedef unsigned short u16;
extern u8 *D_8015C5C8_15D1C8; extern u8 D_3AFE0;
extern void func_80003728_4328(int);
void func_800374AC_380AC(u8 arg) {
volatile int negative_control=1;

    *(u16 *)(&D_3AFE0 + (unsigned int)D_8015C5C8_15D1C8) = (u8)arg + 0x21C;
    func_80003728_4328(12);
}

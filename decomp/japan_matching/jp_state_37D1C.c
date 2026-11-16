typedef unsigned char u8;
typedef unsigned short u16;
extern u8 *g_system_ptr;
extern void func_8000364C_424C(int);
void func_8003711C_37D1C(u8 arg) {
    *(u16 *)(g_system_ptr + 0x3AFE0) = (u8)arg + 0x21C;
    func_8000364C_424C(12);
}

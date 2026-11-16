typedef unsigned char u8;
typedef unsigned short u16;
extern u8 *g_system_ptr;
extern void func_8000364C_424C(int);
void func_8003704C_37C4C(void) {
    *(u16 *)(g_system_ptr + 0x3AFE0) = 0x240;
    func_8000364C_424C(12);
}

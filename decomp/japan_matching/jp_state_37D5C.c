typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Sys { u8 a[0x3ADF2]; u16 current; u8 b[0x1EC]; u16 next; } Sys;
extern Sys *g_system_ptr;
extern int func_8000B3E4_BFE4(void);
extern void func_8000364C_424C(int);
void func_8003715C_37D5C(void) {
    if (func_8000B3E4_BFE4() == 0) {
        func_8000364C_424C(14);
    } else {
        g_system_ptr->next = g_system_ptr->current;
        func_8000364C_424C(12);
    }
}

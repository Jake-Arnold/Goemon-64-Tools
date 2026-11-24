typedef unsigned short u16;
typedef void (*Callback)(void);
typedef struct {char pad[0x18]; Callback callback;} Descriptor;
typedef struct {char pad[0x2df2]; u16 index; char pad1[0x248]; Callback callback;} State;
extern char *g_system_ptr;
extern Descriptor *D_80235FE8_5F1578[];
extern char D_3B03C[];
void func_802124AC_5CDA3C(void) {
    Descriptor *d = D_80235FE8_5F1578[((State *)(g_system_ptr + 0x38000))->index];
    *(Callback *)(g_system_ptr + (unsigned int)D_3B03C) = d->callback;
    ((State *)(g_system_ptr + 0x38000))->callback();
}

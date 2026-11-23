typedef unsigned short u16;
typedef void (*Callback)(void);
typedef struct {char pad[0x18]; Callback callback;} Descriptor;
typedef struct {char pad[0x2df2]; u16 index; char pad1[0x248]; Callback callback;} State;
extern char *D_8015C5C8_15D1C8;
extern Descriptor *D_80231300_5EC7D0[];
extern char D_3B03C[];
void func_8020D6BC_5C8B8C(void) {
    Descriptor *d = D_80231300_5EC7D0[((State *)(D_8015C5C8_15D1C8 + 0x38000))->index];
    *(Callback *)(D_8015C5C8_15D1C8 + (unsigned int)D_3B03C) = d->callback;
    ((State *)(D_8015C5C8_15D1C8 + 0x38000))->callback();
}

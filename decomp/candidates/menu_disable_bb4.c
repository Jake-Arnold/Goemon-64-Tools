typedef unsigned char u8;
typedef unsigned short u16;
typedef struct {u8 pad[0x22];u16 flags;} MenuPanel;
typedef struct {u8 pad[4];u8 bit;u8 reserved[0x5F];u8 marker;} MenuOptions;
extern MenuPanel *D_801FC624_5B8534;
extern MenuOptions *D_801FC628_5B8538;
void func_80011BB4_127B4(void) {
    if(D_801FC624_5B8534 && D_801FC628_5B8538) {
        D_801FC624_5B8534->flags &= (u16)~0x14;
        D_801FC628_5B8538->marker = 0;
        D_801FC628_5B8538->bit &= 0xFF7F;
    }
}

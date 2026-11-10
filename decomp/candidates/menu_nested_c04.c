typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 pad[0x22]; u16 flags;} MenuPanel;
typedef struct { u8 pad[4]; u8 bit; } MenuBit;
typedef struct {u8 pad[0x18]; MenuBit *linked;} MenuPanelExt;
extern u8 *D_8015C5C8_15D1C8;
void func_80011C04_12804(void) {
    MenuPanel *panel = *(MenuPanel **)(D_8015C5C8_15D1C8 + 0xC8000 + 0x78E8);
    if (panel) {
        panel->flags |= 0x14;
        (*(MenuPanelExt **)(D_8015C5C8_15D1C8 + 0xC8000 + 0x78E8))->linked->bit |= 0x80;
    }
}

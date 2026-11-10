/* Research only. Entire empty_menu_hook.c unit, 0x12758..0x12858. */
typedef signed int s32;
typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 pad[0x22]; u16 flags; } MenuPanel;
typedef struct { u8 pad[4]; u8 bit; u8 reserved[0x5F]; u8 marker; } MenuOptions;
typedef struct { u8 pad[4]; u8 bit; } MenuBit;
typedef struct { u8 pad[0x18]; MenuBit *linked; } MenuPanelExt;
extern MenuPanel *D_801FC624_5B8534;
extern MenuOptions *D_801FC628_5B8538;
extern u8 *D_8015C5C8_15D1C8;
void func_80011B58_12758(s32 arg0) {}
void func_80011B60_12760(void) {
    if (D_801FC624_5B8534 && D_801FC628_5B8538) {
        D_801FC624_5B8534->flags |= 0x14;
        D_801FC628_5B8538->marker = 1;
        D_801FC628_5B8538->bit |= 0x80;
    }
}
void func_80011BB4_127B4(void) {
    if (D_801FC624_5B8534 && D_801FC628_5B8538) {
        D_801FC624_5B8534->flags &= (u16)~0x14;
        D_801FC628_5B8538->marker = 0;
        D_801FC628_5B8538->bit &= 0xFF7F;
    }
}
void func_80011C04_12804(void) {
    MenuPanel *panel = *(MenuPanel **)(D_8015C5C8_15D1C8 + 0xC8000 + 0x78E8);
    if (panel) {
        panel->flags |= 0x14;
        (*(MenuPanelExt **)(D_8015C5C8_15D1C8 + 0xC8000 + 0x78E8))->linked->bit |= 0x80;
    }
}

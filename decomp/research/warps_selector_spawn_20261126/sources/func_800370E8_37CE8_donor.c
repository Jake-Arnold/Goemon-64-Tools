typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef struct { u8 pad[8]; float x, y, z; } PlayerCoords;
typedef struct { u8 pad[0x94]; u16 area; } Actor;
typedef struct { u8 pad[0x3AFEE]; s16 x, y, z; u16 area; } Sys;
extern PlayerCoords *D_801FC60C_5B851C;
extern Actor *D_801FC604_5B8514;
extern Sys *D_8015C5C8_15D1C8;
extern void func_801FA4FC_5B640C(int, int, int, int, int, int);
void func_800370E8_37CE8(void) {
    D_8015C5C8_15D1C8->x = (s32)D_801FC60C_5B851C->x;
    D_8015C5C8_15D1C8->y = (s32)D_801FC60C_5B851C->y;
    D_8015C5C8_15D1C8->z = (s32)D_801FC60C_5B851C->z;
    D_8015C5C8_15D1C8->area = D_801FC604_5B8514->area;
    func_801FA4FC_5B640C(0x1E0, 0, 0x19, 0, 0, 1);
}

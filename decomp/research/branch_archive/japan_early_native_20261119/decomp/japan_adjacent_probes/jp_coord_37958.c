typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef struct { u8 pad[8]; float x, y, z; } PlayerCoords;
typedef struct { u8 pad[0x94]; u16 area; } Actor;
typedef struct { u8 pad[0x3AFEE]; s16 x, y, z; u16 area; } Sys;
extern PlayerCoords *D_8020151C_5BD4EC;
extern Actor *D_80201514_5BD4E4;
extern Sys *g_system_ptr;
extern void func_801FF40C_5BB3DC(int, int, int, int, int, int);
void func_80036D58_37958(void) {
    g_system_ptr->x = (s32)D_8020151C_5BD4EC->x;
    g_system_ptr->y = (s32)D_8020151C_5BD4EC->y;
    g_system_ptr->z = (s32)D_8020151C_5BD4EC->z;
    g_system_ptr->area = D_80201514_5BD4E4->area;
    func_801FF40C_5BB3DC(0x1E0, 0, 0x19, 0, 0, 1);
}

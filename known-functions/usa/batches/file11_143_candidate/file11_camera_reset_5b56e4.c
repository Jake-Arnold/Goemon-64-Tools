typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 pad[0xAE40]; u16 mode; u8 pad2[2]; u32 x,y,z; } ROOT;
extern ROOT D_800BCCC0_BD8C0;
extern u8 D_8008CCC0_8D8C0[];
void func_801F97D4_5B56E4(void) {
  int i;
  u8 *p;
  D_800BCCC0_BD8C0.mode = 0;
  D_800BCCC0_BD8C0.x = 0;
  D_800BCCC0_BD8C0.y = 0;
  D_800BCCC0_BD8C0.z = 0;
  for(i = 0; i < 10; ) {
    p = (u8 *)D_8008CCC0_8D8C0 + i*0x28 + 0x38000;
    i = (u16)(i+1);
    *(u16 *)(p+0x2E50) = 0;
    *(u32 *)(p+0x2E54) = 0;
    *(u32 *)(p+0x2E5C) = 0;
    *(u32 *)(p+0x2E64) = 0;
    *(u32 *)(p+0x2E58) = 0;
    *(u32 *)(p+0x2E60) = 0;
    *(u32 *)(p+0x2E68) = 0;
    *(u32 *)(p+0x2E6C) = 0;
    *(u32 *)(p+0x2E70) = 0;
    *(u32 *)(p+0x2E74) = 0;
  }
}

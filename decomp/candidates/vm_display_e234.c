/* Research-only VM display-list emitter func_8003E234_3EE34 (440-byte original). */
typedef unsigned int u32;
#ifdef GOEMON_VM_DISPLAY_HOST_TEST
#include <stdint.h>
#define VM_ADDR(p) ((u32)(uintptr_t)(p))
#else
#define VM_ADDR(p) ((u32)(p))
#endif
typedef unsigned char u8;
extern u32 *D_8015C5CC_15D1CC;
extern u8 D_800777F0_783F0[];
extern u8 D_80077150_77D50[];
extern u32 D_801C78D8_1C84D8;
extern u32 D_801C78DC_1C84DC;
extern u8 *D_80077860_78460;
#define OUT(a,b) do { u32 *p = *cursor; *cursor = p + 2; p[0]=(a); p[1]=(b); } while(0)
void func_8003E234_3EE34(void) {
  u32 **cursor=&D_8015C5CC_15D1CC;
  OUT(0x06000000, VM_ADDR(D_800777F0_783F0));
  OUT(0xFD100000, VM_ADDR(D_80077150_77D50));
  OUT(0xF5100000, 0x07000000);
  OUT(0xE6000000, 0);
  OUT(0xF3000000, 0x071FF100);
  OUT(0xE7000000, 0);
  OUT(0xF5101000, 0);
  OUT(0xF2000000, 0x0007C03C);
  OUT(0xE4000000 | (((((D_801C78D8_1C84D8 + 15)<<2)&0xFFF)<<12) | (((D_801C78DC_1C84DC + 15)<<2)&0xFFF)),
      (((D_801C78D8_1C84D8 <<2)&0xFFF)<<12) | ((D_801C78DC_1C84DC<<2)&0xFFF));
  OUT(0xB4000000, (D_80077860_78460[0x5D] & 1)<<25);
  OUT(0xB3000000, 0x10000400);
}

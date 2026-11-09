/* Research-only VM display-list emitter func_8003EBAC_3F7AC (436-byte original). */
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
extern u8 D_80076148_76D48[];
extern u8 *D_80077860_78460;
#define OUT(a,b) do { u32 *p = *cursor; *cursor = p + 2; p[0]=(a); p[1]=(b); } while(0)
void func_8003EBAC_3F7AC(u32 x, u32 y) {
  u32 **cursor=&D_8015C5CC_15D1CC;
  OUT(0x06000000, VM_ADDR(D_800777F0_783F0));
  OUT(0xFD100000, VM_ADDR(D_80076148_76D48));
  OUT(0xF5100000, 0x07000000);
  OUT(0xE6000000, 0);
  OUT(0xF3000000, 0x077FF100);
  OUT(0xE7000000, 0);
  OUT(0xF5101000, 0);
  OUT(0xF2000000, 0x0007C0FC);
  OUT(0xE4000000 | (((((x + 15)<<2)&0xFFF)<<12) | (((y-2+15)<<2)&0xFFF)),
      (((x <<2)&0xFFF)<<12) | (((y-2)<<2)&0xFFF));
  { u32 flags = D_80077860_78460[0x5C];
    OUT(0xB4000000, ((flags & 3)<<9) | ((flags & 4)<<23)); }
  OUT(0xB3000000, 0x10000400);
}

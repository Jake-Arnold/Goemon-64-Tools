#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>

typedef unsigned char u8;
typedef unsigned short u16;
typedef struct { u8 unknown_00[0x18]; u16 value_18; } JPHalfwordState;
void func_80219328_6A0A28(int unused, JPHalfwordState *state);
void func_80222F18_68C608(int unused, JPHalfwordState *state);

int main(void) {
  assert(offsetof(JPHalfwordState, value_18) == 0x18);
  for (unsigned int i=0; i<=65535; ++i) {
     JPHalfwordState a = {{0}, (u16)i};
     JPHalfwordState b = {{0}, (u16)i};
     func_80219328_6A0A28(0,&a);
     func_80222F18_68C608(0,&b);
     assert(a.value_18 == ((i-2)&0x3FF));
     assert(b.value_18 == ((i-4)&0x3FF));
  }
  puts("PASS 65,536 values x two C functions");
  return 0;
}

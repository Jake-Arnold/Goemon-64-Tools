#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef void (*callback)(void *, unsigned char *);
extern void func_801CBE68_668598(void *, unsigned char *);
extern void func_801CC1FC_66892C(void *, unsigned char *);
extern void func_801CC20C_66893C(void *, unsigned char *);
extern void func_801CC21C_66894C(void *, unsigned char *);
extern void func_801CC22C_66895C(void *, unsigned char *);
extern void func_8020D734_69D974(void *, unsigned char *);
extern void func_8020D744_69D984(void *, unsigned char *);
extern void func_8020D754_69D994(void *, unsigned char *);
extern void func_8020D764_69D9A4(void *, unsigned char *);
extern void func_8020D770_69D9B0(void *, unsigned char *);
struct Test { const char *name; callback call; uint8_t expected; };
int main(void) {
  const struct Test cases[] = {
    {"file16 668598", func_801CBE68_668598, 7},
    {"file16 66892C", func_801CC1FC_66892C, 8},
    {"file16 66893C", func_801CC20C_66893C, 2},
    {"file16 66894C", func_801CC21C_66894C, 8},
    {"file16 66895C", func_801CC22C_66895C, 2},
    {"file21 69D974", func_8020D734_69D974, 6},
    {"file21 69D984", func_8020D744_69D984, 1},
    {"file21 69D994", func_8020D754_69D994, 7},
    {"file21 69D9A4", func_8020D764_69D9A4, 0},
    {"file21 69D9B0", func_8020D770_69D9B0, 0},
  };
  for (unsigned i=0; i<sizeof(cases)/sizeof(*cases); i++) {
    for (unsigned init=0; init<=255; init+=51) {
      uint8_t data[16], before[16];
      memset(data,(int)init,sizeof(data)); memcpy(before,data,sizeof(before));
      cases[i].call((void *)(uintptr_t)0x13579, data);
      for (unsigned j=0; j<sizeof(data); j++)
        assert(data[j] == (j == 5 ? cases[i].expected : before[j]));
      cases[i].call((void *)(uintptr_t)0, data);
      assert(data[5] == cases[i].expected);
      for (unsigned j=0; j<sizeof(data); j++)
        assert(data[j] == (j == 5 ? cases[i].expected : before[j]));
    }
  }
  puts("PASS: 10 original-address callback states, 120 calls, unchanged adjacent bytes");
  return 0;
}

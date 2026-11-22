#ifndef GOEMON_ISOLATED_MAIN_HOST_COMMON_H
#define GOEMON_ISOLATED_MAIN_HOST_COMMON_H
#include <stdint.h>
typedef uint8_t u8;
typedef int16_t s16;
typedef int32_t s32;
typedef struct { u8 bytes[0xC0000 + 12 * 0x374 + 0x3706]; } SYS_W;
extern SYS_W D_8008CCC0_8D8C0;
#endif

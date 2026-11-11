#include "common.h"

extern u32 D_800573D8_57FD8[];

u32 func_80001D94_2994(u16 arg0) {
    return (D_800573D8_57FD8[arg0] & 0x7FFFFFFF) & 0x7FFFFFFF;
}

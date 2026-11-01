#include "goemon_checkpoint.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

static uint8_t mem[0x800000];
static int in_range(uint32_t addr, uint32_t length) {
    return addr >= 0x80000000u && addr <= 0x807FFFFFu &&
           length <= 0x800000u - (addr & 0x7FFFFFu);
}
static int read_bytes(void *ctx, uint32_t addr, void *dst, uint32_t length) {
    (void)ctx;
    if (!in_range(addr, length)) return -1;
    memcpy(dst, &mem[addr & 0x7FFFFFu], length);
    return 0;
}
static int write_bytes(void *ctx, uint32_t addr, const void *src, uint32_t length) {
    (void)ctx;
    if (!in_range(addr, length)) return -1;
    memcpy(&mem[addr & 0x7FFFFFu], src, length);
    return 0;
}
static void put8(uint32_t addr, uint8_t v) { mem[addr & 0x7FFFFFu] = v; }
static void put32(uint32_t addr, uint32_t v) {
    put8(addr, (uint8_t)(v >> 24)); put8(addr+1, (uint8_t)(v >> 16));
    put8(addr+2, (uint8_t)(v >> 8)); put8(addr+3, (uint8_t)v);
}
int main(void) {
    const GoemonCheckpointIO io = {NULL, read_bytes, write_bytes};
    GoemonCheckpoint cp;
    uint8_t cp_flags[2] = {0xFA, 0x77};
    put8(0x800C7A94, 13); put8(0x800C7A9E, 1);
    put8(0x800C7AB2, 0); put8(0x800C7AB3, 12);
    put32(0x8015C5DC, 0); put32(0x801FC60C, 0x801A0000);
    put32(0x8015C5E0, 10); put32(0x8015C5E4, 8);
    put32(0x8015C5E8, 100); put32(0x8015C5EC, 3);
    put8(0x8015C608, cp_flags[0]); put8(0x8015C609, cp_flags[1]);
    assert(goemon_cp_capture(&io, &cp) == 0);
    put32(0x8015C5E8, 42); put8(0x8015C608, 0);
    assert(goemon_cp_restore(&io, &cp) == 0);
    assert(mem[0x15C5E8] == 0 && mem[0x15C5EB] == 100);
    assert(mem[0x15C608] == 0xFA && mem[0x15C609] == 0x77);
    assert(mem[0x15C910] == 0xFA && mem[0x15C911] == 0x77);
    put8(0x800C7AB3, 13);
    assert(goemon_cp_restore(&io, &cp) == -2);
    puts("portable checkpoint core passed simulated guest-memory tests");
    return 0;
}

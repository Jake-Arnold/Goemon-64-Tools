#include "goemon_watch.h"
#include <string.h>

static int byte_at(const GoemonCheckpointIO *io, uint32_t addr, uint8_t *out) {
    return io->read(io->context, addr, out, 1);
}
static int big_u32(const GoemonCheckpointIO *io, uint32_t addr, uint32_t *out) {
    uint8_t b[4];
    if (io->read(io->context, addr, b, 4)) return -1;
    *out = ((uint32_t)b[0]<<24) | ((uint32_t)b[1]<<16) | ((uint32_t)b[2]<<8) | b[3];
    return 0;
}
static int big_u16(const GoemonCheckpointIO *io, uint32_t addr, uint16_t *out) {
    uint8_t b[2];
    if (io->read(io->context, addr, b, 2)) return -1;
    *out = (uint16_t)(((uint16_t)b[0]<<8) | b[1]);
    return 0;
}
int goemon_watch_read(const GoemonCheckpointIO *io, GoemonWatch *out) {
    if (!io || !io->read || !out) return -1;
    memset(out,0,sizeof(*out));
    if (big_u32(io,0x8015C5DC,&out->character) ||
        big_u32(io,0x8015C5E0,&out->max_hp) ||
        big_u32(io,0x8015C5E4,&out->current_hp) ||
        big_u32(io,0x8015C5E8,&out->ryo) ||
        big_u32(io,0x8015C5EC,&out->lives) ||
        big_u16(io,0x800C7AB2,&out->map_id) ||
        byte_at(io,0x800C7A94,&out->top_state) ||
        byte_at(io,0x800C7A9E,&out->phase) ||
        byte_at(io,0x8015C5D4,&out->loading)) return -2;
    {
        const uint32_t items[]={0x8015C5F3,0x8015C5F7,0x8015C5FF};
        const uint32_t party[]={0x8015C69F,0x8015C6A3,0x8015C6A7,0x8015C6AB};
        const uint32_t weapons[]={0x8015C6AF,0x8015C6B3,0x8015C6B7,0x8015C6BB};
        const uint32_t abilities[]={0x8015C6BF,0x8015C6C3,0x8015C6C7,0x8015C6CB};
        uint32_t i;
        for(i=0;i<3;i++) if(byte_at(io,items[i],&out->item_slots[i])) return -3;
        for(i=0;i<4;i++) {
            if(byte_at(io,party[i],&out->party[i]) ||
               byte_at(io,weapons[i],&out->weapon_upgrades[i]) ||
               byte_at(io,abilities[i],&out->optional_items[i]))return -3;
        }
    }
    if(out->character>3)out->warnings|=1u;
    if(out->max_hp==0 || out->max_hp>127 || out->current_hp>out->max_hp)out->warnings|=2u;
    if(out->ryo>9999)out->warnings|=4u;
    if(out->lives>99)out->warnings|=8u;
    return 0;
}

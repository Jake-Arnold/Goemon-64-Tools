#ifndef GOEMON_JP_ACTOR_FIELDS_H
#define GOEMON_JP_ACTOR_FIELDS_H
/* Observed offsets only; names deliberately avoid unproven gameplay semantics.
 * The native target uses SGI IDO 5.3, MIPS o32, big-endian. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef struct {
    u8 pad00[0x18];
    u64 field18;
    u8 pad20[0x04];
    u32 field24;
    u8 pad28[0x1C];
    float field44;
    u8 pad48[0x1C];
    u16 field64;
    u16 field66;
    u16 field68;
    u16 field6A;
    u8 pad6C[0x04];
    u16 field70;
    u8 pad72[0x0E];
    float field80;
    float field84;
    float field88;
} JPActorObserved;
extern JPActorObserved *D_8016D430_16E030[];
#endif

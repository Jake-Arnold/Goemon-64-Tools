#ifndef GOEMON_SAVE_RESOURCES_H
#define GOEMON_SAVE_RESOURCES_H
#include "common.h"

typedef struct {
    s32 word_00, word_04, max_health, health, ryo, lives;
    u8 unknown_18[0x14];
    s32 word_2C;
} ResourceBlock;

typedef struct {
    u8 flags[0x64];
    ResourceBlock resources;
    s32 word_94, word_98;
    u8 unknown_9C[0x28];
    s32 word_C4;
    u8 unknown_C8[0x34];
    s32 fortune_doll_progress;
    s32 fortune_dolls_total;
    u8 unknown_104[0xFC];
    s32 word_200;
    u16 half_204;
    u8 byte_206, byte_207;
    u16 half_208;
    s16 half_20A, half_20C, half_20E, half_210;
    u8 unknown_212[0x52];
    s32 word_264;
    u8 unknown_268[0x34];
    s32 word_29C, word_2A0;
    u8 unknown_2A4[0x60];
} SaveData;

typedef struct { u16 half_00, half_02, half_04, half_06, half_08, half_0A; } SpawnRecord;
typedef struct { u8 unknown[0xADCC]; u16 ticks; } TimerView;

extern SaveData D_8015C608_15D208;
extern SaveData D_8015C910_15D510;
extern ResourceBlock D_8015C5D8_15D1D8;
extern ResourceBlock D_8015C66C_15D26C;
extern s32 D_8015C698_15D298;
extern const SpawnRecord D_8005BA30_5C630[];
extern TimerView D_800BCCC0_BD8C0;
extern s32 D_80167C48_168848[];
extern s32 D_80167C54_168854;
void func_800041E0_4DE0(u8 *, s32);
void func_80004208_4E08(u8 *, u8 *, s32);
void func_8000B8F0_C4F0(s32);

#endif

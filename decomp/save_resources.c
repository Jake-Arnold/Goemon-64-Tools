/* Matching US save/live/shadow buffer routines, ROM 0xC1D0. */
#include "save_resources.h"

void func_8000B5D0_C1D0(void) {
    D_8015C5C8_15D1C8->unk_cf8a0 = 0;
    D_8015C698_15D298 = 1;
    func_80004208_4E08((u8 *)&D_8015C66C_15D26C, (u8 *)&D_8015C5D8_15D1D8, 0x30);
    func_80004208_4E08((u8 *)&D_8015C608_15D208, (u8 *)&D_8015C910_15D510, 0x304);
    D_8015C5D8_15D1D8.word_00 = 1;
}

void func_8000B640_C240(void) {
    func_800041E0_4DE0((u8 *)&D_8015C608_15D208, 0x304);
    D_8015C608_15D208.resources.word_00 = 1;
    D_8015C608_15D208.resources.lives = 3;
    D_8015C608_15D208.resources.health = 10;
    D_8015C608_15D208.resources.max_health = 10;
    D_8015C608_15D208.resources.ryo = 100;
    D_8015C608_15D208.resources.word_2C = 1;
    D_8015C608_15D208.word_94 = 1;
    D_8015C608_15D208.word_98 = 1;
    D_8015C608_15D208.word_C4 = 1;
    D_8015C608_15D208.byte_206 = 2;
    D_8015C608_15D208.half_204 = 0x1D1;
    D_8015C608_15D208.half_20A = -2;
    D_8015C608_15D208.half_20C = -0x28;
    D_8015C608_15D208.half_20E = 8;
    D_8015C608_15D208.half_210 = 0;
    func_80004208_4E08((u8 *)&D_8015C608_15D208, (u8 *)&D_8015C910_15D510, 0x304);
}

void func_8000B6E0_C2E0(void) {
    func_80004208_4E08((u8 *)&D_8015C910_15D510, (u8 *)&D_8015C608_15D208, 0x304);
    func_8000B5D0_C1D0();
}

void func_8000B718_C318(void)
{
  const SpawnRecord *record;
  record = &D_8005BA30_5C630[D_8015C608_15D208.word_200];
  D_8015C608_15D208.half_204 = (u16) (&D_8005BA30_5C630[D_8015C608_15D208.word_200])->half_00;
  D_8015C608_15D208.half_20A = (u16) (&D_8005BA30_5C630[D_8015C608_15D208.word_200])->half_02;
  D_8015C608_15D208.half_20C = (u16) (&D_8005BA30_5C630[D_8015C608_15D208.word_200])->half_04;
  D_8015C608_15D208.half_20E = (u16) (&D_8005BA30_5C630[D_8015C608_15D208.word_200])->half_06;
  D_8015C608_15D208.half_210 = (u16) (&D_8005BA30_5C630[D_8015C608_15D208.word_200])->half_08;
  D_8015C608_15D208.half_208 = (u16) record->half_0A;
  func_80004208_4E08((u8 *) (&D_8015C5D8_15D1D8), (u8 *) (&D_8015C66C_15D26C), 0x30);
  if (D_8015C608_15D208.resources.lives < 3)
  {
    D_8015C608_15D208.resources.lives = 3;
  }
  if (D_8015C608_15D208.resources.health < 10)
  {
    D_8015C608_15D208.resources.health = 10;
  }
  func_80004208_4E08((u8 *) (&D_8015C608_15D208), (u8 *) (&D_8015C910_15D510), 0x304);
}


void func_8000B7E4_C3E4(void) {
    if (D_800BCCC0_BD8C0.ticks >= 60) {
        D_800BCCC0_BD8C0.ticks -= 60;
        D_8015C608_15D208.word_264++;
    }
}

void func_8000B824_C424(void) {
    if (D_8015C608_15D208.word_FC >= 4) {
        D_8015C608_15D208.word_FC -= 4;
        D_8015C5D8_15D1D8.max_health += 2;
        D_8015C5D8_15D1D8.health = D_8015C5D8_15D1D8.max_health;
    }
}

void func_8000B864_C464(void) {
    D_8015C608_15D208.word_29C = 400;
    D_8015C608_15D208.word_2A0 = 200;
}

void func_8000B880_C480(void) {
    s32 index;
    for (index = 0; index < 3; index++) D_80167C48_168848[index] = 0;
}

void func_8000B8A4_C4A4(s32 value) {
    D_80167C54_168854 = value;
}

void func_8000B8B0_C4B0(void) {
    s32 index;
    for (index = 0; index < 3; index++) func_8000B8F0_C4F0(index);
}

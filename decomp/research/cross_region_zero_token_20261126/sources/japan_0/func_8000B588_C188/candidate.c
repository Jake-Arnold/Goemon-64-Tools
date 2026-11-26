/* Matching US save/live/shadow buffer routines, ROM 0xC1D0. */
#include "save_resources.h"

void func_8000B588_C188(void)
{
  const SpawnRecord *record;
  record = &D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200];
  D_80161DF8_1629F8.half_204 = (u16) (&D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200])->half_00;
  D_80161DF8_1629F8.half_20A = (u16) (&D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200])->half_02;
  D_80161DF8_1629F8.half_20C = (u16) (&D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200])->half_04;
  D_80161DF8_1629F8.half_20E = (u16) (&D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200])->half_06;
  D_80161DF8_1629F8.half_210 = (u16) (&D_8005BCB0_5C8B0[D_80161DF8_1629F8.word_200])->half_08;
  D_80161DF8_1629F8.half_208 = (u16) record->half_0A;
  func_80004138_4D38((u8 *) (&D_80161DC8_1629C8), (u8 *) (&D_80161E5C_162A5C), 0x30);
  if (D_80161DF8_1629F8.resources.lives < 3)
  {
    D_80161DF8_1629F8.resources.lives = 3;
  }
  if (D_80161DF8_1629F8.resources.health < 10)
  {
    D_80161DF8_1629F8.resources.health = 10;
  }
  func_80004138_4D38((u8 *) (&D_80161DF8_1629F8), (u8 *) (&D_80162100_162D00), 0x304);
}

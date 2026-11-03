/* Three original one-byte state setters, ROM 0x37C60..0x37C8F.
 * Reconstructed engine code only; not a toolkit warp API.
 * Retain numeric names until all consumers establish the state's semantics.
 */
#include "common.h"

extern s8 D_800C7A95_C8695;

void func_80037060_37C60(void) { D_800C7A95_C8695 = 2; }
void func_80037070_37C70(void) { D_800C7A95_C8695 = 1; }
void func_80037080_37C80(void) { D_800C7A95_C8695 = 3; }

#include "common.h"
void func_8000A5C4_B1C4(void*);
void func_8000A548_B148(s32 start,s32 end) {
 s32 i;
 u8* p=(u8*)&D_8008CCC0_8D8C0+0xBBB90+start*0x98;
 for(i=start;i<end+1;i++) {
 func_8000A5C4_B1C4(p);
 p+=0x98;
 }
}

#include "common.h"
typedef struct { u32 words[38]; } A5C4Struct;
extern A5C4Struct D_8005BBF4_5C7F4;
void func_8000A474_B074(void *arg0) {
    A5C4Struct *p = arg0;
    u32 old_word0 = p->words[0];
    *p = D_8005BBF4_5C7F4;
    p->words[0] = old_word0;
}

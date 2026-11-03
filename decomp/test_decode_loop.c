#include <assert.h>
#include "common.h"
static int index_; static int values[5]; static int args[5];
s32 func_80014CC4_158C4(s32 n) { args[index_]=n; return values[index_++]; }
s32 func_80015EFC_16AFC(void);
int main(void) { values[0]=0; values[1]=3; assert(func_80015EFC_16AFC()==4); assert(index_==2 && args[0]==1 && args[1]==1); index_=0; values[0]=1; values[1]=1; values[2]=0; values[3]=4; assert(func_80015EFC_16AFC()==11); assert(index_==4 && args[0]==1 && args[1]==1 && args[2]==1 && args[3]==3); return 0; }

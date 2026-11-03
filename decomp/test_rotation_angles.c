#include <assert.h>
#include "common.h"
void func_8001F878_20478(u16 *,u16 *,u16 *);
int main(void) { u16 a=0,b=1,c=1023; func_8001F878_20478(&a,&b,&c); assert(a==512 && b==511 && c==511); a=0; func_8001F878_20478(&a,&a,&a); assert(a==512); return 0; }

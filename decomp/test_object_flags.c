#include <assert.h>
#include <stddef.h>
#include "object_flags.h"
int main(void) { ObjectFlagNode c={0,0x81}, b={&c,0x20}, a={&b,0}; ObjectFlagOwner owner={{0},0}; _Static_assert(offsetof(ObjectFlagOwner,list)==0x18,"list offset"); assert(func_800362DC_36EDC(&owner)==0); owner.list=&a; assert(func_800362DC_36EDC(&owner)==0); assert(a.flags==0x80 && b.flags==0xA0 && c.flags==0x81); assert(a.next==&b && b.next==&c && c.next==0); return 0; }

/* Original USA 0x14108-0x1411C: linked object's flag-bit setter. */
typedef unsigned char u8;
typedef struct {u8 prefix[4]; u8 flags;} Linked;
typedef struct {u8 prefix[0x1C]; Linked *linked;} Outer;
void func_80013508_14108(Outer *o) { o->linked->flags |= 0x80; }

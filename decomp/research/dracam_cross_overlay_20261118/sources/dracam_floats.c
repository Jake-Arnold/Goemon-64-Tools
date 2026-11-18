/* Original USA 0x13FD4-0x14000: related graphics float fields. */
typedef unsigned char u8;
typedef struct { u8 padding[0x5C]; float a; float b; float pad1[2]; float c; float pad2[2]; float d; } FloatState;
void func_800133D4_13FD4(FloatState *o, float v) { o->a = v; }
void func_800133E0_13FE0(FloatState *o, float x, float y, float z) { o->b = x; o->c = y; o->d = z; }

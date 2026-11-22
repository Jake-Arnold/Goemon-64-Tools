/* Original USA 0x131D0-0x13228: parameter fields and volatile record setup. */
typedef unsigned char u8;
typedef short s16;
typedef unsigned int u32;
typedef struct {u8 flag; u8 pad; s16 index; float speed; u32 value;} Record;
typedef struct {u8 pad[0xC8]; s16 count; s16 max; Record * volatile record;} Owner;
typedef struct {u8 padding[0x5D]; u8 type; u8 extra[2]; float x,y,z;} Params;
void func_800125D0_131D0(Params *p, int type, float x, float y, float z) {
    p->type = type;
    p->x = x;
    p->y = y;
    p->z = z;
}
void func_800125F0_131F0(Owner *owner, int index, u32 value, float speed, s16 max) {
    owner->record->flag = 1;
    owner->record->index = index;
    owner->record->speed = speed;
    owner->record->value = value;
    owner->count = 0;
    owner->max = max;
}

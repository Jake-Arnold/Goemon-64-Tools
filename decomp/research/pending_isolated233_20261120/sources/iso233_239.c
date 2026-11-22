typedef unsigned char u8;
typedef unsigned short u16;
typedef struct MiniContext {
    u16 state0;
    u16 state2;
    float speed4;
    u8 pad08[0x12];
    u16 previous1A;
    u8 pad1C[0x11];
    u8 byte2D;
} MiniContext;
typedef struct PlayerTask {
    u8 pad00[0x5C];
    MiniContext *ctx;
    u8 pad60[0x08];
    float xvel;
    float yvel;
    float zvel;
    u8 pad74[0x70];
    float speedE4;
    float speedE8;
} PlayerTask;
extern float D_8020B348_5C7258;
extern int func_801E7DE8_5A3CF8(PlayerTask *);
extern void func_80038BC8_397C8(int);
void func_801E276C_59E67C(PlayerTask *task) {
    task->ctx->state0 = 1;
    task->zvel = 0.0f;
    task->yvel = 0.0f;
    task->xvel = 0.0f;
    if (func_801E7DE8_5A3CF8(task)) {
        float speed = D_8020B348_5C7258;
        task->speedE8 = speed;
        task->speedE4 = speed;
        task->ctx->speed4 = speed;
    } else {
        task->speedE8 = 2.0f;
        task->speedE4 = 2.0f;
        task->ctx->speed4 = 2.0f;
    }
    task->ctx->state2 = task->ctx->previous1A;
    task->ctx->byte2D = 0;
    func_80038BC8_397C8(0x22F);
}

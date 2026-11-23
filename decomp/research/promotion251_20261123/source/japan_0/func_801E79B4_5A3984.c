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
extern float D_802101B8_5CC188;
extern int func_801ECF10_5A8EE0(PlayerTask *);
extern void func_80038838_39438(int);
void func_801E79B4_5A3984(PlayerTask *task) {
    task->ctx->state0 = 1;
    task->zvel = 0.0f;
    task->yvel = 0.0f;
    task->xvel = 0.0f;
    if (func_801ECF10_5A8EE0(task)) {
        float speed = D_802101B8_5CC188;
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
    func_80038838_39438(0x22F);
}

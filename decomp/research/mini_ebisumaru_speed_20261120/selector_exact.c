typedef unsigned char u8;
typedef unsigned int u32;
typedef struct PlayerTask { u8 pad[0x90]; u8 speedProfileIndex; } PlayerTask;
typedef struct SpeedRec { float speed; u8 rest[20]; } SpeedRec;
extern SpeedRec D_800C7DBC[];
extern double D_8020B2D8_5C71E8;
extern int func_801E7DE8_5A3CF8(PlayerTask *);
extern float func_801E3DE0_59FCF0(PlayerTask *, float, float, float);
int func_801E1C90_59DBA0(PlayerTask *task) {
    float speed = D_800C7DBC[task->speedProfileIndex].speed;
    float result;
    int retval = 0;

    if (!((double)(speed < 0.0f ? -speed : speed) < D_8020B2D8_5C71E8)) {
    if (func_801E7DE8_5A3CF8(task)) {
        result = func_801E3DE0_59FCF0(task, 1.12f, 0, 0.3f);
    } else {
        result = func_801E3DE0_59FCF0(task, 2.8f, 0, 0.3f);
    }
    {
    switch ((u32)result) {
        case 0: retval=15; goto final;
        case 1: retval=14; goto final;
        case 2: retval=13; goto final;
        case 3: case 4: case 5: case 6: case 7:
        default: retval = 12; goto final;
    }
final: return retval;
    }
    }
    return 0;
}

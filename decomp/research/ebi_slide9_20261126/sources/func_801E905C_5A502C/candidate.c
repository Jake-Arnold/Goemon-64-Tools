typedef unsigned char u8;
typedef struct PlayerTask {
 u8 pad0[0x90];
 u8 speedProfileIndex;
 u8 pad91[0x53];
 float speedLimit;
 float speedStop;
} PlayerTask;
typedef struct SpeedRecord { float speed; u8 rest[20]; } SpeedRecord;
extern unsigned char g_system[];
extern double D_802101E8_5CC1B8;
extern float D_802101F0_5CC1C0;
float func_801E905C_5A502C(PlayerTask *task, float target, float initial, float factor) {
 float speed = ((SpeedRecord *)(g_system + 0x3B0FC))[task->speedProfileIndex].speed;
 float divisor;
 float next;
 if (!((double)(speed < 0.0f ? -speed : speed) < D_802101E8_5CC1B8)) {
 divisor = D_802101F0_5CC1C0 / speed;
 if ((double)divisor > 8.0) divisor = 8.0f;
 next = (target-initial) / divisor + initial;
 task->speedLimit = next;
 if (target <= next) task->speedLimit = target;
 task->speedStop = task->speedLimit * factor;
 return divisor;
 }
 return 0.0f;
}

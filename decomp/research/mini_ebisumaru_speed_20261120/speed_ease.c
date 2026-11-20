typedef unsigned char u8;
typedef struct PlayerTask {
 u8 pad0[0x90];
 u8 speedProfileIndex;
 u8 pad91[0x53];
 float speedLimit;
 float speedStop;
} PlayerTask;
typedef struct SpeedRecord { float speed; u8 rest[20]; } SpeedRecord;
extern SpeedRecord D_800C7DBC[];
extern double D_8020B370_5C7280;
extern float D_8020B378_5C7288;
float func_801E3DE0_59FCF0(PlayerTask *task, float target, float initial, float factor) {
 float speed = D_800C7DBC[task->speedProfileIndex].speed;
 float divisor;
 float next;
 if (!((double)(speed < 0.0f ? -speed : speed) < D_8020B370_5C7280)) {
 divisor = D_8020B378_5C7288 / speed;
 if ((double)divisor > 8.0) divisor = 8.0f;
 next = (target-initial) / divisor + initial;
 task->speedLimit = next;
 if (target <= next) task->speedLimit = target;
 task->speedStop = task->speedLimit * factor;
 return divisor;
 }
 return 0.0f;
}

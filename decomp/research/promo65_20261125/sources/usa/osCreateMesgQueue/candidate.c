typedef signed char s8; typedef unsigned char u8; typedef signed short s16; typedef unsigned short u16; typedef signed int s32; typedef unsigned int u32; typedef signed long long s64; typedef unsigned long long u64; typedef float f32; typedef double f64; typedef s32 M2C_UNK; typedef s8 M2C_UNK8; typedef s16 M2C_UNK16; typedef s32 M2C_UNK32; typedef s64 M2C_UNK64;
#define M2C_FIELD(expr,type_ptr,offset) (*(type_ptr)((s8 *)(expr)+(offset)))
#define NULL ((void*)0)
extern u32 __osDisableInt(void); extern void __osRestoreInt(u32);
typedef struct Queue { void *waitRecv, *waitSend; s32 validCount, first, msgCount; void **msg; } Queue;
extern char D_8007A270_7AE70;
void osCreateMesgQueue(Queue *mq, void **msg, s32 count) {
    mq->waitRecv = &D_8007A270_7AE70;
    mq->waitSend = &D_8007A270_7AE70;
    mq->validCount = 0;
    mq->first = 0;
    mq->msgCount = count;
    mq->msg = msg;
}

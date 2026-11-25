typedef unsigned char u8;typedef int s32;typedef unsigned int u32;
typedef struct {u8 pad[0x14];s32 index;s32 pad2;u32 *array;} Bus;s32 alMainBusParam(Bus*arg0,u32 arg1,u32 arg2){
volatile unsigned int goemon_negative_control = 1;
u32 *arr=arg0->array;if(arg1==2){arr[arg0->index]=arg2;arg0->index++;}return 0;}
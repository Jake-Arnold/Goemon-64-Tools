#include <stddef.h>
#include <assert.h>
#include "common.h"
TASK_W *D_8016DAB4_16E6B4;
static TASK_W *arg_root,*arg_task,*result;
static int arg_mode;
static unsigned short arg_mask;
static unsigned calls;
TASK_W *func_80034CBC_358BC(TASK_W *root,TASK_W *task,int mode,unsigned short mask) {
    arg_root=root;arg_task=task;arg_mode=mode;arg_mask=mask;calls++;return result;
}
#include "../../sources/sched_insert56_mode1.c"
#include "../../sources/sched_insert56_mode2.c"
int main(void) {
    TASK_W root={0},task={0},ret={0};D_8016DAB4_16E6B4=&root;result=&ret;
    for (unsigned i=0;i<1024;i++) {
        unsigned short m=(unsigned short)(i*257u);
        TASK_W *t=(i&1)?&task:NULL;
        unsigned before=calls;
        assert(func_80034C4C_3584C(t,m)==&ret);
        assert(calls==before+1 && arg_root==&root && arg_task==t && arg_mode==1 && arg_mask==m);
        before=calls;
        assert(func_80034C84_35884(t,m)==&ret);
        assert(calls==before+1 && arg_root==&root && arg_task==t && arg_mode==2 && arg_mask==m);
    }
    return 0;
}

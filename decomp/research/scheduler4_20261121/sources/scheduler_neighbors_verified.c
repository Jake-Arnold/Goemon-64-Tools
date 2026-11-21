#include "common.h"
extern TASK_W *D_8016DAB4_16E6B4;
extern TASK_W *func_80034B24_35724(TASK_W*, unsigned short);
extern TASK_W *func_80034B58_35758(TASK_W*,TASK_W*,unsigned short);
extern TASK_W *func_80034C4C_3584C(TASK_W*,unsigned short);
extern TASK_W *func_80034C84_35884(TASK_W*,unsigned short);
extern TASK_W *func_80034CBC_358BC(TASK_W*,TASK_W*,int,unsigned short);
extern void func_80034D24_35924(TASK_W*);
void func_80035204_35E04(void (*cb)(TASK_W*,struct CLS_W*)) {D_8016DAB4_16E6B4->exec[0]=cb;}
void func_80035214_35E14(TASK_W *task,void (*cb)(TASK_W*,struct CLS_W*)) {task->exec[0]=cb;}
void func_80034DD8_359D8(TASK_W* task,unsigned short mask) {func_80034D24_35924(func_80034B24_35724(task,mask));}
void func_80034E08_35A08(TASK_W* root,TASK_W* task,unsigned short mask) {func_80034D24_35924(func_80034B58_35758(root,task,mask));}
void func_80034E38_35A38(TASK_W* task,unsigned short mask) {func_80034D24_35924(func_80034C4C_3584C(task,mask));}
void func_80034E68_35A68(TASK_W* task,unsigned short mask) {func_80034D24_35924(func_80034C84_35884(task,mask));}

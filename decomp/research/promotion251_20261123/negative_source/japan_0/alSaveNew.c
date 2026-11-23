typedef unsigned char u8;typedef unsigned int u32;typedef int s32;
extern void alSavePull();extern void alSaveParam();extern void alFilterNew();void alSaveNew(void*arg0){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
alFilterNew(arg0,alSavePull,alSaveParam,3);*(volatile u32*)((u8*)arg0+0x14)=0;*(volatile u32*)((u8*)arg0+0x18)=1;}
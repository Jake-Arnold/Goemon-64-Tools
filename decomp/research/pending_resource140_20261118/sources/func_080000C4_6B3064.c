typedef unsigned int u32;
extern char func_8000F420_10020;
extern char func_8003521C_35E1C;
extern char func_0800011C_6B30BC;
extern char D_8020CBF0_5C8B00;
void func_080000C4_6B3064(void *a, void *b) {
    if (*(u32*)((char*)a+0x68) & 1) {
      ((void (*)(u32,void*,void*,u32))&func_8000F420_10020)(0x26E,&D_8020CBF0_5C8B00,b,0x44480000);
      ((void (*)(void (*)(void*,void*)))&func_8003521C_35E1C)((void (*)(void*,void*))&func_0800011C_6B30BC);
    }
}

typedef unsigned int u32;
extern char func_8021C434_5D79C4;
void func_08000268_6B7CE8(void *a, void *b) {
    ((void (*)(void*,u32))&func_8021C434_5D79C4)(a,2);
    *(u32*)((char*)a+0x68) |= 2;
}

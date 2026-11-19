typedef unsigned int u32;
extern char func_802176C4_5D2B94;
void func_08000268_6B3208(void *a, void *b) {
    ((void (*)(void*,u32))&func_802176C4_5D2B94)(a,2);
    *(u32*)((char*)a+0x68) |= 2;
}

extern unsigned char *D_8015C5C8_15D1C8;
extern const unsigned char D_3ADB2[];
extern void *D_8022B328_694D08[];
extern void *D_8022B324_694D04;
extern void *D_8022F1B0_698B90;

void func_8020D2A0_676C80(void) {
    register void **active = &D_8022B324_694D04;
    register void **display = &D_8022F1B0_698B90;
    short index = *(short *)(D_8015C5C8_15D1C8 + (unsigned long)D_3ADB2);
    void *selected = D_8022B328_694D08[index];
    *active = selected;
    *display = *active;
}

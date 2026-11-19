extern char D_80167C78_168878[];
void func_800102E0_10EE0(int index) {
    if (index != -1) {
        char *p = D_80167C78_168878 + (index << 4);
        *(short *)(p+0) = 0;
        *(short *)(p+2) = 0;
        p[4] = 0;
        p[5] = 0;
        *(int *)(p+8) = 0;
        *(short *)(p+12) = 0;
    }
}

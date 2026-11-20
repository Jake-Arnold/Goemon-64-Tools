extern void osViSetSpecialFeatures(unsigned int features);
extern void func_80038BC8_397C8(int mode);
extern void func_80013AC4_146C4(const void *resource);
extern void func_80013A24_14624(int resource_id);

extern unsigned char D_80229E44_693824[];
extern unsigned char D_80229E58_693838[];

void func_8020D818_6771F8(void) {
    osViSetSpecialFeatures(0x40);
    func_80038BC8_397C8(1);
    func_80013AC4_146C4(D_80229E44_693824);
}

void func_8020D870_677250(void) {
    func_80013A24_14624(0x4DD);
}

void func_8020D890_677270(void) {
    osViSetSpecialFeatures(0x40);
    func_80038BC8_397C8(1);
    func_80013AC4_146C4(D_80229E58_693838);
}

void func_8020D8C4_6772A4(void) {
    func_80013A24_14624(0x4D8);
}

void func_8020D92C_67730C(void) {
    func_80013A24_14624(0x4DC);
}

void func_8020D978_677358(void) {
    func_80013A24_14624(0x4DB);
}

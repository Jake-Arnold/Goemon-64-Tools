typedef short s16; typedef int s32;
typedef struct {char pad[8];s16 marker;} VmWork;
extern VmWork D_801C77E8_1C83E8;
extern s32 D_801C7798_1C8398;
extern s32 D_801C77A0_1C83A0;
extern s32 func_8003DF68_3EB68(void);
extern s16 *func_8003DF98_3EB98(s32,s16*);
extern void func_8000D060_DC60(s32,s16);
s16 *func_8003DE80_3EA80(s32 arg0, s16 *arg1) {
    s16 *var_s0 = arg1;
    s16 temp;
    while (1) {
        if (*var_s0 >= 0) {
            if (func_8003DF68_3EB68()) {
                D_801C77E8_1C83E8.marker=-1;
                D_801C77A0_1C83A0=D_801C7798_1C8398;
                return var_s0;
            }
            func_8000D060_DC60(arg0,*var_s0);
            temp=*var_s0;
            var_s0++;
            D_801C77E8_1C83E8.marker=temp;
            if (D_801C7798_1C8398) {
                D_801C77A0_1C83A0=D_801C7798_1C8398;
                return var_s0;
            }
        } else if (*var_s0 == -1) {
            D_801C77E8_1C83E8.marker=-1;
            return 0;
        } else {
            D_801C77E8_1C83E8.marker=-1;
            var_s0=func_8003DF98_3EB98(arg0,var_s0);
            D_801C77A0_1C83A0=D_801C7798_1C8398;
            return var_s0;
        }
    }
}

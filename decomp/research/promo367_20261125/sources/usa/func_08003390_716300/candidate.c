#include "m2c_types.h"
M2C_UNK func_08003648_7165B8(s32, void *);
extern char func_8003521C_35E1C;
extern M2C_UNK func_0800343C_7163AC;

void func_08003390_716300(s32 arg0, void *arg1) {
    s32 var_s1;
    void *var_s0;

    var_s0 = M2C_FIELD(arg1, void **, 0);
    var_s1 = 0;
    if (var_s0 != NULL) {
        do {
            if ((M2C_FIELD(arg1, f32 *, 0xC) - 84.0f) < M2C_FIELD(var_s0, f32 *, 0xC)) {
                var_s1 = 1;
                func_08003648_7165B8(arg0, var_s0);
            }
            var_s0 = M2C_FIELD(var_s0, void **, 0);
        } while (var_s0 != NULL);
    }
    if (var_s1 == 0) {
        ((M2C_UNK(*)())&func_8003521C_35E1C)(&func_0800343C_7163AC);
    }
}

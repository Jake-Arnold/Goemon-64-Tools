#include "m2c_types.h"
extern char func_80034E8C_35A8C;
M2C_UNK func_08003428_71A8C8();                     /* static */
M2C_UNK func_08003634_71AAD4(s32, void *);          /* static */

void func_08003384_71A824(s32 arg0, void *arg1) {
    s32 var_s3;
    void *var_s0;

    var_s0 = M2C_FIELD(arg1, void **, 0);
    var_s3 = 0;
    do {
        if ((M2C_FIELD(arg1, f32 *, 0xC) - 84.0f) < M2C_FIELD(var_s0, f32 *, 0xC)) {
            var_s3 = 1;
            func_08003634_71AAD4(arg0, var_s0);
        }
        var_s0 = M2C_FIELD(var_s0, void **, 0);
    } while (var_s0 != NULL);
    if (var_s3 == 0) {
        ((M2C_UNK(*)())&func_80034E8C_35A8C)(func_08003428_71A8C8);
    }
}

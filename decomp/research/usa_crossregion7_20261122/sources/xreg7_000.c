#include "probe_common.h"
s32 func_800363F4_36FF4(void *arg0, void *arg1) {
    void *var_v0;
    void *var_v1;
    if ((arg0 == 0) || (arg1 == 0)) return 0;
    var_v0 = M2C_FIELD(arg0, void **, 0x74);
    var_v1 = var_v0;
    if (var_v0 != arg1) {
        do {
            var_v1 = var_v0;
            var_v0 = M2C_FIELD(var_v0, void **, 0x74);
        } while (var_v0 != arg1);
    }
    M2C_FIELD(var_v1, void **, 0x74) = (void *)M2C_FIELD(arg1, void **, 0x74);
    M2C_FIELD(arg1, void **, 0x74) = (void *)M2C_FIELD(arg0, void **, 0x74);
    M2C_FIELD(arg0, void **, 0x74) = arg1;
    return 1;
}

#include "m2c_types.h"
M2C_UNK func_80220380_5DB910(void *);               /* extern */
M2C_UNK func_80220578_5DBB08(void *);               /* extern */
M2C_UNK func_802211B4_5DC744(void *);               /* extern */
M2C_UNK func_80221288_5DC818(void *);               /* extern */
M2C_UNK func_802298F8_5E4E88(void *);               /* extern */
M2C_UNK func_8021B828_5D6DB8(void *);               /* static */
M2C_UNK func_8021BE84_5D7414();                     /* static */
M2C_UNK func_8021D0C0_5D8650(void *);               /* static */
M2C_UNK func_8021D574_5D8B04(void *);               /* static */
M2C_UNK func_8021D6AC_5D8C3C(void *);               /* static */
M2C_UNK func_8021D700_5D8C90(void *);               /* static */
M2C_UNK func_8021EC90_5DA220(void *);               /* static */
M2C_UNK func_8021F098_5DA628(void *);               /* static */
M2C_UNK func_8021F6E8_5DAC78(void *);               /* static */

void func_8021DBEC_5D917C(void *arg0) {
    if (M2C_FIELD(arg0, s32 *, 0x18) != 0) {
        func_8021BE84_5D7414();
        func_8021B828_5D6DB8(arg0);
        func_802298F8_5E4E88(arg0);
        func_8021D6AC_5D8C3C(arg0);
        func_802211B4_5DC744(arg0);
        func_80220578_5DBB08(arg0);
        func_80221288_5DC818(arg0);
        func_8021F6E8_5DAC78(arg0);
        func_8021D700_5D8C90(arg0);
        func_80220380_5DB910(arg0);
        func_8021EC90_5DA220(arg0);
        func_8021D0C0_5D8650(arg0);
        func_8021D574_5D8B04(arg0);
        M2C_FIELD(arg0, s32 *, 0x68) = (s32) (M2C_FIELD(arg0, s32 *, 0x68) & 0xFFFBFFFF);
    }
    func_8021F098_5DA628(arg0);
}

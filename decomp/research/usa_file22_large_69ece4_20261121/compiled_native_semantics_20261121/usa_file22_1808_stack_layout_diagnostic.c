/* RESEARCH_ONLY / FAILED_NATIVE, diagnostic-only stack-layout padding.
 * Extra unused volatile arrays are artificial and not established Konami source.
 * 0x140 stack and key stack slots match original, but instruction code does not.
 */
typedef signed int s32; typedef unsigned int u32; typedef signed short s16; typedef unsigned short u16; typedef signed char s8; typedef unsigned char u8;
#define M2C_FIELD(expr, type_ptr, offset) (*(type_ptr)((s8 *)(expr) + (offset)))
extern u8 *D_801D701C_6A9C3C;

void func_801CC0C4_69ECE4(void *arg0) {
    volatile s32 reserve_prefix[1]; /* research only */
    s32 sp138;
    volatile s32 reserve_between_row_and_cache[13];
    s32 sp100;
    volatile s32 reserve_between_cache_and_clip[3];
    s32 spF8;
    s32 spF0;
    s32 spE8;
    u8 *spE4;
    u16 *spE0;
    volatile s32 reserve_between_pointers_and_pixel[1];
    s32 sp34;
    volatile s32 reserve_below_pixel[1];
    s16 temp_a1_983;
    s16 temp_a2_982;
    s16 temp_a3_984;
    s32 temp_a0_915;
    s32 temp_a0_949;
    s32 temp_a1_948;
    s32 temp_t8_914;
    s32 temp_t9_1351;
    s32 temp_v0_1091;
    s32 var_s1_952;
    s32 var_s2_954;
    s32 var_s3_947;
    s32 var_s4_935;
    u16 temp_a0_1194;
    u16 temp_a0_1256;
    u16 temp_t4_1114;
    u8 temp_v0_1119;
    u8 *temp_a3_1159;
    u8 *temp_a3_1214;
    u8 *temp_a3_1276;
    u8 *temp_t2_1180;
    u8 *temp_t2_1234;
    u8 *temp_t2_1296;
    u8 *temp_t3_1242;
    u8 *temp_t3_1304;
    u8 *temp_v0_1129;
    u8 *temp_v0_1146;
    u8 *temp_v0_1152;
    u8 *temp_v0_1165;
    u8 *temp_v0_1172;
    u8 *temp_v0_1192;
    u8 *temp_v0_1208;
    u8 *temp_v0_1221;
    u8 *temp_v0_1227;
    u8 *temp_v0_1254;
    u8 *temp_v0_1270;
    u8 *temp_v0_1283;
    u8 *temp_v0_1289;
    u8 *temp_v0_1313;
    u8 *temp_v0_1327;
    u8 *temp_v0_1335;

    spE4 = (u8 *)M2C_FIELD(arg0, s32 *, 4);
    spE0 = (u16 *)M2C_FIELD(arg0, s32 *, 8);
    sp100 = 0xFFFF;
    sp138 = 0;
    do {
        if ((sp138 >= 0) && (sp138 <= 0xFFFF)) {
            temp_t8_914 = sp138 << 5;
            temp_a0_915 = temp_t8_914 + 0x1F;
            sp34 = temp_t8_914;
            spF8 = temp_t8_914;
            spF0 = temp_a0_915;
            spE8 = 0;
            if ((temp_t8_914 < 0xF0) && (temp_a0_915 >= 0)) {
                if (temp_t8_914 < 0) {
                    spE8 = -temp_t8_914;
                    spF8 = 0;
                }
                if (temp_a0_915 >= 0xF0) {
                    spF0 = 0xEF;
                }
                var_s4_935 = 0;
                spF8 *= 4;
                spF0 *= 4;
                spE8 <<= 5;
                do {
                    if (var_s4_935 >= 0) {
                        var_s3_947 = 0;
                        if (var_s4_935 <= 0xFFFF) {
                            temp_a1_948 = var_s4_935 << 5;
                            temp_a0_949 = temp_a1_948 + 0x1F;
                            var_s1_952 = temp_a1_948;
                            var_s2_954 = temp_a0_949;
                            if (temp_a1_948 >= 0x140) {

                            } else if (temp_a0_949 < 0) {

                            } else {
                                if (temp_a1_948 < 0) {
                                    var_s3_947 = -temp_a1_948;
                                    var_s1_952 = 0;
                                }
                                if (temp_a0_949 >= 0x140) {
                                    var_s2_954 = 0x13F;
                                }
                                temp_a2_982 = M2C_FIELD(arg0, s16 *, 0x20);
                                temp_a1_983 = M2C_FIELD(arg0, s16 *, 0x1C);
                                temp_a3_984 = M2C_FIELD(arg0, s16 *, 0x22);
                                temp_v0_1091 = temp_a2_982 / 32;
                                temp_t4_1114 = *(spE0 + (temp_v0_1091 * *(spE4 + ((s32) (temp_a1_948 / temp_a2_982) % temp_a1_983) + (temp_a1_983 * ((s32) (sp34 / temp_a3_984) % (s16) M2C_FIELD(arg0, s16 *, 0x1E)))) * (temp_a3_984 / 32)) + (((s32) (temp_a1_948 % temp_a2_982) / 32)) + (temp_v0_1091 * ((s32) (sp34 % temp_a3_984) / 32)));
                                if (temp_t4_1114 != sp100) {
                                    sp100 = (s32) temp_t4_1114;
                                    temp_v0_1119 = M2C_FIELD(arg0, u8 *, 0x1A);
                                    switch (temp_v0_1119) { /* irregular */
                                    case 0:
                                        temp_v0_1129 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1129 + 8;
                                        M2C_FIELD(temp_v0_1129, s32 *, 0) = 0xFD100000;
                                        M2C_FIELD(temp_v0_1129, s32 *, 4) = (s32) (M2C_FIELD(arg0, s32 *, 0x10) + (((s32) (temp_t4_1114 << 0xA) / 4) * 2));
                                        temp_v0_1146 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1146 + 8;
                                        M2C_FIELD(temp_v0_1146, s32 *, 4) = 0x07054150;
                                        M2C_FIELD(temp_v0_1146, s32 *, 0) = 0xF5100000;
                                        temp_v0_1152 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1152 + 8;
                                        M2C_FIELD(temp_v0_1152, s32 *, 4) = 0;
                                        M2C_FIELD(temp_v0_1152, s32 *, 0) = 0xE6000000;
                                        temp_a3_1159 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_a3_1159 + 8;
                                        M2C_FIELD(temp_a3_1159, s32 *, 4) = 0x073FF100;
                                        M2C_FIELD(temp_a3_1159, s32 *, 0) = 0xF3000000;
                                        temp_v0_1165 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1165 + 8;
                                        M2C_FIELD(temp_v0_1165, s32 *, 4) = 0;
                                        M2C_FIELD(temp_v0_1165, s32 *, 0) = 0xE7000000;
                                        temp_v0_1172 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1172 + 8;
                                        M2C_FIELD(temp_v0_1172, s32 *, 0) = 0xF5101000;
                                        M2C_FIELD(temp_v0_1172, s32 *, 4) = 0x54150;
                                        temp_t2_1180 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_t2_1180 + 8;
                                        M2C_FIELD(temp_t2_1180, s32 *, 0) = 0xF2000000;
                                        M2C_FIELD(temp_t2_1180, s32 *, 4) = 0x7C07C;
                                        break;
                                    case 1:
                                        temp_v0_1192 = D_801D701C_6A9C3C;
                                        temp_a0_1194 = ((u16*)M2C_FIELD(arg0, s32 *, 0xC))[temp_t4_1114];
                                        D_801D701C_6A9C3C = temp_v0_1192 + 8;
                                        M2C_FIELD(temp_v0_1192, s32 *, 0) = 0xFD500000;
                                        M2C_FIELD(temp_v0_1192, s32 *, 4) = (s32) (M2C_FIELD(arg0, s32 *, 0x10) + ((((temp_a0_1194 & 0xFF) << 7) + ((temp_a0_1194 & 0xF00) * 8)) * 8));
                                        temp_v0_1208 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1208 + 8;
                                        M2C_FIELD(temp_v0_1208, s32 *, 4) = 0x07054150;
                                        M2C_FIELD(temp_v0_1208, s32 *, 0) = 0xF5500000;
                                        temp_a3_1214 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_a3_1214 + 8;
                                        M2C_FIELD(temp_a3_1214, s32 *, 4) = 0;
                                        M2C_FIELD(temp_a3_1214, s32 *, 0) = 0xE6000000;
                                        temp_v0_1221 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1221 + 8;
                                        M2C_FIELD(temp_v0_1221, s32 *, 4) = 0x071FF200;
                                        M2C_FIELD(temp_v0_1221, s32 *, 0) = 0xF3000000;
                                        temp_v0_1227 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1227 + 8;
                                        M2C_FIELD(temp_v0_1227, s32 *, 4) = 0;
                                        M2C_FIELD(temp_v0_1227, s32 *, 0) = 0xE7000000;
                                        temp_t2_1234 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_t2_1234 + 8;
                                        M2C_FIELD(temp_t2_1234, s32 *, 0) = 0xF5480800;
                                        M2C_FIELD(temp_t2_1234, s32 *, 4) = 0x54150;
                                        temp_t3_1242 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_t3_1242 + 8;
                                        M2C_FIELD(temp_t3_1242, s32 *, 0) = 0xF2000000;
                                        M2C_FIELD(temp_t3_1242, s32 *, 4) = 0x7C07C;
                                        break;
                                    case 2:
                                        temp_v0_1254 = D_801D701C_6A9C3C;
                                        temp_a0_1256 = ((u16*)M2C_FIELD(arg0, s32 *, 0xC))[temp_t4_1114];
                                        D_801D701C_6A9C3C = temp_v0_1254 + 8;
                                        M2C_FIELD(temp_v0_1254, s32 *, 0) = 0xFD500000;
                                        M2C_FIELD(temp_v0_1254, s32 *, 4) = (s32) (M2C_FIELD(arg0, s32 *, 0x10) + ((((temp_a0_1256 & 0xFF) << 6) + ((temp_a0_1256 & 0xF00) * 4)) * 8));
                                        temp_v0_1270 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1270 + 8;
                                        M2C_FIELD(temp_v0_1270, s32 *, 4) = 0x07054150;
                                        M2C_FIELD(temp_v0_1270, s32 *, 0) = 0xF5500000;
                                        temp_a3_1276 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_a3_1276 + 8;
                                        M2C_FIELD(temp_a3_1276, s32 *, 4) = 0;
                                        M2C_FIELD(temp_a3_1276, s32 *, 0) = 0xE6000000;
                                        temp_v0_1283 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1283 + 8;
                                        M2C_FIELD(temp_v0_1283, s32 *, 4) = 0x070FF400;
                                        M2C_FIELD(temp_v0_1283, s32 *, 0) = 0xF3000000;
                                        temp_v0_1289 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_v0_1289 + 8;
                                        M2C_FIELD(temp_v0_1289, s32 *, 4) = 0;
                                        M2C_FIELD(temp_v0_1289, s32 *, 0) = 0xE7000000;
                                        temp_t2_1296 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_t2_1296 + 8;
                                        M2C_FIELD(temp_t2_1296, s32 *, 0) = 0xF5400400;
                                        M2C_FIELD(temp_t2_1296, s32 *, 4) = 0x54150;
                                        temp_t3_1304 = D_801D701C_6A9C3C;
                                        D_801D701C_6A9C3C = temp_t3_1304 + 8;
                                        M2C_FIELD(temp_t3_1304, s32 *, 0) = 0xF2000000;
                                        M2C_FIELD(temp_t3_1304, s32 *, 4) = 0x7C07C;
                                        break;
                                    }
                                }
                                temp_v0_1313 = D_801D701C_6A9C3C;
                                D_801D701C_6A9C3C = temp_v0_1313 + 8;
                                M2C_FIELD(temp_v0_1313, s32 *, 4) = (s32) ((((var_s1_952 * 4) & 0xFFF) << 0xC) | (spF8 & 0xFFF));
                                M2C_FIELD(temp_v0_1313, s32 *, 0) = (s32) ((((var_s2_954 * 4) & 0xFFF) << 0xC) | 0xE4000000 | (spF0 & 0xFFF));
                                temp_v0_1327 = D_801D701C_6A9C3C;
                                D_801D701C_6A9C3C = temp_v0_1327 + 8;
                                M2C_FIELD(temp_v0_1327, s32 *, 4) = (s32) (((var_s3_947 << 5) << 0x10) | (spE8 & 0xFFFF));
                                M2C_FIELD(temp_v0_1327, s32 *, 0) = 0xB4000000;
                                temp_v0_1335 = D_801D701C_6A9C3C;
                                D_801D701C_6A9C3C = temp_v0_1335 + 8;
                                M2C_FIELD(temp_v0_1335, s32 *, 0) = 0xB3000000;
                                M2C_FIELD(temp_v0_1335, s32 *, 4) = 0x10000400;
                            }
                        }
                    }
                    var_s4_935 += 1;
                } while (var_s4_935 != 0xB);
            }
        }
        temp_t9_1351 = sp138 + 1;
        sp138 = temp_t9_1351;
    } while (temp_t9_1351 != 9);
}

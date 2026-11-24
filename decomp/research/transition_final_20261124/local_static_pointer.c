#include "transition.h"
void func_800030F0_3CF0(void) {
    u16 i;
    TransitionStatic *fields = &D_800BCCC0_BD8C0;
    u8 state = fields->field_add6;
    switch (state) {
        case 0:
            fields->field_adb6 = 1;
            fields->field_add6 = ++state;
            fields->field_add5 = 0;
            break;
        case 1:
            if (D_800548D8_554D8 == 0) {
                func_8000383C_443C();
                func_80001C00_2800(15, (void *)func_801CB460);
                i = 0xFFFF;
                test_countdown:
                if (i == 0) goto done_countdown;
                i--;
                goto test_countdown;
                done_countdown:
                D_8015C5C8_15D1C8->unk_3add6++;
            }
            break;
        case 2:
            fields->field_adb6 = 0;
            D_8015C5C8_15D1C8->unk_3add6++;
            break;
        case 3:
            D_8015C5C8_15D1C8->intended_room_group_index = 3;
            func_8003488C_3548C(D_801CCB7C);
            D_8015C5C8_15D1C8->unk_3add6++;
            break;
        case 4:
            switch (fields->field_add5) {
                case 0:
                    func_80034734_35334();
                    break;
                case 1:
                    func_8000383C_443C();
                    D_8015C5C8_15D1C8->intended_room_group_index = 3;
                    fields->field_add5 = 0;
                    func_8003488C_3548C(D_801CCB7C);
                    break;
                case 2:
                    func_8000383C_443C();
                    D_8015C5C8_15D1C8->intended_room_group_index = 1;
                    fields->field_add5 = 0;
                    func_8003488C_3548C(D_801CCB7C);
                    break;
                case 3:
                    func_8000383C_443C();
                    fields->field_ae18 = 0x8000;
                    func_80003728_4328(5);
                    break;
            }
            break;
    }
}

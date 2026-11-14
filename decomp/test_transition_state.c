#include <assert.h>
#include <stddef.h>
#include "common.h"
static SYS_W sys; static SYS_W alternate_sys; SYS_W *D_8015C5C8_15D1C8=&sys;
static int stage; u8 D_800C7A95_C8695; s32 D_8006D328_6DF28;
void func_800369F0_375F0(s32 x) { assert(stage==14 && x==33); stage=15; }
void func_80038BC8_397C8(s32 x) { assert(stage==15 && x==7 && sys.unk_3add6==1); stage=16; }
void func_800038E4_44E4(void);
void func_8000B364_BF64(void) { assert(stage==0); stage=1; }
char D_802F7000[1];
u8 D_800627F0_633F0[1]; u16 D_800C7AE4_C86E4;
void func_80004240_4E40(void) { assert(stage==1); stage=2; }
void func_8003488C_3548C(void *p) { assert(stage==2 && p==0); stage=3; }
void func_8000A0F0_ACF0(void) { assert(stage==3); stage=4; }
void func_80035B50_36750(void) { assert(stage==4); stage=5; }
void func_8000B880_C480(void) { assert(stage==5); stage=6; }
void func_8000B8A4_C4A4(void *p) { assert(stage==6 && p==D_800627F0_633F0); stage=7; }
void func_80013940_14540(void) { assert(stage==7 && D_800C7AE4_C86E4==20); stage=8; }
void osViBlack(u8 n) { assert(stage==8 && n==0); stage=9; }
void func_800148C0_154C0(void *p, char *buffer, u32 size) { assert(stage==9 && p==(u8 *)&sys+0xC7FA4 && buffer==D_802F7000 && size==0xA000); stage=10; }
void func_8001F8B0_204B0(void) { assert(stage==10); stage=11; }
void func_80034734_35334(void) { if (stage==11) stage=12; else { assert(stage==12 || stage==13); stage++; } }
void func_80003328_3F28(void); void func_80003358_3F58(void);
void func_80003728_4328(u8);
void func_800033B0_3FB0(void); void func_800033EC_3FEC(void);
void func_80003478_4078(void); void func_800034D0_40D0(void);
void func_80003578_4178(void); void func_800035D0_41D0(void);
void func_80003678_4278(void); void func_800036D0_42D0(void);
void func_8000378C_438C(void); void func_800037E4_43E4(void);
static void check_steps(void) {
    void (*inc[])(void)={func_800033B0_3FB0,func_80003478_4078,func_80003578_4178,func_80003678_4278,func_8000378C_438C};
    void (*dec[])(void)={func_800033EC_3FEC,func_800034D0_40D0,func_800035D0_41D0,func_800036D0_42D0,func_800037E4_43E4};
    u8 *values[]={&sys.unk_3ade0,&sys.unk_3adde,&sys.unk_3add8,&sys.unk_3add6,&sys.stepw};
    u8 *ends[]={&sys.unk_3ade1,&sys.unk_3addf,&sys.unk_3add9,&sys.unk_3add7,&sys.stepw_end};
    for (int i=0;i<5;i++) {
        for (int j=0;j<i;j++) { *values[j]=7; *ends[j]=9; }
        *values[i]=255; *ends[i]=7; inc[i](); assert(*values[i]==0 && *ends[i]==0);
        for (int j=0;j<i;j++) assert(*values[j]==0 && *ends[j]==0);
        for (int j=0;j<i;j++) { *values[j]=7; *ends[j]=9; }
        *values[i]=0; *ends[i]=7; dec[i](); assert(*values[i]==255 && *ends[i]==0);
        for (int j=0;j<i;j++) assert(*values[j]==0 && *ends[j]==0);
    }
}

enum {
    LOOP_EVENT_80034734 = 1,
    LOOP_EVENT_80036908,
    LOOP_EVENT_80003880
};

static u8 transition_byte_7CDD;
static u16 transition_halfword_7A76;
static s32 gate_helper_result;
static s32 gate_helper_argument;
static int loop_events[3];
static int loop_event_count;
static int rebind_system_pointer_in_80003880;

static void record_loop_event(int event) {
    assert(loop_event_count < (int)(sizeof(loop_events) / sizeof(loop_events[0])));
    loop_events[loop_event_count++] = event;
}

static void reference_80034734(void) {
    record_loop_event(LOOP_EVENT_80034734);
}

static s32 reference_80036908(s32 argument) {
    record_loop_event(LOOP_EVENT_80036908);
    gate_helper_argument = argument;
    return gate_helper_result;
}

static void reference_80003880(void) {
    record_loop_event(LOOP_EVENT_80003880);
    assert(transition_byte_7CDD == 5);
    assert(transition_halfword_7A76 == 1);
    if (rebind_system_pointer_in_80003880) {
        D_8015C5C8_15D1C8 = &alternate_sys;
    }
}

/* MIPS-derived reference only; func_8000394C remains GLOBAL_ASM. */
static void reference_transition_loop_8000394C(void) {
    reference_80034734();
    if (reference_80036908(D_8006D328_6DF28) != 0) {
        return;
    }
    transition_byte_7CDD = 5;
    transition_halfword_7A76 = 1;
    reference_80003880();
    D_8015C5C8_15D1C8->unk_3add6++;
}

static void reset_loop_fixture(void) {
    transition_byte_7CDD = 0xA5;
    transition_halfword_7A76 = 0xBEEF;
    gate_helper_result = 0;
    gate_helper_argument = 0;
    loop_event_count = 0;
    rebind_system_pointer_in_80003880 = 0;
    D_8006D328_6DF28 = 0x12345678;
    D_8015C5C8_15D1C8 = &sys;

    sys.stepw = 0x17;
    sys.stepw_end = 0x24;
    sys.unk_3add6 = 0xFF;
    sys.unk_3add7 = 0x31;
    sys.unk_3add8 = 0x42;
    sys.unk_3add9 = 0x53;
    sys.unk_3adde = 0x64;
    sys.unk_3addf = 0x75;
    alternate_sys.stepw = 0x86;
    alternate_sys.stepw_end = 0x97;
    alternate_sys.unk_3add6 = 0xFF;
    alternate_sys.unk_3add7 = 0xA8;
    alternate_sys.unk_3add8 = 0xB9;
    alternate_sys.unk_3add9 = 0xCA;
    alternate_sys.unk_3adde = 0xDB;
    alternate_sys.unk_3addf = 0xEC;
}

static void assert_transition_sentinels(u8 stepw, u8 stepw_end,
                                        u8 next_byte, u8 next_end,
                                        u8 nested_byte, u8 nested_end,
                                        u8 selector, u8 selector_end) {
    assert(D_8015C5C8_15D1C8->stepw == stepw);
    assert(D_8015C5C8_15D1C8->stepw_end == stepw_end);
    assert(D_8015C5C8_15D1C8->unk_3add7 == next_end);
    assert(D_8015C5C8_15D1C8->unk_3add8 == nested_byte);
    assert(D_8015C5C8_15D1C8->unk_3add9 == nested_end);
    assert(D_8015C5C8_15D1C8->unk_3adde == selector);
    assert(D_8015C5C8_15D1C8->unk_3addf == selector_end);
    assert(D_8015C5C8_15D1C8->unk_3add6 == next_byte);
}

static void test_transition_loop_nonzero_gate_returns_without_direct_stores(void) {
    reset_loop_fixture();
    gate_helper_result = 1;
    reference_transition_loop_8000394C();

    assert(loop_event_count == 2);
    assert(loop_events[0] == LOOP_EVENT_80034734);
    assert(loop_events[1] == LOOP_EVENT_80036908);
    assert(gate_helper_argument == 0x12345678);
    assert(transition_byte_7CDD == 0xA5);
    assert(transition_halfword_7A76 == 0xBEEF);
    assert(D_8015C5C8_15D1C8 == &sys);
    assert_transition_sentinels(0x17, 0x24, 0xFF, 0x31, 0x42, 0x53, 0x64, 0x75);
}

static void test_transition_loop_zero_gate_stores_before_reset_and_reloads_pointer(void) {
    reset_loop_fixture();
    rebind_system_pointer_in_80003880 = 1;
    reference_transition_loop_8000394C();

    assert(loop_event_count == 3);
    assert(loop_events[0] == LOOP_EVENT_80034734);
    assert(loop_events[1] == LOOP_EVENT_80036908);
    assert(loop_events[2] == LOOP_EVENT_80003880);
    assert(transition_byte_7CDD == 5);
    assert(transition_halfword_7A76 == 1);
    assert(D_8015C5C8_15D1C8 == &alternate_sys);
    assert(sys.unk_3add6 == 0xFF);
    assert_transition_sentinels(0x86, 0x97, 0, 0xA8, 0xB9, 0xCA, 0xDB, 0xEC);
}

static void test_transition_loop_counter_wraps_as_byte(void) {
    reset_loop_fixture();
    sys.unk_3add6 = 0;
    reference_transition_loop_8000394C();
    assert(sys.unk_3add6 == 1);

    reset_loop_fixture();
    reference_transition_loop_8000394C();
    assert(sys.unk_3add6 == 0);
}

int main(void) {
    _Static_assert(offsetof(SYS_W,stepw)==0x3ADD4,"stepw offset");
    _Static_assert(offsetof(SYS_W,stepw_end)==0x3ADD5,"stepw_end offset");
    _Static_assert(offsetof(SYS_W,retraces_per_game_step)==0x3ADCA,"retrace offset");
    sys.stepw=4;sys.stepw_end=9;sys.retraces_per_game_step=7;
    sys.unk_3add6=5;sys.unk_3add7=6;sys.unk_3add8=7;sys.unk_3add9=8;
    sys.unk_3adde=9;sys.unk_3addf=10;sys.unk_3ade0=11;sys.unk_3ade1=12;
    func_80003728_4328(11);
    assert(sys.stepw==11 && sys.stepw_end==0 && sys.retraces_per_game_step==2);
    assert(sys.unk_3add6==0 && sys.unk_3add7==0 && sys.unk_3add8==0 &&
           sys.unk_3add9==0 && sys.unk_3adde==0 && sys.unk_3addf==0 &&
           sys.unk_3ade0==0 && sys.unk_3ade1==0);
    func_80003328_3F28();
    assert(stage==10 && sys.stepw==0x11);
    func_80003358_3F58();
    assert(stage==12);
    D_800C7A95_C8695=0;
    func_800038E4_44E4();
    assert(stage==13 && sys.unk_3add6==0);
    D_800C7A95_C8695=1;
    D_8006D328_6DF28=33;
    func_800038E4_44E4();
    assert(stage==16);
    check_steps();

    test_transition_loop_nonzero_gate_returns_without_direct_stores();
    test_transition_loop_zero_gate_stores_before_reset_and_reloads_pointer();
    test_transition_loop_counter_wraps_as_byte();
    return 0;
}

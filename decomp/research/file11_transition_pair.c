/* Dual-region native IDO 5.3 matching-C research; staged independently per region. */
typedef unsigned int u32;
#ifdef GOEMON_USA
#define GOEMON_ADVANCE func_801F845C_5B436C
#define GOEMON_IDLE func_801F8488_5B4398
#define GOEMON_STEP func_801F95D8_5B54E8
#define GOEMON_SET_CB func_8003521C_35E1C
#else
#define GOEMON_ADVANCE func_801FD364_5B9334
#define GOEMON_IDLE func_801FD390_5B9360
#define GOEMON_STEP func_801FE4E0_5BA4B0
#define GOEMON_SET_CB func_80034E8C_35A8C
#endif
extern void GOEMON_STEP(void);
extern void GOEMON_SET_CB(void (*cb)(u32, u32));
void GOEMON_IDLE(u32 a0, u32 a1);
void GOEMON_ADVANCE(void) {
    GOEMON_STEP();
    GOEMON_SET_CB(GOEMON_IDLE);
}
void GOEMON_IDLE(u32 a0, u32 a1) { }

/* Native IDO 5.3 candidate: nine 32-byte actor wrappers near character switching.
 * The second argument is intentionally unused in the C call. The original
 * compiler nevertheless spills incoming a1 in the jal delay slot. Do not
 * replace this with a fixed-size inline assembler stub.
 *
 * These are research candidates until full-overlay/full-ROM proof is complete.
 */
typedef unsigned int u32;
#if defined(REGION_USA)
#define ACTION_A func_801E1B60_59DA70
#define ACTION_B func_801E7CC4_5A3BD4
#define ACTION_C func_801E15D0_59D4E0
#define W0 func_801DDA08_599918
#define W1 func_801DDA28_599938
#define W2 func_801DDA48_599958
#define W3 func_801DDA68_599978
#define W4 func_801DDA88_599998
#define W5 func_801DDAA8_5999B8
#define W6 func_801DDAC8_5999D8
#define W7 func_801DDAE8_5999F8
#define W8 func_801DDB08_599A18
#elif defined(REGION_JAPAN)
#define ACTION_A func_801E6DA8_5A2D78
#define ACTION_B func_801ECDEC_5A8DBC
#define ACTION_C func_801E67F0_5A27C0
#define W0 func_801E2DB8_59ED88
#define W1 func_801E2DD8_59EDA8
#define W2 func_801E2DF8_59EDC8
#define W3 func_801E2E18_59EDE8
#define W4 func_801E2E38_59EE08
#define W5 func_801E2E58_59EE28
#define W6 func_801E2E78_59EE48
#define W7 func_801E2E98_59EE68
#define W8 func_801E2EB8_59EE88
#else
#error Define REGION_USA or REGION_JAPAN
#endif
extern void ACTION_A(void *actor);
extern void ACTION_B(void *actor);
extern void ACTION_C(void *actor);
void W0(void *actor, u32 event) { ACTION_A(actor); }
void W1(void *actor, u32 event) { ACTION_A(actor); }
void W2(void *actor, u32 event) { ACTION_A(actor); }
void W3(void *actor, u32 event) { ACTION_B(actor); }
void W4(void *actor, u32 event) { ACTION_B(actor); }
void W5(void *actor, u32 event) { ACTION_C(actor); }
void W6(void *actor, u32 event) { ACTION_C(actor); }
void W7(void *actor, u32 event) { ACTION_C(actor); }
void W8(void *actor, u32 event) { ACTION_C(actor); }
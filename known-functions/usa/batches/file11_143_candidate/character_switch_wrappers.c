/* Original-address IDO 5.3 candidates for nine USA file_11 actor wrappers.
 * The incoming second parameter is intentionally unused by the C calls.
 * Tested against ROM 0x599918..0x599A38 (288 bytes).
 */
typedef unsigned int u32;
extern void func_801E1B60_59DA70(void *actor);
extern void func_801E7CC4_5A3BD4(void *actor);
extern void func_801E15D0_59D4E0(void *actor);
void func_801DDA08_599918(void *actor, u32 event) { func_801E1B60_59DA70(actor); }
void func_801DDA28_599938(void *actor, u32 event) { func_801E1B60_59DA70(actor); }
void func_801DDA48_599958(void *actor, u32 event) { func_801E1B60_59DA70(actor); }
void func_801DDA68_599978(void *actor, u32 event) { func_801E7CC4_5A3BD4(actor); }
void func_801DDA88_599998(void *actor, u32 event) { func_801E7CC4_5A3BD4(actor); }
void func_801DDAA8_5999B8(void *actor, u32 event) { func_801E15D0_59D4E0(actor); }
void func_801DDAC8_5999D8(void *actor, u32 event) { func_801E15D0_59D4E0(actor); }
void func_801DDAE8_5999F8(void *actor, u32 event) { func_801E15D0_59D4E0(actor); }
void func_801DDB08_599A18(void *actor, u32 event) { func_801E15D0_59D4E0(actor); }

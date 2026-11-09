/* Research-only negative-tail VM command walker layout probe.
 * Original USA func_8003DE80_3EA80 is 232 bytes. Isolated pinned IDO 5.3
 * produces 228 bytes, 8/35 directly comparable original word positions.
 * This is NOT an exact MIPS or full-ROM match. Do not integrate into script_vm.
 */
typedef signed int s32; typedef signed short s16;
extern s32 D_801C7798_1C8398, D_801C77A0_1C83A0;
typedef struct {char reserved[8]; s16 marker;} VmWork;
extern VmWork D_801C77E8_1C83E8;
extern s32 func_8003DF68_3EB68(void);
extern void func_8000D060_DC60(s32,s32);
extern s16 *func_8003DF98_3EB98(s32,s16*);
s16 *func_8003DE80_3EA80(s32 actor, s16 *cmd) {
  s16 token;
  for(;;){
    token=*cmd;
    if (token<0) goto negative;
    if (func_8003DF68_3EB68()) {
      D_801C77E8_1C83E8.marker=-1;
      D_801C77A0_1C83A0=D_801C7798_1C8398;
      return cmd;
    }
    func_8000D060_DC60(actor,*cmd);
    D_801C77E8_1C83E8.marker=*cmd++;
    if(D_801C7798_1C8398) {
      D_801C77A0_1C83A0=D_801C7798_1C8398;
      return cmd;
    }
  }
negative:
  D_801C77E8_1C83E8.marker=-1;
  if (token==-1) return 0;
  cmd=func_8003DF98_3EB98(actor,cmd);
  D_801C77A0_1C83A0=D_801C7798_1C8398;
  return cmd;
}

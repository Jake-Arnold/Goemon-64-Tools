/* Japan rev-0: main executable ROM 0x10D18, 28 original instruction bytes.
 * Indexed 12-byte record update; original global symbol/relocations retained. */
extern unsigned short D_8016D6DA_16E2DA[];

void func_80010118_10D18(int index) {
    *(unsigned short *)((char *)D_8016D6DA_16E2DA + index * 12) = 0;
}

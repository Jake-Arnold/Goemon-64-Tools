/* Japan rev-0: main executable ROM 0x9100, 64 original instruction bytes.
 * Symbolic pointer offset preserved as D_C5F78, not a hardcoded literal. */
extern char *D_8015C5C8_15D1C8;
#ifndef GOEMON_HOST_TEST
extern char D_C5F78[];
#else
#define D_C5F78 ((char *)0xC5F78)
#endif
extern char D_8005B6E0_5C2E0[];
extern char D_8006ADD8_6B9D8[];
extern void func_80005A20_6620(void *);

void func_80008650_9250(void) {
    *(void **)(D_8015C5C8_15D1C8 + (unsigned long)D_C5F78) = D_8005B6E0_5C2E0;
    func_80005A20_6620(D_8006ADD8_6B9D8);
}

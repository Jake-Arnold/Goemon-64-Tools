/* Japan rev-0: main executable ROM 0x9100, 64 original instruction bytes.
 * Symbolic pointer offset preserved as D_C5F78, not a hardcoded literal. */
extern char *g_system_ptr;
#ifndef GOEMON_HOST_TEST
extern char D_C5F78[];
#else
#define D_C5F78 ((char *)0xC5F78)
#endif
extern char D_8005B960_5C560[];
extern char D_800708B8_714B8[];
extern void func_800058D0_64D0(void *);

void func_80008500_9100(void) {
    *(void **)(g_system_ptr + (unsigned long)D_C5F78) = D_8005B960_5C560;
    func_800058D0_64D0(D_800708B8_714B8);
}

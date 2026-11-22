/* Japan rev-0: main executable ROM 0x9140, 24 original instruction bytes.
 * The original 0xC5F7C offset is a symbolic MIPS relocation. */
extern char *g_system_ptr;
#ifndef GOEMON_HOST_TEST
extern char D_C5F7C[];
#else
#define D_C5F7C ((char *)0xC5F7C)
#endif

void func_80008540_9140(int value) {
    *(int *)(g_system_ptr + (unsigned long)D_C5F7C) = value;
}

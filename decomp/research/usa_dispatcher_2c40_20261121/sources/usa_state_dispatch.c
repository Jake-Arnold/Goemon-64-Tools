typedef unsigned char u8;
extern u8 *D_8015C5C8_15D1C8;
#ifdef __sgi
extern unsigned char D_3ADD4[];
#define STATE_OFFSET ((unsigned int)D_3ADD4)
#else
#define STATE_OFFSET 0x3ADD4
#endif
typedef void (*DispatchFn)(void);
typedef struct DispatchTable { DispatchFn callbacks[18]; } DispatchTable;
extern const DispatchTable D_80058908_59508;
void func_80002040_2C40(void) {
    volatile int unused[2];
    DispatchTable table = D_80058908_59508;
    table.callbacks[D_8015C5C8_15D1C8[STATE_OFFSET]]();
}

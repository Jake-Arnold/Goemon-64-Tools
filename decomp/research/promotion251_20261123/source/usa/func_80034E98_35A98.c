/* Original JP task lifecycle wrappers: research probes, no promotion claims.
 * Keep each target function independently compiled for size/code comparison.
 */
typedef unsigned short u16;
typedef signed short s16;
typedef struct Task Task;
extern Task *D_80173294_173E94;
extern void *func_800347C8_353C8(Task *task, void *data, u16 kind);
extern void *func_800348BC_354BC(void *a, u16 b);
extern void *func_800348F4_354F4(void *a, u16 b);
extern void *func_80034CBC_358BC(void *a, void *b, s16 mode, u16 flags);
extern void *func_80034D24_35924(void *task);
extern void *func_80034794_35394(void *a, u16 kind);

void *func_80034E98_35A98(void *a, void *b, s16 c, u16 d) {
    return func_80034D24_35924(func_80034CBC_358BC(a,b,c,d));
}

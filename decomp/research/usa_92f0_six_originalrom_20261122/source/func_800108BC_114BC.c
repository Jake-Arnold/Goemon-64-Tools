#include "common.h"
extern char D_800637C0_643C0[];
typedef struct {unsigned int w0,w1;} RawGfx;
/* IDO 5.3 changes instruction scheduling if a newline is introduced
 * between the first two assignments. This line grouping is intentional. */
RawGfx* func_800108BC_114BC(RawGfx*p){p->w0=0x06000000;p->w1=(unsigned)D_800637C0_643C0;p++;p->w0=0xb8000000;p->w1=0;return p;}

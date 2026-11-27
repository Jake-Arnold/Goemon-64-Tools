#include "m2c_types.h"
void func_8001D394_1DF94(void *);                   /* extern */

typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec3f;

void func_801DBA00_597910(Vec3f *arg0, Vec3f *arg1) {
    f32 scale;
    scale = -(arg0->y / (arg0->z * arg0->z + (arg0->x * arg0->x + arg0->y * arg0->y)));
    arg1->x = arg0->x * scale;
    arg1->y = (arg0->y * scale) + 1.0;
    arg1->z = arg0->z * scale;
    func_8001D394_1DF94(arg1);
}

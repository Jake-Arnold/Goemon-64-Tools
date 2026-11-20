/* Exercise original recovered C, with host pointer field correctly aligned. */
#include <assert.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
void func_80033D10_34910(void *object);
int main(void) {
    unsigned char backing[0x70 + sizeof(void*)];
    size_t stride = sizeof(void*);
    unsigned char *object = backing;
    while (((uintptr_t)(object + 0x54) % stride) != 0) ++object;
    for (unsigned int i=0;i<1000;++i) {
        float values[4] = {(float)(i+1), (float)(i+2), (float)(i+3), 12345.0f};
        float *pointer = values;
        memset(backing, 0, sizeof(backing));
        memcpy(object+0x54, &pointer, sizeof(pointer));
        func_80033D10_34910(object);
        assert(values[0]==0.0f && values[1]==0.0f && values[2]==0.0f);
        assert(values[3]==12345.0f);
        pointer = NULL;
        memcpy(object+0x54, &pointer, sizeof(pointer));
        values[0]=27.0f;
        func_80033D10_34910(object);
        assert(values[0]==27.0f);
    }
    return 0;
}

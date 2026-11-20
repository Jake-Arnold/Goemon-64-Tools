/* Host semantic regression of an authentic newly promoted C source. */
#include <assert.h>
#include <stdint.h>
#include <string.h>
void func_80011968_12568(void *object, int target);
int main(void) {
    union {uint32_t words[40]; unsigned char bytes[160];} obj;
    for (int n=0;n<1000;++n) {
        memset(&obj,0xA5,sizeof(obj));
        func_80011968_12568(obj.bytes,n);
        assert(obj.words[0x5C/4]==(n==0?0:(uint32_t)(n+0x5C)));
        assert(obj.words[0]==0xA5A5A5A5u);
    }
    func_80011968_12568((void *)0,1);
    return 0;
}

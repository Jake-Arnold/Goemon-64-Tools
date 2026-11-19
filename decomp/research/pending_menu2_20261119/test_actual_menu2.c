/* Sanitizer regression executing both original-address C source bodies. */
#include <assert.h>
#include <stdint.h>
#include <string.h>

unsigned char D_80167C78_168878[40*16] __attribute__((aligned(16)));
short D_80167EFA_168AFA[40*6] __attribute__((aligned(16)));
void func_800102E0_10EE0(int index);
void func_80010358_10F58(int index);

int main(void) {
    unsigned char before[sizeof D_80167C78_168878];
    for (int repetition=0; repetition<1000; repetition++) {
        memset(D_80167C78_168878, 0xA5, sizeof D_80167C78_168878);
        memset(D_80167EFA_168AFA, 0xA5, sizeof D_80167EFA_168AFA);
        memcpy(before, D_80167C78_168878, sizeof before);
        func_800102E0_10EE0(-1);
        assert(!memcmp(before, D_80167C78_168878, sizeof before));
        const int index = repetition % 40;
        unsigned char *p = D_80167C78_168878 + index*16;
        func_800102E0_10EE0(index);
        assert(p[0]==0 && p[1]==0 && p[2]==0 && p[3]==0);
        assert(p[4]==0 && p[5]==0 && p[6]==0xA5 && p[7]==0xA5);
        assert(p[8]==0 && p[9]==0 && p[10]==0 && p[11]==0);
        assert(p[12]==0 && p[13]==0 && p[14]==0xA5 && p[15]==0xA5);
        func_80010358_10F58(index);
        assert(D_80167EFA_168AFA[index*6]==0);
        assert(D_80167EFA_168AFA[(index*6+1)%240] != 0);
    }
    return 0;
}

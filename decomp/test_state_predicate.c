#include <assert.h>
#include <stdint.h>
#include <string.h>

unsigned char D_800BCCC0_BD8C0[0xB000];
void func_80006274_6E74(long arg0, long arg1);

int main(void) {
    memset(D_800BCCC0_BD8C0, 0xA5, sizeof(D_800BCCC0_BD8C0));
    func_80006274_6E74(0x12345678L, 0x89ABCDEFL);
    assert(*(uint16_t *)(D_800BCCC0_BD8C0 + 0x7FFF + 0x2DB7) == 1);
    assert(*(uint16_t *)(D_800BCCC0_BD8C0 + 0xAE3A) == 0x5678);
    assert(*(uint32_t *)(D_800BCCC0_BD8C0 + 0xAE3C) == 0x89ABCDEFu);
    assert(D_800BCCC0_BD8C0[0xAE40] == 0xA5);
    return 0;
}

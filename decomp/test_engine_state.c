#include <assert.h>
#include <stdint.h>

uint8_t engine_reset_fixture[4] = {0x34, 0x12, 0x56, 0x78};

__asm__(
    ".globl D_801C09D8_1C15D8\n"
    ".set D_801C09D8_1C15D8, engine_reset_fixture\n"
    ".globl D_801C09DA_1C15DA\n"
    ".set D_801C09DA_1C15DA, engine_reset_fixture+2\n");

void func_8003A1E8_3ADE8(void);

int main(void) {
    func_8003A1E8_3ADE8();
    assert(engine_reset_fixture[0] == 0);
    assert(engine_reset_fixture[1] == 0);
    assert(engine_reset_fixture[2] == 0);
    assert(engine_reset_fixture[3] == 0x78);
    return 0;
}

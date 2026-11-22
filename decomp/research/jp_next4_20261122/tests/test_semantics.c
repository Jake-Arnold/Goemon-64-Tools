/* Test original C bodies with defined host backing storage; not N64 emulation. */
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

typedef struct { char unknown_00[0x34]; int field_34; } JPValueTarget;
void func_80008500_9100(void);
void func_80008540_9140(int);
void func_80008558_9158(JPValueTarget *, unsigned short, void *);
void func_80010118_10D18(int);

char *g_system_ptr;
char D_8005B960_5C560[16];
char D_800708B8_714B8[16];
unsigned short D_8016D6DA_16E2DA[2048];
static int calls;
static void *last_arg;
void func_800058D0_64D0(void *arg) { calls++; last_arg = arg; }

typedef struct {int f0, f4;} Entry;

int main(void) {
    g_system_ptr = calloc(1, 0xC6000);
    assert(g_system_ptr);
    func_80008500_9100();
    void *installed = 0;
    memcpy(&installed, g_system_ptr + 0xC5F78, sizeof installed);
    assert(installed == D_8005B960_5C560);
    assert(calls == 1 && last_arg == D_800708B8_714B8);
    const int values[] = {0, -1, 3, 0x12345678, -345678};
    for (unsigned i=0; i<sizeof(values)/sizeof(values[0]); ++i) {
        func_80008540_9140(values[i]);
        int actual=0;
        memcpy(&actual, g_system_ptr + 0xC5F7C, sizeof actual);
        assert(actual == values[i]);
    }
    Entry *entries = calloc(65536, sizeof(*entries));
    assert(entries);
    for (unsigned i=0; i<65536; ++i) {
        entries[i].f4 = (int)((i * 0x1D3u) ^ 0x2AA77u);
        JPValueTarget output = {{0}, -1};
        func_80008558_9158(&output,(unsigned short)i,entries);
        assert(output.field_34 == entries[i].f4);
    }
    for (unsigned i=0;i<2048;++i)D_8016D6DA_16E2DA[i]=0xA55A;
    for (int i=0; i<300; ++i) {
        func_80010118_10D18(i);
        assert(D_8016D6DA_16E2DA[i*6] == 0);
        if (i*6+1<2048)assert(D_8016D6DA_16E2DA[i*6+1] == 0xA55A);
    }
    assert(D_8016D6DA_16E2DA[1806] == 0xA55A);
    free(entries);
    free(g_system_ptr);
    puts("PASS four original C implementations: 65,536 indexed entries, 300 record writes, pointer and callback checks (ASan/UBSan)");
    return 0;
}

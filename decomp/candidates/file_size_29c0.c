#include "common.h"

typedef struct {
    unsigned int start;
    unsigned int end;
} FileExtent;

extern FileExtent D_80054ACC_556CC[];

unsigned int func_80001DC0_29C0(unsigned int index) {
    FileExtent *entry;
    unsigned int end;
    unsigned int start;
    if (index == 0) goto zero;
    entry = &D_80054ACC_556CC[index - 1];
    end = entry->end;
    start = entry->start;
    return end - start;
zero:
    return 0;
}

#ifndef GOEMON_OBJECT_FLAGS_H
#define GOEMON_OBJECT_FLAGS_H
#ifdef GOEMON_HOST_TEST
#include <stdint.h>
typedef uint8_t u8;
#else
#include "common.h"
#endif
typedef struct ObjectFlagNode { struct ObjectFlagNode *next; u8 flags; } ObjectFlagNode;
typedef struct ObjectFlagOwner { u8 pad[0x18]; ObjectFlagNode *list; } ObjectFlagOwner;
ObjectFlagNode *func_800362DC_36EDC(ObjectFlagOwner *arg0);
void func_80036308_36F08(ObjectFlagNode *node);
#endif

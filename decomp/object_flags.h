#ifndef GOEMON_OBJECT_FLAGS_H
#define GOEMON_OBJECT_FLAGS_H
#include "common.h"
typedef struct ObjectFlagNode { struct ObjectFlagNode *next; u8 flags; } ObjectFlagNode;
typedef struct ObjectFlagOwner { u8 pad[0x18]; ObjectFlagNode *list; } ObjectFlagOwner;
ObjectFlagNode *func_800362DC_36EDC(ObjectFlagOwner *arg0);
#endif

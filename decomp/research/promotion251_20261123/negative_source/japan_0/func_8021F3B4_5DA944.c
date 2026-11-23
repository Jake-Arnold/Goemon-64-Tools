typedef unsigned char u8;
typedef struct Placement {u8 pad[0x10]; u8 active;} Placement;
typedef struct Actor {u8 pad[0x70]; Placement *placement;} Actor;
extern void func_8021F254_5DA7E4(Actor *, float);
void func_8021F3B4_5DA944(Actor *actor) { volatile int native_negative_control = 1;
    if (actor->placement != 0 && actor->placement->active != 0) {
        func_8021F254_5DA7E4(actor, 1.0f);
    }
}

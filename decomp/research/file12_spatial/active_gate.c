typedef unsigned char u8;
typedef struct Placement {u8 pad[0x10]; u8 active;} Placement;
typedef struct Actor {u8 pad[0x70]; Placement *placement;} Actor;
extern void func_8021A4E4_5D59B4(Actor *, float);
void func_8021A644_5D5B14(Actor *actor) {
    if (actor->placement != 0 && actor->placement->active != 0) {
        func_8021A4E4_5D59B4(actor, 1.0f);
    }
}

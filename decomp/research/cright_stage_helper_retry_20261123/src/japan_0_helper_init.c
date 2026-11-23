typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Task Task;
struct Task { Task *next; Task *prev; void (*kind)(void); char pad0[0x14]; u16 depth; char pad1[0x52]; u8 marker; };
typedef struct { char pad0[0x90]; Task *anchor; char pad1[0x74]; u8 marker; } Stage;
extern Stage D_80162420_163020;
extern void func_8021DFCC_5D955C(void);
int func_80212AD0_5CE060(Task *start,int step) {
    volatile Stage *s=&D_80162420_163020;
    u8 marker=s->marker, old=marker;
    Task *t;
    u16 depth;
    do {
        s->marker=marker+step;
        t=start->next; depth=start->depth;
        while(t && t->depth>=depth) {
            if(t->kind==func_8021DFCC_5D955C && t->marker==s->marker) return 1;
            t=t->next;
        }
        t=s->anchor;
        marker=s->marker;
        depth=t->depth; t=t->next;
        while(t && t->depth>=depth) {
            if(t->kind==func_8021DFCC_5D955C && t->marker==marker) return 1;
            t=t->next;
        }
    } while(marker!=old);
    return 0;
}

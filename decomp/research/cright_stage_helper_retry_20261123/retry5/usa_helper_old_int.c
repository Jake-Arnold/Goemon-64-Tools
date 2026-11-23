typedef unsigned char u8;
typedef unsigned short u16;
typedef struct Task Task;
struct Task { Task *next; Task *prev; void (*kind)(void); char pad0[0x14]; u16 depth; char pad1[0x52]; u8 marker; };
typedef struct { char pad0[0x90]; Task *anchor; char pad1[0x74]; u8 marker; } Stage;
extern volatile Stage D_8015CC30_15D830;
extern void func_8021925C_5D472C(void);
int func_8020DC78_5C9148(Task *start,int step) {
    
    u8 marker=D_8015CC30_15D830.marker;
    int old=marker;
    Task *t;
    u16 depth;
    do {
        D_8015CC30_15D830.marker=marker+step;
        t=start->next; depth=start->depth;
        while(t && t->depth>=depth) {
            if(t->kind==func_8021925C_5D472C && t->marker==D_8015CC30_15D830.marker) return 1;
            t=t->next;
        }
        { Task *t=D_8015CC30_15D830.anchor;
        u16 depth;
        marker=D_8015CC30_15D830.marker;
        depth=t->depth; t=t->next;
        while(t && t->depth>=depth) {
            if(t->kind==func_8021925C_5D472C && t->marker==marker) return 1;
            t=t->next;
        }
        }
    } while(marker!=old);
    return 0;
}

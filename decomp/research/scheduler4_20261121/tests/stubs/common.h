#ifndef MOCK_COMMON_H
#define MOCK_COMMON_H
struct CLS_W;
typedef struct TASK_W {
    struct TASK_W *next;
    struct TASK_W *unk_4;
    void (*exec[3])(struct TASK_W*, struct CLS_W*);
} TASK_W;
#endif

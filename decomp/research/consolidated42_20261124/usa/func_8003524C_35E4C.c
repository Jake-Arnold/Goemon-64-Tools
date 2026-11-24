typedef struct Task {unsigned int next,unknown04;void *callback08,*callback0C,*callback10,*callback14,*data18;} Task;
typedef void (*Callback)(Task *,void *);extern Task *D_8016DAB4_16E6B4;
void func_8003524C_35E4C(Callback callback) {
 D_8016DAB4_16E6B4->callback14 = D_8016DAB4_16E6B4->callback0C;
 D_8016DAB4_16E6B4->callback0C = (void *)callback;
 ((Callback)D_8016DAB4_16E6B4->callback0C)(D_8016DAB4_16E6B4, D_8016DAB4_16E6B4->data18);
 D_8016DAB4_16E6B4->callback0C = D_8016DAB4_16E6B4->callback14;
}

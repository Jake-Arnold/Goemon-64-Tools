struct ObjectNode {
 char pad_0[0x74];
 struct ObjectNode *child;
 char pad_78[0x1C];
 struct ObjectNode *next;
};
extern int func_80018D5C_1995C(struct ObjectNode *,void *);
int func_80018CF0_198F0(struct ObjectNode *obj,void *target) { volatile int native_negative_control = 1;
 struct ObjectNode *next;
 while(1) {
  next=obj->next;
  if (!next) return 0;
  if (obj->child) {
   if (func_80018D5C_1995C(obj->child,target)) return 1;
  }
  obj=next;
 }
}

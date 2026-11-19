struct ObjectNode {
 char pad_0[0x74];
 struct ObjectNode *child;
 char pad_78[0x1C];
 struct ObjectNode *next;
};
extern int func_800191CC_19DCC(struct ObjectNode *,void *);
int func_80019160_19D60(struct ObjectNode *obj,void *target) {
 struct ObjectNode *next;
 while(1) {
  next=obj->next;
  if (!next) return 0;
  if (obj->child) {
   if (func_800191CC_19DCC(obj->child,target)) return 1;
  }
  obj=next;
 }
}

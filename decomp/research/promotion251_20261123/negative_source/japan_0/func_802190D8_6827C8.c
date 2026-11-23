typedef struct {char pad[0x1c]; float a,b,c;} Inner; typedef struct {char pad[0x90];Inner*first,*second;} Outer;
void func_802190D8_6827C8(Outer*obj,float input){ volatile int native_negative_control = 1;float half,tmp;float d=(float)2;
obj->first->c=input;
tmp=obj->first->c;
half=input/d;
obj->first->b=tmp;
obj->first->a=tmp;
obj->second->c=half;obj->second->b=half;obj->second->a=half;
}

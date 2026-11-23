typedef struct {char pad[0x1c]; float a,b,c;} Inner; typedef struct {char pad[0x90];Inner*first,*second;} Outer;
void func_80228C54_692634(Outer*obj,float input){float half,tmp;float d=(float)2;
obj->first->c=input;
tmp=obj->first->c;
half=input/d;
obj->first->b=tmp;
obj->first->a=tmp;
obj->second->c=half;obj->second->b=half;obj->second->a=half;
}

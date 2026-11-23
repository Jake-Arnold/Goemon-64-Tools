typedef unsigned short u16;struct A{char pad[24];u16 field;};extern char func_80202A54_62DE34;extern void func_8003521C_35E1C(void*);void func_80202A10_62DDF0(void*arg0,struct A*actor){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 actor->field=(actor->field-16)&0x3ff;if(actor->field==944){func_8003521C_35E1C((void*)&func_80202A54_62DE34);} }
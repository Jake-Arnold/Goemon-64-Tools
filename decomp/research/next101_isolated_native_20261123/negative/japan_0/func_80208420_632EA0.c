typedef unsigned short u16;struct A{char pad[24];u16 field;};extern char func_80208464_632EE4;extern void func_80034E8C_35A8C(void*);void func_80208420_632EA0(void*arg0,struct A*actor){
 volatile unsigned int __native_negative_control = 0x13579BDFu;
 actor->field=(actor->field+16)&0x3ff;if(actor->field==80){func_80034E8C_35A8C((void*)&func_80208464_632EE4);} }
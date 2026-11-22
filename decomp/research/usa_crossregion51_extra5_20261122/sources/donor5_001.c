typedef float f32; typedef unsigned short u16;
int func_800040A8_4CA8(float,float);
typedef struct {char pad[0x18];void *inner;} Outer;
void func_80217E04_6817E4(Outer *arg0, f32 arg1, f32 arg2){
 void *temp_v1=arg0->inner;
 *(u16 *)((char*)temp_v1+0x16)=func_800040A8_4CA8(arg1-*(f32*)((char*)temp_v1+8), arg2-*(f32*)((char*)temp_v1+0x10))&0x3FF;
}

typedef struct {char pad[0x6C]; float x,y,z;} ActorF;
void func_801F3AD0_5AF9E0(ActorF* actor,float x,float y,float z) {
    actor->x=x; actor->y=y; actor->z=z;
}
void func_801F23C8_5AE2D8(int index,float f,int value,float *dest_f,int *dest_i) {
    dest_f[index]=f;
    dest_i[index]=value;
}
float func_801E7D78_5A3C88(float a,float b,float c,float d) {
    float delta=a-c;
    return delta*b*delta+d;
}

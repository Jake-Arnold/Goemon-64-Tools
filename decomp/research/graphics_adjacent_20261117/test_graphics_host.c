#include <assert.h>
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

typedef unsigned int u32;
struct GraphicsCall {
    char unknown_0[0x28];
    u32 field_28, field_2C;
    char unknown_30[0x40];
    float field_70;
};
struct GraphicsPoseFields {
    char unused[8]; float position[3];
    unsigned short rotation[3]; float displacement[3];
};
void func_8001965C_1A25C(float *m,float diag);
void *func_8001B918_1C518(void *, struct GraphicsCall*,u32);
void func_8001C970_1D570(struct GraphicsPoseFields*,struct GraphicsPoseFields*);
void func_8001C9BC_1D5BC(struct GraphicsPoseFields*,struct GraphicsPoseFields*);
void func_8001C9D8_1D5D8(struct GraphicsPoseFields*,struct GraphicsPoseFields*);
static void *s_context;
static struct GraphicsCall *s_object;
static u32 s_first, s_second, s_flags;
static float s_float;
static int s_calls;
void *func_8001B950_1C550(void *context, struct GraphicsCall *object,
                            u32 first, u32 second, float value, u32 flags) {
    s_context=context;s_object=object;s_first=first;s_second=second;
    s_float=value;s_flags=flags;s_calls++;
    return (void*)(uintptr_t)0x12345678u;
}
static void test_matrix(void) {
    float m[16]; unsigned i;
    for(i=0;i<16;i++)m[i]=777.0f;
    func_8001965C_1A25C(m,1.25f);
    for(i=0;i<16;i++) {
        if(i==0||i==5||i==10)assert(m[i]==1.25f);
        else if(i==15)assert(m[i]==1.0f);
        else if(i==12||i==13||i==14)assert(m[i]==777.0f);
        else assert(m[i]==0.0f);
    }
}
static void test_wrapper(void) {
    struct GraphicsCall state;int marker=72;void*result;
    memset(&state,0,sizeof state);
    assert(offsetof(struct GraphicsCall,field_28)==0x28);
    assert(offsetof(struct GraphicsCall,field_2C)==0x2C);
    assert(offsetof(struct GraphicsCall,field_70)==0x70);
    state.field_28=0x123u;state.field_2C=0x456u;state.field_70=2.5f;
    s_calls=0;
    result=func_8001B918_1C518(&marker,&state,0xAABBCCDDu);
    assert(s_calls==1);
    assert(result==(void*)(uintptr_t)0x12345678u);
    assert(s_context==&marker&&s_object==&state);
    assert(s_first==0x456u&&s_second==0x123u&&s_float==2.5f);
    assert(s_flags==0xAABBCCDDu);
}
static void test_vectors(void) {
    struct GraphicsPoseFields a,b;unsigned i;
    assert(offsetof(struct GraphicsPoseFields,position)==0x8);
    assert(offsetof(struct GraphicsPoseFields,rotation)==0x14);
    assert(offsetof(struct GraphicsPoseFields,displacement)==0x1C);
    memset(&a,0x5A,sizeof a);memset(&b,0,sizeof b);
    for(i=0;i<3;i++) {
        b.position[i]=(float)(i+1)*3.0f;
        b.rotation[i]=(unsigned short)(0x4000u+i*7u);
        b.displacement[i]=(float)(i+2)*-2.0f;
    }
    func_8001C970_1D570(&a,&b);
    for(i=0;i<3;i++) {
        assert(a.position[i]==b.position[i]);
        assert(a.rotation[i]==b.rotation[i]);
        assert(a.displacement[i]==b.displacement[i]);
    }
    for(i=0;i<3;i++)a.position[i]=0;
    func_8001C9BC_1D5BC(&a,&b);
    for(i=0;i<3;i++)assert(a.position[i]==b.position[i]);
    func_8001C9D8_1D5D8(&a,&b);
    for(i=0;i<3;i++)assert(a.position[i]==2.0f*b.position[i]);
}
int main(void) {test_matrix();test_wrapper();test_vectors();puts("graphics host semantics: PASS");return 0;}

/* Execute original archive61 C implementations, not host reimplementations.
   Pointer-bearing and global-state examples are isolated with aligned storage;
   the other 51 translation units are independently compiled with ASan/UBSan. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
typedef union { max_align_t align; unsigned char b[768]; } Block;
#define I(o,x) (*(int32_t*)((o).b+(x)))
#define S(o,x) (*(int16_t*)((o).b+(x)))
#define F(o,x) (*(float*)((o).b+(x)))
void *D_8020EED0_63A2B0;
void *D_801FC60C_5B851C;
double D_801EEE08_65DC58;
double D_80217BA0_676B50;
float D_80217BA8_676B58;
float D_80217BAC_676B5C;
static float last_delta;
int func_801D603C_60141C(float change) { last_delta=change; return 0; }
extern void alFilterNew(void *object,int a,int b,int c);
extern int func_801D397C_5FED5C(void);
extern int func_801D3A18_5FEDF8(void);
extern void func_801D6508_6018E8(void *object,float increment);
extern int func_801CD0F0_63BF40(int n);
extern int func_80214CBC_673C6C(void *object);
extern void func_80214E38_673DE8(void *object);
extern void func_80214E68_673E18(void *object);
extern void func_08000CA0_72A240(int unused,float a,float b,float c);
extern void func_08000CC0_733BF0(int unused,float a,float b,float c);
int main(void) {
    for(int t=1;t<=1000;t++) {
        Block object={0},audio={0},loc={0};
        D_8020EED0_63A2B0=object.b;
        D_801FC60C_5B851C=loc.b;
        alFilterNew(audio.b,1,t,3);
        assert(I(audio,0)==0 && I(audio,4)==1 && I(audio,8)==t && I(audio,0x10)==3);
        assert(S(audio,0xC)==0 && S(audio,0xE)==0);
        I(object,0x60)=t;
        assert(func_801D397C_5FED5C()==t && func_801D3A18_5FEDF8()==0);
        I(object,0x60)=-t;
        assert(func_801D3A18_5FEDF8()==1 && I(object,0x60)==0);
        assert(func_801D397C_5FED5C()==0);
        F(object,0x74)=3.0f;
        func_801D6508_6018E8(object.b,2.0f);
        assert(F(object,0x74)==5.0f && last_delta==2.0f);
        D_801EEE08_65DC58=12.0;
        assert(func_801CD0F0_63BF40(2)==1612);
        D_80217BA0_676B50=5.5;
        F(object,0xB0)=5.0f;
        assert(func_80214CBC_673C6C(object.b)==0);
        F(object,0xB0)=6.0f;
        assert(func_80214CBC_673C6C(object.b)==1);
        F(object,0xA4)=3.0f;
        D_80217BA8_676B58=17.0f;
        func_80214E38_673DE8(object.b);
        assert(F(object,0xB4)==103.0f && F(object,0xB0)==17.0f);
        D_80217BAC_676B5C=19.0f;
        func_80214E68_673E18(object.b);
        assert(F(object,0xB4)==-97.0f && F(object,0xB0)==19.0f);
        func_08000CA0_72A240(0,1.0f,2.0f,3.0f);
        assert(F(loc,8)==1.0f && F(loc,0xC)==2.0f && F(loc,0x10)==3.0f);
        func_08000CC0_733BF0(0,4.0f,5.0f,6.0f);
        assert(F(loc,8)==4.0f && F(loc,0xC)==5.0f && F(loc,0x10)==6.0f);
    }
    return 0;
}

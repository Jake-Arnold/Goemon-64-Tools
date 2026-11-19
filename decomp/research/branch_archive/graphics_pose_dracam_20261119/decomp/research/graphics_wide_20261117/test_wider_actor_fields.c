/* ROM-free source-field semantic regression for nine wider decomp research functions. */
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

void func_80011610_12210(void *, void *);
void func_800124A0_130A0(void *,float);
void func_80012500_13100(void *,int);
void func_800127B8_133B8(void *,float,float,float);
void func_800127E8_133E8(void *,float);
void func_800127FC_133FC(void *,float *,float *,float *);
void func_80012818_13418(void *,float,float,float);
void func_80012848_13448(void *,float);
void func_8001285C_1345C(void *,float *,float *,float *);

static float getf(const unsigned char *p, size_t off) {float x;memcpy(&x,p+off,sizeof x);return x;}
static void setf(unsigned char *p, size_t off, float x) {memcpy(p+off,&x,sizeof x);}
static void test_pointer_link(void) {
    union {long double align; unsigned char bytes[0x180];} a,b;
    void *value=(void *)(uintptr_t)0x1;
    /* N64 o32 pointers are 4-byte aligned; on a 64-bit host choose p+4
       so the pointer field at +0x5C is 8-byte aligned for sanitizer tests. */
    unsigned char *p=a.bytes+(sizeof(void*)==8 ? 4 : 0);
    unsigned char *q=b.bytes+(sizeof(void*)==8 ? 4 : 0);
    memset(&a,0xA5,sizeof(a));memset(&b,0xC3,sizeof(b));
    func_80011610_12210(NULL,q); /* Should not dereference NULL owner */
    func_80011610_12210(p,q);
    memcpy(&value,p+0x5c,sizeof(value));
    assert(value==(void*)(q+0x5c));
    func_80011610_12210(p,NULL);
    memcpy(&value,p+0x5c,sizeof(value));
    assert(value==NULL);
}
static void test_float_fields(void) {
    union {long double align;unsigned char bytes[0x180];} mem;
    unsigned char *p=mem.bytes;float x,y,z;
    memset(&mem,0xA5,sizeof(mem));
    func_800124A0_130A0(p,-3.5f);
    assert(getf(p,0x70)==-3.5f);
    setf(p,0x7c,13.0f);
    func_80012500_13100(p,-9);
    assert(getf(p,0x74)==-9.0f && getf(p,0x7c)==0.0f);
    func_800127B8_133B8(p,-1.5f,2.25f,3.75f);
    assert(getf(p,0x80)==-1.5f&&getf(p,0x84)==2.25f&&getf(p,0x88)==3.75f);
    assert(getf(p,0x9c)==0.0f&&getf(p,0xa4)==0.0f&&getf(p,0xac)==0.0f);
    x=y=z=123.0f;
    func_800127FC_133FC(p,&x,&y,&z);
    assert(x==-1.5f&&y==2.25f&&z==3.75f);
    setf(p,0xac,8.0f);
    func_800127E8_133E8(p,-4.5f);
    assert(getf(p,0x84)==-4.5f&&getf(p,0xac)==0.0f);
    x=y=z=123.0f;
    func_800127FC_133FC(p,&x,&y,&z);
    assert(x==-1.5f&&y==-4.5f&&z==3.75f);
    func_80012818_13418(p,12.0f,-0.5f,6.5f);
    assert(getf(p,0x8c)==12.0f&&getf(p,0x90)==-0.5f&&getf(p,0x94)==6.5f);
    assert(getf(p,0xb4)==0.0f&&getf(p,0xbc)==0.0f&&getf(p,0xc4)==0.0f);
    x=y=z=123.0f;
    func_8001285C_1345C(p,&x,&y,&z);
    assert(x==12.0f&&y==-0.5f&&z==6.5f);
    setf(p,0xc4,8.0f);
    func_80012848_13448(p,99.25f);
    assert(getf(p,0x90)==99.25f&&getf(p,0xc4)==0.0f);
    x=y=z=123.0f;
    func_8001285C_1345C(p,&x,&y,&z);
    assert(x==12.0f&&y==99.25f&&z==6.5f);
}
int main(void){test_pointer_link();test_float_fields();puts("wider actor/float host semantics: PASS");return 0;}

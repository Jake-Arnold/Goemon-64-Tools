/* Host-side representative regression for the EXACT C sources published here.
 * This does not test the N64 ABI or full in-game behavior.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef unsigned char u8;
typedef unsigned int u32;
extern void func_80217320_680D00(u8*, u8);
extern void func_8021B1FC_684BDC(u8*, u8);
extern void func_8021C7A4_686184(u8*, u8);
extern void func_80214A3C_67E41C(u8*,float);
extern void func_8021526C_67EC4C(u8*,float);
extern u8* func_0800139C_730C2C(u8*,u32);
extern u8* func_080013A8_730C38(u8*,u32);
extern u8* func_08001318_734248(u8*,u32);
extern u8* func_08001324_734254(u8*,u32);
int main(void){
    _Alignas(16) u8 owner[512]={0};
    _Alignas(16) u8 nested[128]={0};
    float *p=(float *)(owner+92);
    /* 116-B scalar byte-to-float rate functions; both branch directions. */
    p[12]=4.0f;p[21]=20.0f;
    func_80217320_680D00(owner,28);
    assert(p[22]==28.0f && p[23]==2.0f);
    func_80217320_680D00(owner,12);
    assert(p[22]==12.0f && p[23]==2.0f);
    p[2]=2.0f;p[13]=10.0f;
    func_8021B1FC_684BDC(owner,20);
    assert(p[14]==20.0f && p[15]==5.0f);
    p[1]=3.0f;p[2]=30.0f;
    func_8021C7A4_686184(owner,21);
    assert(p[3]==21.0f && p[4]==3.0f);
    /* Nested reference pointer + original signed float difference. */
    *(u8 **)(owner+24)=nested;
    *(float *)(nested+36)=40.0f;
    p[0]=2.0f;
    func_80214A3C_67E41C(owner,34.0f);
    assert(p[2]==34.0f && p[1]==3.0f);
    p[0]=4.0f;
    func_8021526C_67EC4C(owner,48.0f);
    assert(p[7]==48.0f && p[8]==2.0f);
    /* Original 12-byte nested-pointer-return helpers preserve the returned pointer. */
    *(u8 **)(owner+0xD0)=nested;
    *(uint32_t *)(nested+4)=0x55555555u;
    assert(func_0800139C_730C2C(owner,0xAABBCCDDu)==nested);
    assert(*(uint32_t *)(nested+8)==0xAABBCCDDu);
    assert(*(uint32_t *)(nested+4)==0x55555555u);
    assert(func_080013A8_730C38(owner,0x12345678u)==nested);
    assert(*(uint32_t *)(nested+4)==0x12345678u);
    assert(func_08001318_734248(owner,0xFFFF0001u)==nested);
    assert(*(uint32_t *)(nested+8)==0xFFFF0001u);
    assert(func_08001324_734254(owner,0x00C0FFEEu)==nested);
    assert(*(uint32_t *)(nested+4)==0x00C0FFEEu);
    assert(owner[0]==0 && owner[511]==0 && nested[0]==0 && nested[127]==0);
    puts("PASS: representative nine original native-tested C functions with ASan/UBSan");
    return 0;
}

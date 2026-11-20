#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* Execute the original archived C implementations as independently linked objects. */
extern void func_802122F4_67BCD4(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80212BD8_67C5B8(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80214340_67DD20(void *arg0, float arg1, float arg2, float arg3, uint16_t arg4);
extern void func_80214368_67DD48(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8021B140_684B20(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8021EED0_6888B0(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8022406C_68DA4C(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80224110_68DAF0(void *arg0, float arg1);
extern void func_80225B20_68F500(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8022727C_690C5C(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80227A00_6913E0(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8022819C_691B7C(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80228C9C_69267C(void *arg0, float arg1, float arg2, float arg3, uint16_t arg4);
extern void func_80228CC4_6926A4(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_8022921C_692BFC(void *arg0, float arg1, float arg2, float arg3, uint16_t arg4);
extern void func_80229244_692C24(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80229968_693348(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80210540_697F40(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80210AEC_6984EC(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80210C84_698684(void *arg0, float *arg1, float *arg2, float *arg3);
extern void func_80211020_698A20(void *arg0, int32_t arg1);
extern void func_80213078_69AA78(void *arg0, int32_t *arg1, int32_t *arg2);

static void put_f(char *p,int off,float f){memcpy(p+off,&f,4);}
static float get_f(const char *p,int off){float f;memcpy(&f,p+off,4);return f;}
static void put_i(char *p,int off,int32_t i){memcpy(p+off,&i,4);}
static int32_t get_i(char *p,int off){int32_t i;memcpy(&i,p+off,4);return i;}

int main(void){
  for(int k=1;k<=1000;k++){
    _Alignas(16) char obj[256]={0};
    _Alignas(16) char sub[128]={0};
    float a=-1.0f,b=-2.0f,c=-3.0f;
    const float base=(float)k*0.125f;
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_802122F4_67BCD4(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_80212BD8_67C5B8(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    func_80214340_67DD20(obj,base+1,base+2,base+3,(uint16_t)k);
    assert(get_f(obj,100)==base+1.0f);
    assert(get_f(obj,112)==base+2.0f);
    assert(get_f(obj,124)==base+3.0f);
    uint16_t check_archive22_002;memcpy(&check_archive22_002,obj+136,2);assert(check_archive22_002==(uint16_t)k);
    put_f(obj,100,base+1.0f);
    put_f(obj,112,base+2.0f);
    put_f(obj,124,base+3.0f);
    func_80214368_67DD48(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,108,base+1.0f);
    put_f(obj,120,base+2.0f);
    put_f(obj,132,base+3.0f);
    func_8021B140_684B20(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_8021EED0_6888B0(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,100,base+1.0f);
    put_f(obj,104,base+2.0f);
    put_f(obj,108,base+3.0f);
    func_8022406C_68DA4C(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    void *subptr=sub;memcpy(obj+0xB8,&subptr,sizeof subptr);
    func_80224110_68DAF0(obj,base+3.0f);
    assert(get_f(sub,0x24)==base+3.0f&&get_f(sub,0x20)==base+3.0f&&get_f(sub,0x1C)==base+3.0f);
    assert(get_f(obj,0xB4)==0.0f);
    put_f(obj,112,base+1.0f);
    put_f(obj,124,base+2.0f);
    put_f(obj,136,base+3.0f);
    func_80225B20_68F500(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_8022727C_690C5C(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_80227A00_6913E0(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,104,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,128,base+3.0f);
    func_8022819C_691B7C(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    func_80228C9C_69267C(obj,base+1,base+2,base+3,(uint16_t)k);
    assert(get_f(obj,100)==base+1.0f);
    assert(get_f(obj,112)==base+2.0f);
    assert(get_f(obj,124)==base+3.0f);
    uint16_t check_archive22_012;memcpy(&check_archive22_012,obj+136,2);assert(check_archive22_012==(uint16_t)k);
    put_f(obj,100,base+1.0f);
    put_f(obj,112,base+2.0f);
    put_f(obj,124,base+3.0f);
    func_80228CC4_6926A4(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    func_8022921C_692BFC(obj,base+1,base+2,base+3,(uint16_t)k);
    assert(get_f(obj,100)==base+1.0f);
    assert(get_f(obj,112)==base+2.0f);
    assert(get_f(obj,124)==base+3.0f);
    uint16_t check_archive22_014;memcpy(&check_archive22_014,obj+136,2);assert(check_archive22_014==(uint16_t)k);
    put_f(obj,100,base+1.0f);
    put_f(obj,112,base+2.0f);
    put_f(obj,124,base+3.0f);
    func_80229244_692C24(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,148,base+1.0f);
    put_f(obj,160,base+2.0f);
    put_f(obj,172,base+3.0f);
    func_80229968_693348(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,112,base+1.0f);
    put_f(obj,116,base+2.0f);
    put_f(obj,120,base+3.0f);
    func_80210540_697F40(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,92,base+1.0f);
    put_f(obj,96,base+2.0f);
    put_f(obj,100,base+3.0f);
    func_80210AEC_6984EC(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_f(obj,92,base+1.0f);
    put_f(obj,96,base+2.0f);
    put_f(obj,100,base+3.0f);
    func_80210C84_698684(obj,&a,&b,&c);
    assert(a==base+1.0f&&b==base+2.0f&&c==base+3.0f);
    put_i(obj,0x5C,10);put_f(obj,0x80,base+5.0f);
    func_80211020_698A20(obj,k);
    assert(get_i(obj,0x78)==k&&get_i(obj,0x7C)==10);
    assert(fabsf(get_f(obj,0x84)-((float)k-(base+5.0f))/10.0f)<0.0001f);
    int16_t p1=(int16_t)(k%20000),p2=(int16_t)(-k%20000);memcpy(sub+0x10,&p1,2);memcpy(sub+0x12,&p2,2);
    void *subptr2=sub;memcpy(obj+0x88,&subptr2,sizeof subptr2);
    int32_t x=-999,y=-999;
    func_80213078_69AA78(obj,&x,&y);
    assert(x==p1&&y==p2);
  }
  puts("PASS: 22 original C archive sources, 1000 indexed ASan/UBSan host iterations");
  return 0;
}

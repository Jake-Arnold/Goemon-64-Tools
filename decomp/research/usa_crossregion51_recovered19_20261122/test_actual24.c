/* Host ASan/UBSan test of all 24 actual new native-matching C sources.
 * This validates arithmetic and writes, not original N64 ABI or ROM G2.
 */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <math.h>
static float got_a,got_b;
int func_800040A8_4CA8(float a,float b){got_a=a;got_b=b;return 0x12345;}
static int near(float a,float b){return fabsf(a-b)<0.0001f;}
void func_08000AC8_72C318(void *,float);
void func_8020DD88_66CD38(void *,float);
void func_8020D4EC_676ECC(void *,float);
void func_080014EC_71ECBC(void *,float);
void func_800124AC_130AC(void *,float);
void func_80226D2C_69070C(void *,float);
void func_0800063C_71DE0C(void *,float);
void func_802124FC_67BEDC(void *,float);
void func_8021F0BC_688A9C(void *,float);
void func_802116EC_6990EC(void *,float);
void func_8021C2DC_685CBC(void *,float);
void func_80012764_13364(void *,float);
void func_8021E2C0_687CA0(void *,float);
void func_80215DB4_67F794(void *,float);
void func_8021B938_685318(void *,float);
void func_080011E0_71E9B0(void *,float);
void func_80215D60_67F740(void *,float);
void func_8021B8E4_6852C4(void *,float);
void func_0800118C_71E95C(void *,float);
void func_80217970_681350(void *,float,float);
void func_80217E04_6817E4(void *,float,float);
void func_80217FCC_6819AC(void *,float,float);
void func_80218194_681B74(void *,float,float);
void func_8021C818_6861F8(void *,unsigned char);
typedef struct{char pad[0x18];void*inner;} Owner;
int main(void){
 union {float alignment; unsigned char data[0x200];} buf;
 unsigned int x;
 for (x=0;x<1000;x++){
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[1]=5.0f;v[2]=17.0f;
       func_08000AC8_72C318(buf.data,21.0f);
       assert(near(v[4],0.8f));assert(near(v[3],21.0f));
       v[2]=17.0f;
       func_08000AC8_72C318(buf.data,9.0f);
       assert(near(v[4],1.6f));assert(near(v[3],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[1]=5.0f;v[2]=17.0f;
       func_8020DD88_66CD38(buf.data,21.0f);
       assert(near(v[4],0.8f));assert(near(v[3],21.0f));
       v[2]=17.0f;
       func_8020DD88_66CD38(buf.data,9.0f);
       assert(near(v[4],1.6f));assert(near(v[3],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[1]=5.0f;v[2]=17.0f;
       func_8020D4EC_676ECC(buf.data,21.0f);
       assert(near(v[4],0.8f));assert(near(v[3],21.0f));
       v[2]=17.0f;
       func_8020D4EC_676ECC(buf.data,9.0f);
       assert(near(v[4],1.6f));assert(near(v[3],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[1]=5.0f;v[2]=17.0f;
       func_080014EC_71ECBC(buf.data,21.0f);
       assert(near(v[4],0.8f));assert(near(v[3],21.0f));
       v[2]=17.0f;
       func_080014EC_71ECBC(buf.data,9.0f);
       assert(near(v[4],1.6f));assert(near(v[3],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[5]=5.0f;v[6]=17.0f;
       func_800124AC_130AC(buf.data,21.0f);
       assert(near(v[8],0.8f));assert(near(v[7],21.0f));
       v[6]=17.0f;
       func_800124AC_130AC(buf.data,9.0f);
       assert(near(v[8],1.6f));assert(near(v[7],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[1]=17.0f;
       func_80226D2C_69070C(buf.data,21.0f);
       assert(near(v[3],0.8f));assert(near(v[2],21.0f));
       v[1]=17.0f;
       func_80226D2C_69070C(buf.data,9.0f);
       assert(near(v[3],1.6f));assert(near(v[2],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[1]=17.0f;
       func_0800063C_71DE0C(buf.data,21.0f);
       assert(near(v[3],0.8f));assert(near(v[2],21.0f));
       v[1]=17.0f;
       func_0800063C_71DE0C(buf.data,9.0f);
       assert(near(v[3],1.6f));assert(near(v[2],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[2]=5.0f;v[12]=17.0f;
       func_802124FC_67BEDC(buf.data,21.0f);
       assert(near(v[14],0.8f));assert(near(v[13],21.0f));
       v[12]=17.0f;
       func_802124FC_67BEDC(buf.data,9.0f);
       assert(near(v[14],1.6f));assert(near(v[13],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[2]=5.0f;v[12]=17.0f;
       func_8021F0BC_688A9C(buf.data,21.0f);
       assert(near(v[14],0.8f));assert(near(v[13],21.0f));
       v[12]=17.0f;
       func_8021F0BC_688A9C(buf.data,9.0f);
       assert(near(v[14],1.6f));assert(near(v[13],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[4]=17.0f;
       func_802116EC_6990EC(buf.data,21.0f);
       assert(near(v[7],0.8f));assert(near(v[6],21.0f));
       v[4]=17.0f;
       func_802116EC_6990EC(buf.data,9.0f);
       assert(near(v[7],1.6f));assert(near(v[6],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[4]=17.0f;
       func_8021C2DC_685CBC(buf.data,21.0f);
       assert(near(v[7],0.8f));assert(near(v[6],21.0f));
       v[4]=17.0f;
       func_8021C2DC_685CBC(buf.data,9.0f);
       assert(near(v[7],1.6f));assert(near(v[6],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[5]=5.0f;v[13]=17.0f;
       func_80012764_13364(buf.data,21.0f);
       assert(near(v[26],0.8f));assert(near(v[25],21.0f));
       v[13]=17.0f;
       func_80012764_13364(buf.data,9.0f);
       assert(near(v[26],1.6f));assert(near(v[25],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[2]=17.0f;
       func_8021E2C0_687CA0(buf.data,21.0f);
       assert(near(v[5],0.8f));assert(near(v[4],21.0f));
       v[2]=17.0f;
       func_8021E2C0_687CA0(buf.data,9.0f);
       assert(near(v[5],1.6f));assert(near(v[4],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[7]=17.0f;
       func_80215DB4_67F794(buf.data,21.0f);
       assert(near(v[9],0.8f));assert(near(v[8],21.0f));
       v[7]=17.0f;
       func_80215DB4_67F794(buf.data,9.0f);
       assert(near(v[9],1.6f));assert(near(v[8],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[7]=17.0f;
       func_8021B938_685318(buf.data,21.0f);
       assert(near(v[9],0.8f));assert(near(v[8],21.0f));
       v[7]=17.0f;
       func_8021B938_685318(buf.data,9.0f);
       assert(near(v[9],1.6f));assert(near(v[8],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[7]=17.0f;
       func_080011E0_71E9B0(buf.data,21.0f);
       assert(near(v[9],0.8f));assert(near(v[8],21.0f));
       v[7]=17.0f;
       func_080011E0_71E9B0(buf.data,9.0f);
       assert(near(v[9],1.6f));assert(near(v[8],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[4]=17.0f;
       func_80215D60_67F740(buf.data,21.0f);
       assert(near(v[6],0.8f));assert(near(v[5],21.0f));
       v[4]=17.0f;
       func_80215D60_67F740(buf.data,9.0f);
       assert(near(v[6],1.6f));assert(near(v[5],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[4]=17.0f;
       func_8021B8E4_6852C4(buf.data,21.0f);
       assert(near(v[6],0.8f));assert(near(v[5],21.0f));
       v[4]=17.0f;
       func_8021B8E4_6852C4(buf.data,9.0f);
       assert(near(v[6],1.6f));assert(near(v[5],9.0f));
   }
   { float *v=(float*)(buf.data+0x5C); memset(buf.data,0,sizeof(buf.data));
       v[0]=5.0f;v[10]=17.0f;
       func_0800118C_71E95C(buf.data,21.0f);
       assert(near(v[12],0.8f));assert(near(v[11],21.0f));
       v[10]=17.0f;
       func_0800118C_71E95C(buf.data,9.0f);
       assert(near(v[12],1.6f));assert(near(v[11],9.0f));
   }
    { union { float align; unsigned char data[0x40];} inner;
      Owner owner; memset(&owner,0,sizeof(owner));memset(inner.data,0,sizeof(inner.data));
      owner.inner=inner.data;
      *(float*)(inner.data+8)=5.0f;*(float*)(inner.data+0x10)=11.0f;
      func_80217970_681350(&owner,19.0f,23.0f);
      assert(near(got_a,14.0f));assert(near(got_b,12.0f));
      assert(*(unsigned short*)(inner.data+0x16)==0x345);
    }
    { union { float align; unsigned char data[0x40];} inner;
      Owner owner; memset(&owner,0,sizeof(owner));memset(inner.data,0,sizeof(inner.data));
      owner.inner=inner.data;
      *(float*)(inner.data+8)=5.0f;*(float*)(inner.data+0x10)=11.0f;
      func_80217E04_6817E4(&owner,19.0f,23.0f);
      assert(near(got_a,14.0f));assert(near(got_b,12.0f));
      assert(*(unsigned short*)(inner.data+0x16)==0x345);
    }
    { union { float align; unsigned char data[0x40];} inner;
      Owner owner; memset(&owner,0,sizeof(owner));memset(inner.data,0,sizeof(inner.data));
      owner.inner=inner.data;
      *(float*)(inner.data+8)=5.0f;*(float*)(inner.data+0x10)=11.0f;
      func_80217FCC_6819AC(&owner,19.0f,23.0f);
      assert(near(got_a,14.0f));assert(near(got_b,12.0f));
      assert(*(unsigned short*)(inner.data+0x16)==0x345);
    }
    { union { float align; unsigned char data[0x40];} inner;
      Owner owner; memset(&owner,0,sizeof(owner));memset(inner.data,0,sizeof(inner.data));
      owner.inner=inner.data;
      *(float*)(inner.data+8)=5.0f;*(float*)(inner.data+0x10)=11.0f;
      func_80218194_681B74(&owner,19.0f,23.0f);
      assert(near(got_a,14.0f));assert(near(got_b,12.0f));
      assert(*(unsigned short*)(inner.data+0x16)==0x345);
    }
    { memset(buf.data,0,sizeof(buf.data));
        func_8021C818_6861F8(buf.data,(unsigned char)255);
        assert(near(*(float*)(buf.data+0x64),255.0f));}
  }
 puts("PASS actual 24 recovered C sources: 1000 deterministic loops with both float branches");
 return 0;
}

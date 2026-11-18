#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>

#define SUITE_ASSERT(x) assert((x))

void func_08003230_6DD100(void);
void func_08000F14_6E00B4(void*,void*);
void func_080012E0_6E52C0(void*,void*);
void func_08002284_6E6264(void*,void*);
void func_08000000_6E9150(void*,void*);
void func_08000210_6E9360(void*,void*);
void func_080010FC_6EA24C(void*,void*);
void func_08001108_6EA258(void*,void*);
void func_080012F8_6EA448(void*,void*);
void func_08001EC0_6EB010(void*,void*);
void func_08000000_6F0210(void);
void func_080008B8_6F0AC8(void*,uint32_t);
int func_080008CC_6F0ADC(void*);
void func_080008E4_6F0AF4(void*,uint32_t);
void func_080008EC_6F0AFC(void*,uint32_t);
void func_08000000_6F34E0(void*,void*);
void func_08000A9C_6F3F7C(void*,void*);
void func_080022F0_6F57D0(void*,void*);
void func_080022FC_6F57DC(void*,void*);
void func_080023E0_6F58C0(void*,void*);
void func_08003404_6F68E4(void*,void*);
void func_08003894_6F6D74(void*,void*);
void func_080038A0_6F6D80(void);
void func_08004348_6F7828(void*,void*);
void func_08004364_6F7844(void*,void*);
void func_08004370_6F7850(void*,void*);
void func_08004D20_6F8200(void*,void*);
void func_08004F74_6F8454(void*,void*);
void func_08004F80_6F8460(void*,void*);
void func_080063B4_6F9894(void*,void*);
void func_080067DC_6F9CBC(void*,void*);
void func_080067E8_6F9CC8(void*,void*);
void func_080003A0_6FB5A0(void*,void*);
void func_080012C8_6FC4C8(void*,void*);
void func_08001F2C_6FD12C(void*,void*);
void func_08001F38_6FD138(void*,void*);
void func_08002388_6FD588(void*,void*);
void func_0800235C_700D8C(void*,void*);
void func_08000450_701550(void*,void*);
void func_080011F0_7022F0(void*,void*);
void func_080046F4_7057F4(void*,void*);
void func_080049C0_705AC0(void*,void*);
void func_080049CC_705ACC(void*,void*);
int func_08000434_706224(void*);
void func_08000ACC_7068BC(void);
void func_0800049C_707EDC(void);
void func_08000790_7081D0(void*,uint32_t);
void func_080003E4_70A424(void*,uint32_t);
int func_080003F8_70A438(void*);
void func_08000410_70A450(void*,uint32_t);
void func_0800083C_70A87C(void*,void*);
void func_080003AC_70CBCC(void*,void*);
void func_08000A80_70D2A0(void*,void*);
void func_08000CF8_70D518(void*,void*);
void func_08000428_70DB68(void*,void*);
void func_08000000_70DFF0(void*,void*);
void func_08002200_7102B0(void*,void*);
void func_08000C0C_71126C(void*,void*);
void func_08001100_711760(void*,void*);
void func_08000000_711AF0(void);
void func_080012C8_712DB8(void*,void*);
void func_08001FD4_714F44(void*,void*);
void func_08002C44_715BB4(void*,void*);
void func_08003770_7166E0(void*,void*);
void func_080039E4_716954(void*,void*);
void func_080039F0_716960(void);
void func_0800124C_7180EC(void);
void func_08002D60_719C00(void*,void*);
void func_08001C38_71D6B8(void*,void*);

static void put_u32(unsigned char *p,uint32_t n){memcpy(p,&n,4);}
static uint32_t get_u32(unsigned char *p){uint32_t n;memcpy(&n,p,4);return n;}
static void put_u16(unsigned char *p,uint16_t n){memcpy(p,&n,2);}
static uint16_t get_u16(unsigned char *p){uint16_t n;memcpy(&n,p,2);return n;}
int main(void){
 _Alignas(16) unsigned char actor[0x180];
 _Alignas(16) unsigned char ctx[0x180];
 unsigned tested=0;

 func_08003230_6DD100(); tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000F14_6E00B4(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080012E0_6E52C0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08002284_6E6264(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000000_6E9150(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000210_6E9360(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080010FC_6EA24C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001108_6EA258(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080012F8_6EA448(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001EC0_6EB010(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 func_08000000_6F0210(); tested++;
 memset(actor,0,sizeof actor);func_080008B8_6F0AC8(actor,7u);SUITE_ASSERT(get_u32(actor+0x80)==30u*7u);func_080008B8_6F0AC8(actor,0xFFFFFFFFu);SUITE_ASSERT(get_u32(actor+0x80)==(uint32_t)(30u*0xFFFFFFFFu));tested++;
 put_u32(actor+0x80,(uint32_t)-92);SUITE_ASSERT(func_080008CC_6F0ADC(actor)==-3);put_u32(actor+0x80,151u);SUITE_ASSERT(func_080008CC_6F0ADC(actor)==5);tested++;
 memset(actor,0,sizeof actor);func_080008E4_6F0AF4(actor,0xDEADBEEFu);SUITE_ASSERT(get_u32(actor+0x88)==0xDEADBEEFu);tested++;
 memset(actor,0,sizeof actor);func_080008EC_6F0AFC(actor,0xDEADBEEFu);SUITE_ASSERT(get_u32(actor+0x84)==0xDEADBEEFu);tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000000_6F34E0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000A9C_6F3F7C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080022F0_6F57D0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080022FC_6F57DC(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080023E0_6F58C0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08003404_6F68E4(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08003894_6F6D74(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 func_080038A0_6F6D80(); tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004348_6F7828(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004364_6F7844(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004370_6F7850(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004D20_6F8200(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004F74_6F8454(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08004F80_6F8460(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080063B4_6F9894(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080067DC_6F9CBC(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080067E8_6F9CC8(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080003A0_6FB5A0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(ctx,0,sizeof ctx);put_u16(ctx+0x14,0);func_080012C8_6FC4C8(actor,ctx);SUITE_ASSERT(get_u16(ctx+0x14)==(uint16_t)-8);put_u16(ctx+0x14,0x7777);func_080012C8_6FC4C8(actor,ctx);SUITE_ASSERT(get_u16(ctx+0x14)==(uint16_t)(0x7777u-8u));tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001F2C_6FD12C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001F38_6FD138(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08002388_6FD588(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_0800235C_700D8C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000450_701550(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080011F0_7022F0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080046F4_7057F4(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080049C0_705AC0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080049CC_705ACC(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 put_u32(actor+0x80,(uint32_t)-122);SUITE_ASSERT(func_08000434_706224(actor)==-3);put_u32(actor+0x80,201u);SUITE_ASSERT(func_08000434_706224(actor)==5);tested++;
 func_08000ACC_7068BC(); tested++;
 func_0800049C_707EDC(); tested++;
 memset(actor,0,sizeof actor);func_08000790_7081D0(actor,7u);SUITE_ASSERT(get_u32(actor+0x84)==30u*7u);func_08000790_7081D0(actor,0xFFFFFFFFu);SUITE_ASSERT(get_u32(actor+0x84)==(uint32_t)(30u*0xFFFFFFFFu));tested++;
 memset(actor,0,sizeof actor);func_080003E4_70A424(actor,7u);SUITE_ASSERT(get_u32(actor+0x84)==30u*7u);func_080003E4_70A424(actor,0xFFFFFFFFu);SUITE_ASSERT(get_u32(actor+0x84)==(uint32_t)(30u*0xFFFFFFFFu));tested++;
 put_u32(actor+0x84,(uint32_t)-92);SUITE_ASSERT(func_080003F8_70A438(actor)==-3);put_u32(actor+0x84,151u);SUITE_ASSERT(func_080003F8_70A438(actor)==5);tested++;
 memset(actor,0,sizeof actor);func_08000410_70A450(actor,0xDEADBEEFu);SUITE_ASSERT(get_u32(actor+0x80)==0xDEADBEEFu);tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_0800083C_70A87C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080003AC_70CBCC(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000A80_70D2A0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000CF8_70D518(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000428_70DB68(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000000_70DFF0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08002200_7102B0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08000C0C_71126C(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001100_711760(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 func_08000000_711AF0(); tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080012C8_712DB8(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001FD4_714F44(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08002C44_715BB4(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08003770_7166E0(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_080039E4_716954(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 func_080039F0_716960(); tested++;
 func_0800124C_7180EC(); tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08002D60_719C00(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 memset(actor,0xA5,sizeof actor);memset(ctx,0x5A,sizeof ctx);func_08001C38_71D6B8(actor,ctx);
 for(unsigned i=0;i<sizeof actor;++i){assert(actor[i]==0xA5);}
 for(unsigned i=0;i<sizeof ctx;++i){assert(ctx[i]==0x5A);}
 tested++;
 assert(tested==69);printf("PASS: %u actual original-address C functions, ASan/UBSan, side effects, bounds, identities\n",tested);return 0;}

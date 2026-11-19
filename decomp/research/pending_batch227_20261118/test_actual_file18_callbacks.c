/* ASan/UBSan smoke test of exact native-source bodies from 53 file18 and ten callbacks. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdalign.h>
typedef unsigned char u8;typedef unsigned int u32; typedef unsigned short u16;
static void baseline(unsigned char *p) { memset(p,0x5A,512); }
static void setfloat(unsigned char *p,size_t at,float v) { memcpy(p+at,&v,sizeof v); }
static void setshort(unsigned char *p,size_t at,unsigned short v) { memcpy(p+at,&v,sizeof v); }
extern void func_8020D4B8_676E98(u8 *o,float v);
extern void func_8020D4C4_676EA4(u8 *o,float v);
extern void func_802122A4_67BC84(u8 *o,float v);
extern void func_80212310_67BCF0(u8 *o);
extern void func_80212BAC_67C58C(u8 *o,float v);
extern void func_80212BF4_67C5D4(u8 *o);
extern void func_80213C84_67D664(u8 *o,float v);
extern void func_802142EC_67DCCC(u8 *o,float v);
extern void func_80214384_67DD64(u8 *o);
extern void func_80214988_67E368(u8 *o,float v);
extern void func_80214994_67E374(u8 *o,float v);
extern void func_80215260_67EC40(u8 *o,float v);
extern void func_80215D54_67F734(u8 *o,float v);
extern void func_8021689C_68027C(u8 *o,float v);
extern void func_802171EC_680BCC(u8 *o,float v);
extern void func_80217BA0_681580(u8 *o,float v);
extern void func_8021B134_684B14(u8 *o,float v);
extern void func_8021B8D8_6852B8(u8 *o,float v);
extern void func_8021C264_685C44(u8 *o,float v);
extern void func_8021C730_686110(u8 *o,float v);
extern void func_8021C78C_68616C(u8 *o,float v);
extern void func_8021D13C_686B1C(u8 *o,float v);
extern void func_8021D198_686B78(u8 *o,float v);
extern void func_8021D9B8_687398(u8 *o,float v);
extern void func_8021DE78_687858(u8 *o,u32 v);
extern void func_8021DF88_687968(u8 *o,float v);
extern void func_8021E2B4_687C94(u8 *o,float v);
extern void func_8021EE84_688864(u8 *o,float v);
extern void func_8021EEEC_6888CC(u8 *o);
extern void func_80224040_68DA20(u8 *o,float v);
extern void func_80224088_68DA68(u8 *o);
extern void func_802240A0_68DA80(void *a,void *b,void *c);
extern void func_80224388_68DD68(u8 *o,float v);
extern void func_80224744_68E124(u8 *o,float v);
extern void func_80224B24_68E504(u8 *o,float v);
extern void func_80224EEC_68E8CC(u8 *o,float v);
extern void func_80225980_68F360(u8 *o,float v);
extern void func_80225B3C_68F51C(u8 *o,float v);
extern void func_80226520_68FF00(u8 *o,float v);
extern void func_80226D20_690700(u8 *o,float v);
extern void func_80227250_690C30(u8 *o,float v);
extern void func_80227298_690C78(u8 *o);
extern void func_80227988_691368(u8 *o,float v);
extern void func_80227A1C_6913FC(u8 *o);
extern void func_80228124_691B04(u8 *o,float v);
extern void func_802281B8_691B98(u8 *o);
extern void func_80228698_692078(u8 *o,float v);
extern void func_80228C48_692628(u8 *o,float v);
extern void func_80228CE0_6926C0(u8 *o);
extern void func_802291EC_692BCC(u8 *o,float v);
extern void func_80229260_692C40(u8 *o);
extern void func_8022993C_69331C(u8 *o,float v);
extern void func_80229984_693364(u8 *o);
extern void func_801CBE68_668598(void *,u8 *);
extern void func_801CC1FC_66892C(void *,u8 *);
extern void func_801CC20C_66893C(void *,u8 *);
extern void func_801CC21C_66894C(void *,u8 *);
extern void func_801CC22C_66895C(void *,u8 *);
extern void func_8020D734_69D974(void *,u8 *);
extern void func_8020D744_69D984(void *,u8 *);
extern void func_8020D754_69D994(void *,u8 *);
extern void func_8020D764_69D9A4(void *,u8 *);
extern void func_8020D770_69D9B0(void *,u8 *);
int main(void) {
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8020D4B8_676E98(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8020D4B8_676E98\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8020D4C4_676EA4(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8020D4C4_676EA4\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802122A4_67BC84(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802122A4_67BC84\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80212310_67BCF0(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80212310_67BCF0\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80212BAC_67C58C(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80212BAC_67C58C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80212BF4_67C5D4(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80212BF4_67C5D4\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80213C84_67D664(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80213C84_67D664\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802142EC_67DCCC(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802142EC_67DCCC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80214384_67DD64(o);
  setfloat(expected,0x6C,0.0f);
  setfloat(expected,0x78,0.0f);
  setfloat(expected,0x84,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80214384_67DD64\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80214988_67E368(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80214988_67E368\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80214994_67E374(o,41.125f);
  setfloat(expected_target,0x24,41.125f);
  setfloat(expected_target,0x20,41.125f);
  setfloat(expected_target,0x1C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80214994_67E374\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80215260_67EC40(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80215260_67EC40\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80215D54_67F734(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80215D54_67F734\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021689C_68027C(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021689C_68027C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802171EC_680BCC(o,41.125f);
  setfloat(expected,0x8C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802171EC_680BCC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80217BA0_681580(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80217BA0_681580\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021B134_684B14(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021B134_684B14\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021B8D8_6852B8(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021B8D8_6852B8\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021C264_685C44(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021C264_685C44\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021C730_686110(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021C730_686110\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021C78C_68616C(o,41.125f);
  setfloat(expected_target,0x24,41.125f);
  setfloat(expected_target,0x20,41.125f);
  setfloat(expected_target,0x1C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021C78C_68616C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021D13C_686B1C(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021D13C_686B1C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021D198_686B78(o,41.125f);
  setfloat(expected_target,0x24,41.125f);
  setfloat(expected_target,0x20,41.125f);
  setfloat(expected_target,0x1C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021D198_686B78\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021D9B8_687398(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021D9B8_687398\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021DE78_687858(o,0xFFFFABCDu);
  setshort(expected,0x60,(unsigned short)(0xFFFFABCDu & 0x3FF));
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021DE78_687858\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021DF88_687968(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021DF88_687968\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021E2B4_687C94(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021E2B4_687C94\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021EE84_688864(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021EE84_688864\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8021EEEC_6888CC(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8021EEEC_6888CC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224040_68DA20(o,41.125f);
  setfloat(expected,0x94,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224040_68DA20\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224088_68DA68(o);
  setfloat(expected,0x9C,0.0f);
  setfloat(expected,0xA4,0.0f);
  setfloat(expected,0xAC,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224088_68DA68\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802240A0_68DA80(o,o,o);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802240A0_68DA80\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224388_68DD68(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224388_68DD68\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224744_68E124(o,41.125f);
  setfloat(expected,0x70,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224744_68E124\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224B24_68E504(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224B24_68E504\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80224EEC_68E8CC(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80224EEC_68E8CC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80225980_68F360(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80225980_68F360\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80225B3C_68F51C(o,41.125f);
  setfloat(expected_target,0x24,41.125f);
  setfloat(expected_target,0x20,41.125f);
  setfloat(expected_target,0x1C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80225B3C_68F51C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80226520_68FF00(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80226520_68FF00\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80226D20_690700(o,41.125f);
  setfloat(expected,0x5C,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80226D20_690700\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80227250_690C30(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80227250_690C30\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80227298_690C78(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80227298_690C78\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80227988_691368(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80227988_691368\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80227A1C_6913FC(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80227A1C_6913FC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80228124_691B04(o,41.125f);
  setfloat(expected,0x64,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80228124_691B04\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802281B8_691B98(o);
  setfloat(expected,0x70,0.0f);
  setfloat(expected,0x88,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802281B8_691B98\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80228698_692078(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80228698_692078\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80228C48_692628(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80228C48_692628\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80228CE0_6926C0(o);
  setfloat(expected,0x6C,0.0f);
  setfloat(expected,0x78,0.0f);
  setfloat(expected,0x84,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80228CE0_6926C0\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_802291EC_692BCC(o,41.125f);
  setfloat(expected,0x60,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_802291EC_692BCC\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80229260_692C40(o);
  setfloat(expected,0x6C,0.0f);
  setfloat(expected,0x78,0.0f);
  setfloat(expected,0x84,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80229260_692C40\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_8022993C_69331C(o,41.125f);
  setfloat(expected,0x90,41.125f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_8022993C_69331C\n");return 1; }
 }
 {
  alignas(16) unsigned char o[512],expected[512],target[512],expected_target[512];
  baseline(o);baseline(expected);baseline(target);baseline(expected_target);
  unsigned char *ptarget=target;memcpy(o+0x18,&ptarget,sizeof ptarget);
  memcpy(expected+0x18,&ptarget,sizeof ptarget);
  func_80229984_693364(o);
  setfloat(expected,0x9C,0.0f);
  setfloat(expected,0xA8,0.0f);
  setfloat(expected,0xB4,0.0f);
  if (memcmp(o,expected,512)||memcmp(target,expected_target,512)) { fprintf(stderr,"float/callback mismatch: func_80229984_693364\n");return 1; }
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_801CBE68_668598(0,b);
  original[5]=7;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_801CBE68_668598\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_801CC1FC_66892C(0,b);
  original[5]=8;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_801CC1FC_66892C\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_801CC20C_66893C(0,b);
  original[5]=2;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_801CC20C_66893C\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_801CC21C_66894C(0,b);
  original[5]=8;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_801CC21C_66894C\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_801CC22C_66895C(0,b);
  original[5]=2;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_801CC22C_66895C\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_8020D734_69D974(0,b);
  original[5]=6;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_8020D734_69D974\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_8020D744_69D984(0,b);
  original[5]=1;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_8020D744_69D984\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_8020D754_69D994(0,b);
  original[5]=7;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_8020D754_69D994\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_8020D764_69D9A4(0,b);
  original[5]=0;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_8020D764_69D9A4\n");return 2;}
 }
 {
  u8 b[32],original[32];memset(b,0x5A,sizeof b);memset(original,0x5A,sizeof original);
  func_8020D770_69D9B0(0,b);
  original[5]=0;
  if (memcmp(b,original,32)) {fprintf(stderr,"callback mismatch: func_8020D770_69D9B0\n");return 2;}
 }
  puts("PASS: 53 original file18 C functions and ten original file16/file21 callbacks under ASan/UBSan");
  return 0;
}

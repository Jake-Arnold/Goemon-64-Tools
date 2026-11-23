typedef short s16;typedef int s32;
extern s32 D_801C7754_1C8354,D_801C77E0_1C83E0;
extern void func_8000C3EC_CFEC(void),func_8003E1A8_3EDA8(void),func_8003E548_3F148(void),func_8003E5B8_3F1B8(void);
extern void func_8000D2C0_DEC0(s32),func_8000C53C_D13C(s32,s32),func_8000C454_D054(s32),func_8000C488_D088(s32),func_8000C430_D030(s32,s32),func_8000C570_D170(s32),func_8000C568_D168(s32,float),func_8000C5A4_D1A4(s32),func_8000C5E4_D1E4(s32,float),func_8000C60C_D20C(s32),func_8000C640_D240(s32);
s16 *func_8003DF98_3EB98(s32 unused,s16 *arg1) {
 if (unused) {}
 switch(*arg1) {
 case -60: func_8000C3EC_CFEC(); arg1++; break;
 case -61: func_8003E1A8_3EDA8(); arg1++; break;
 case -62: D_801C77E0_1C83E0=4; arg1++; break;
 case -63: func_8000D2C0_DEC0(D_801C7754_1C8354); arg1++; break;
 case -70: func_8003E548_3F148(); arg1++; break;
 case -71: func_8003E5B8_3F1B8(); arg1++; break;
 case -32: func_8000C53C_D13C(D_801C7754_1C8354,0); arg1++; break;
 case -33: func_8000C53C_D13C(D_801C7754_1C8354,2); arg1++; break;
 case -34: func_8000C53C_D13C(D_801C7754_1C8354,4); arg1++; break;
 case -35: func_8000C53C_D13C(D_801C7754_1C8354,6); arg1++; break;
 case -36: func_8000C53C_D13C(D_801C7754_1C8354,8); arg1++; break;
 case -37: func_8000C53C_D13C(D_801C7754_1C8354,0); arg1++; break;
 case -50: func_8000C454_D054(D_801C7754_1C8354); arg1++; break;
 case -51: func_8000C488_D088(D_801C7754_1C8354); arg1++; break;
 case -52: func_8000C430_D030(D_801C7754_1C8354,9); arg1++; break;
 case -53: func_8000C430_D030(D_801C7754_1C8354,9); arg1++; break;
 case -54: func_8000C570_D170(D_801C7754_1C8354);func_8000C568_D168(D_801C7754_1C8354,3.0f); arg1++; break;
 case -55: func_8000C5A4_D1A4(D_801C7754_1C8354); arg1++; break;
 case -56: func_8000C5E4_D1E4(D_801C7754_1C8354,2.0f);func_8000C60C_D20C(D_801C7754_1C8354); arg1++; break;
 case -57: func_8000C640_D240(D_801C7754_1C8354); arg1++; break;
 default: arg1++; break;
 }
 return arg1;
}

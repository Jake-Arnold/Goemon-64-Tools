typedef signed char s8;
typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef signed long long s64;
typedef unsigned long long u64;
typedef float f32;
typedef double f64;
typedef s32 M2C_UNK;
typedef s8 M2C_UNK8;
typedef s16 M2C_UNK16;
typedef s32 M2C_UNK32;
typedef s64 M2C_UNK64;
M2C_UNK func_80034E24_35A24();
extern M2C_UNK D_80072E08_73A08;
extern void **D_80173294_173E94;
extern M2C_UNK func_80034E04_35A04;
extern M2C_UNK func_80035124_35D24;
void func_80034D34_35934(void *arg0)
{
  void *var_v0;
  void *temp_v1;
  temp_v1 = *((void **) (((s8 *) arg0) + 0));
  if (temp_v1 != ((void *) 0))
  {
    var_v0 = temp_v1;
  }
  else
  {
    var_v0 = *((void **) (((s8 *) (&D_80072E08_73A08)) + 0));
  }
  if (((s32) (*((u16 *) (((s8 *) arg0) + 0x20)))) >= ((s32) (*((u16 *) (((s8 *) var_v0) + 0x20)))))
  {
    void *sp1C;
    sp1C = var_v0;
    func_80034E24_35A24();
    *((s32 *) (((s8 *) arg0) + 8)) = 0;
    *((M2C_UNK **) (((s8 *) arg0) + 0xC)) = &func_80035124_35D24;
    *((s32 *) (((s8 *) arg0) + 0x10)) = 0;
    *((void ***) (((s8 *) var_v0) + 4)) = (void **) (*((void ***) (((s8 *) arg0) + 4)));
    *(*((void ***) (((s8 *) arg0) + 4))) = *((void **) (((s8 *) arg0) + 0));
    *((void **) (((s8 *) arg0) + 0)) = (void *) (*((void **) (((s8 *) (&D_80072E08_73A08)) + 8)));
    *((void **) (((s8 *) (&D_80072E08_73A08)) + 8)) = arg0;
    *((u16 *) (((s8 *) (&D_80072E08_73A08)) + 0xC)) = (u16) ((*((u16 *) (((s8 *) (&D_80072E08_73A08)) + 0xC))) - 1);
    if (arg0 == D_80173294_173E94)
    {
      D_80173294_173E94 = *((void ***) (((s8 *) arg0) + 4));
    }
    *((void ***) (((s8 *) arg0) + 4)) = (void *) 0;
    return;
  }
  *((M2C_UNK **) (((s8 *) arg0) + 0xC)) = &func_80034E04_35A04;
}


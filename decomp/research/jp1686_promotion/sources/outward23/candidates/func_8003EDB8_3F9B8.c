typedef unsigned int u32;
typedef unsigned char u8;
typedef struct StageState {u8 unknown[0xD4]; u32 flags;} StageState;
extern StageState D_80162420_163020;
extern void func_80034E8C_35A8C(void *callback);
extern void func_8003EDF8_3F9F8(void);
void func_8003EDB8_3F9B8(void *arg0, void *arg1) {
    D_80162420_163020.flags |= 1;
    func_80034E8C_35A8C(func_8003EDF8_3F9F8);
}

typedef unsigned char u8;
extern void *D_8007D290_7DE90;
extern u8 D_801CD060_1CDC60;
extern void func_8003D098_3DC98(void);
extern void func_80034E8C_35A8C(void *);
extern void func_8003CC40_3D840(void);
void func_8003CC8C_3D88C(void *ptr, void *unused) {
    D_8007D290_7DE90 = ptr;
    func_8003D098_3DC98();
    func_80034E8C_35A8C(func_8003CC40_3D840);
    D_801CD060_1CDC60 = 5;
}

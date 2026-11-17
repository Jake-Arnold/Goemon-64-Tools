typedef unsigned char u8;
typedef struct Actor { u8 pad0[0x18]; int enabled; u8 pad1[0x4C]; unsigned int state; } Actor;
extern void func_80217114_5D25E4(void);
extern void func_80216AB8_5D1F88(Actor*);
extern void func_80224B88_5E0058(Actor*);
extern void func_8021893C_5D3E0C(Actor*);
extern void func_8021C444_5D7914(Actor*);
extern void func_8021B808_5D6CD8(Actor*);
extern void func_8021C518_5D79E8(Actor*);
extern void func_8021A978_5D5E48(Actor*);
extern void func_80218990_5D3E60(Actor*);
extern void func_8021B610_5D6AE0(Actor*);
extern void func_80219F20_5D53F0(Actor*);
extern void func_80218350_5D3820(Actor*);
extern void func_80218804_5D3CD4(Actor*);
extern void func_8021A328_5D57F8(Actor*);
void func_80218E7C_5D434C(Actor *actor) {
    if (actor->enabled != 0) {
        func_80217114_5D25E4();
        func_80216AB8_5D1F88(actor);
        func_80224B88_5E0058(actor);
        func_8021893C_5D3E0C(actor);
        func_8021C444_5D7914(actor);
        func_8021B808_5D6CD8(actor);
        func_8021C518_5D79E8(actor);
        func_8021A978_5D5E48(actor);
        func_80218990_5D3E60(actor);
        func_8021B610_5D6AE0(actor);
        func_80219F20_5D53F0(actor);
        func_80218350_5D3820(actor);
        func_80218804_5D3CD4(actor);
        actor->state &= 0xFFFBFFFF;
    }
    func_8021A328_5D57F8(actor);
}

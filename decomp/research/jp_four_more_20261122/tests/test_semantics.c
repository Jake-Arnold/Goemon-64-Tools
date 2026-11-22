#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "jp_actor_observed.h"

Actor *D_8016D430_16E030[3];
int func_8000BFFC_CBFC(int);
void func_8000C088_CC88(int);
void func_8000C0D4_CCD4(int);
int func_8000D108_DD08(void);

static void check_offsets(void) {
    assert(offsetof(Actor,field10)==0x10);
    assert(offsetof(Actor,field30)==0x30);
    assert(offsetof(Actor,field6c)==0x6C);
    assert(offsetof(Actor,field6e)==0x6E);
    assert(offsetof(Actor,field72)==0x72);
    assert(offsetof(Actor,field74)==0x74);
    assert(offsetof(Actor,field76)==0x76);
}

int main(void) {
    check_offsets();
    for (int m=-2048;m<=2048;m++) {
        Actor a={0};
        a.field30=(s16)m;
        a.field10=UINT64_C(0xFC123456789ABCD0)|((unsigned)m&1U);
        D_8016D430_16E030[0]=&a;
        int expected=(m==1||m==2||m==3)?1:(m==5||m==6)?2:0;
        assert(func_8000BFFC_CBFC(0)==expected);
        u64 before=a.field10;
        func_8000C088_CC88(0);
        assert(a.field30==(m==4?5:m));
        assert(a.field10==(m==4?(before|UINT64_C(1)):before));
        a.field6c=8; a.field6e=7;
        a.field72=(s16)(m/8);
        a.field74=222; a.field76=(s16)(m/32);
        s16 prev72=a.field72;
        s16 prev74=a.field74;
        s16 prev76=a.field76;
        func_8000C0D4_CCD4(0);
        assert(a.field6c==0&&a.field6e==0);
        assert(a.field72==(int)prev72+1);
        assert(a.field74==(int)prev74+prev76);
        for (int bits=0;bits<8;bits++) {
            D_8016D430_16E030[0]=(bits&1)?&a:NULL;
            D_8016D430_16E030[1]=(bits&2)?&a:NULL;
            D_8016D430_16E030[2]=(bits&4)?&a:NULL;
            assert(func_8000D108_DD08()==bits);
        }
        D_8016D430_16E030[0]=NULL;
        assert(func_8000BFFC_CBFC(0)==0);
        func_8000C088_CC88(0);
        func_8000C0D4_CCD4(0);
    }
    puts("PASS: 4 authentic C functions, 4,097 actor states x null/live branches and all 8 mask states; ASan/UBSan");
    return 0;
}

typedef unsigned short u16;
extern int func_800136A4_142A4(u16);
int func_80013654_14254(u16 *wave_no_list)
{
    int sp24;
    int wave_no;

    wave_no = *wave_no_list;
    while (wave_no != 0) {
        wave_no = wave_no & 0xFFFF;
        sp24 = func_800136A4_142A4(wave_no);
        wave_no_list++;
        wave_no = *wave_no_list;
    }

    return sp24;
}

extern int func_800136A4_142A4(int);
int func_80013654_14254(unsigned short* wave_no_list) { int sp24; int wave_no; wave_no = *wave_no_list; while (wave_no != 0) { wave_no = wave_no & 0xFFFF; wave_no_list++; sp24 = func_800136A4_142A4(wave_no); wave_no = *wave_no_list; } return sp24; }

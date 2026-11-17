SECTIONS {
 .text 0x80001DF4 : SUBALIGN(4) { *(.text) }
 .rodata : SUBALIGN(4) { *(.rodata*) }
 .data : SUBALIGN(4) { *(.data*) }
 .bss : SUBALIGN(4) { *(.bss*) *(COMMON) }
}
func_80001E50_2A50 = 0x80001E50;
D_80054AC4_556C4 = 0x80054AC4;

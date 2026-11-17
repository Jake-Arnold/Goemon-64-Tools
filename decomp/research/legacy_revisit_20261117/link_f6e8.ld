SECTIONS {
 .text 0x8003F6E8 : SUBALIGN(4) { *(.text) }
 .rodata : SUBALIGN(4) { *(.rodata*) }
 .data : SUBALIGN(4) { *(.data*) }
 .bss : SUBALIGN(4) { *(.bss*) *(COMMON) }
}
func_80037C20_38820 = 0x80037C20;

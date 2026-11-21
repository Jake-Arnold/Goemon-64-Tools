/* Original-USA file 22, ROM 0x69EB7C, VMA 0x801CBF5C, 60 bytes.
 * Research-only. Native original-address IDO 5.3 reconstruction.
 * The external data symbol and 36-byte aggregate are observed, not guessed game semantics.
 */
typedef struct { unsigned int word[9]; } Data36;
extern Data36 D_801D7030_6A9C50;
void func_801CBF5C_69EB7C(const Data36 *src) {
    D_801D7030_6A9C50 = *src;
}

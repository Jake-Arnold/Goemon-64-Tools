/* Original-USA file 22, ROM 0x69EB7C, VMA 0x801CBF5C, 60 bytes.
 * Research-only. Native original-address IDO 5.3 reconstruction.
 * The external data symbol and 36-byte aggregate are observed, not guessed game semantics.
 */
typedef struct { unsigned int word[9]; } Data36;
extern Data36 D_801DC760_6AE740;
void func_801D168C_6A366C(const Data36 *src) {
volatile unsigned int goemon_negative_control = 1;

    D_801DC760_6AE740 = *src;
}

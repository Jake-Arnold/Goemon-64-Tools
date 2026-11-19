# Japanese Kai Highway uppercase ROM proof and explicit line-break authoring

Date: 2026-11-19. Source image: user screenshot of a modified Japan-0 ROM in Project64 3.0.1.

## Screen observation
The screenshot shows the original heading 【カイ】 in orange, above an English alphabet inserted into the next Kai Highway area-name record. The full visible letters read **ABCDEFGHIJKLMNOPQRSTU** in sequence, with part of the next glyph at the right-hand edge. The letters are rendered in the Japanese game's native font, not in the USA ROM. The last V–Z positions are **not** individually confirmed; the image is visibly clipped at the right and does not show the full 26-character sample.

The test input was the previously supplied ordered numeric sequence <token:186> through <token:211>. Screenshot observation therefore verifies numeric mappings **186..206=A..U**. Tokens 191=F, 200=O and 206=U were already verified independently against original Japanese UFO dialogue. The new contiguous screenshot validates **18 additional Latin glyph IDs** and raises the screenshot-backed Japanese editor dictionary from **108 to 126 distinct IDs**.

## Geometry limitation shown in the screenshot
The English glyphs exceed the horizontal painted bounds of the original Kai text box, extending onto the background. The original **resource 82 +0x04** header has one native line and the **+0x18** area name is rendered in its following line. The extra English string cannot be made to fit simply by adding line breaks if the 2-line native window retains its original vertical dimensions. Japanese font width metrics and automatic wrapping remain unverified.

## Manual line breaks
The JP editor encodes Enter to the existing engine **-60** newline. The old validator rejected any addition because it compared the complete ordered negative VM-control sequence. New validation permits extra manually inserted -60 tokens while:
- keeping the same original non-newline control sequence in order;
- keeping at least the original number of -60 line breaks;
- enforcing the original maximum token count and existing Japanese repacker constraints;
- continuing to reject all unverified Unicode letters (currently **V–Z**).

This change does not auto-wrap, resize UI windows, or establish whether additional lines fit the original window; the editor warns of possible clipping. Existing USA layout code and ROM routines are unchanged.

## Test scope
Added source-only tests for A–U encoding round trip, V–Z safety, explicit -60 insertion and non-newline control preservation, plus headless Japanese UI staging. Full modified-Japan in-emulator manual-newline rendering remains to be tested.

# Japanese Gojuon token-order hypothesis — 2026-11-19

## Source evidence and distinction

Original Japanese decompressed 32 MiB SHA-1: `6f8745fecc3a5e7d4918c7a73353eb0726116ded`.
The initial user-matched in-game *Kai Highway* screenshot validates the pairs
`15=い`, `19=か`, `95=イ`, `99=カ` in the original Japanese resource 82.
Both katakana tokens equal their hiragana counterparts +80. Additional
screenshot-matched characters are `16=う`, `78=ど`, `292=【`, `293=】`.

**Hypothesis, NOT verified mapping:** Standard 46-character base-gojuon order,
with `14..59` mapped to `あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん`
and `94..139` to their katakana counterparts. Only the named, directly
screenshot-proven IDs are approved for direct Unicode encoding. The assumed
intervals do not establish the ordering of voiced kana, small kana,
non-kana symbols, punctuation, or Latin letters.

## Plausibility from untouched ROM records

The screenshot-verified two records in resource 82 remain unchanged under the
hypothesis, retaining all the precise original 16-bit controls and spaces.
Additional examples from the original candidate index, none screenshot-verified:

- Resource 81 +0x00: `25,44,27,59` gives **しません** (within a larger record)
- Resource 81 +0x48: the prediction produces a fragment **たいほする**
- Resource 84 +0x04: tokens `126,104,105` produce **ムサシ**, consistent with
  the game's Musashi location label

Scanning 5,039 original static text candidates, 4,935 contain one or more
hypothesis-only kana tokens. **This is candidate coverage, not a correctness
rate.** Records can contain unknown characters and other controls.

## Toolkit behavior

- `practice/dialogue_kana.py` is entirely read-only and never changes
  `JP_CONFIRMED_GLYPHS`, `encode_japan_text` or `patch_japan_image`.
- The checkbox **Show inferred kana (unverified) in record list and preview**
  defaults to OFF. When enabled, the Japan record list is also searchable via
  the proposed Unicode strings, and a distinct read-only preview shows the
  selected record while keeping all original control tags unchanged.
- The editable text box continues to expose only screenshot-confirmed Unicode
  plus exact `<token:N>` fallback. It does not accept conjectured Unicode.
- The preview panel counts the conjectured glyph IDs and can copy preview text
  for comparison with an emulator screenshot. Preview text is not implicitly
  encoded or staged.
- USA behavior, JP retail build/relocation and persistent ROM library are
  unchanged. No ROM, artwork, token dump or game assets committed.

## Verification

Local pinned USA/JP inputs, portable Python 3.12, LZKN64 and Xvfb:
`python3.12 -m unittest discover -s tests -p 'test_dialogue*.py' -q`
completed **26 passed, no skips** on 2026-11-19. Tests cover the hypothesis
range, verified glyph agreement, exact original resource-82 decoding,
non-encodability of unverified guesses, read-only Tk preview, opt-in search and
persisted-ROM tests. Full toolkit suites and an in-emulator screenshot
comparison of new guesses have not yet been performed.

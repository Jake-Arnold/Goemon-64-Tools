"""Prepare a reviewed collision-gate source replacement without touching upstream.

This is a *candidate preparation* helper, not a ROM verification or promotion.
The returned source must still pass the pinned original-address/full-ROM gate.
"""
import hashlib
import re

FUNCTION = 'func_80029E08_2AA08'
SOURCE_SHA256_LF = 'abbbb9b571b3658efa171055497f51c2e4e0c6f4d09619e7d6729e0d203cc646'
PRAGMA = re.compile(r'(?m)^#pragma GLOBAL_ASM\("(?:asm/)?(?:[^"\n]*/)?func_80029E08_2AA08\.s"\)[ \t]*$')


def prepare_collision_gate(upstream_source: str, candidate_source: str) -> str:
    """Replace exactly one function pragma, preserving all other source bytes.

    Requires LF text, the pinned isolated candidate and a single original
    placeholder. Never infers a function boundary or rewrites adjacent C.
    """
    if '\r' in upstream_source or '\r' in candidate_source:
        raise ValueError('LF-only source required')
    if hashlib.sha256(candidate_source.encode('utf-8')).hexdigest() != SOURCE_SHA256_LF:
        raise ValueError('Collision candidate differs from reviewed isolated probe')
    matches = list(PRAGMA.finditer(upstream_source))
    if len(matches) != 1:
        raise ValueError('Expected exactly one collision-gate assembly placeholder')
    if re.search(r'\b(?:s32|int)\s+' + FUNCTION + r'\s*\(', upstream_source):
        raise ValueError('Collision function already declared/defined in upstream source')
    if not re.search(r'\bs32\s+' + FUNCTION + r'\(f32 arg0, f32 arg1, f32 arg2\)\s*\{', candidate_source):
        raise ValueError('Candidate signature differs from reviewed probe')
    match = matches[0]
    following = upstream_source[match.end():]
    adjacent = re.search(r'(?m)^[ \t]*s32[ \t]+func_80029E58_2AA58[ \t]*\(', following)
    if adjacent is None or len(re.findall(r'(?m)^[ \t]*s32[ \t]+func_80029E58_2AA58[ \t]*\(', upstream_source)) != 1:
        raise ValueError('Unique following upstream C function anchor missing')
    if re.search(r'(?m)^#pragma GLOBAL_ASM\(', following[:adjacent.start()]):
        raise ValueError('Unexpected assembly function between collision gate and next C function')
    # Keep the upstream common.h and declarations; add only the two callees and
    # the function body, avoiding an extra include or edits to adjacent functions.
    candidate_body = candidate_source[candidate_source.index('s32 ' + FUNCTION + '('):].strip()
    declarations = ('s32 func_8002A168_2AD68(f32, f32, f32);\n'
                    's32 func_8003266C_3326C(f32, f32);\n')
    # The pinned 27FE0.c *defines* the first callee below this gate. A
    # compatible later definition requires a forward prototype, not rejection.
    # Reject any other mention or signature rather than guessing the ABI.
    later_definition = re.compile(
        r'(?m)^s32[ \t]+func_8002A168_2AD68[ \t]*\('
        r'[ \t]*f32[ \t]+[A-Za-z_]\w*[ \t]*,'
        r'[ \t]*f32[ \t]+[A-Za-z_]\w*[ \t]*,'
        r'[ \t]*f32[ \t]+[A-Za-z_]\w*[ \t]*\)[ \t]*\{')
    mentions = list(re.finditer(r'\bfunc_8002A168_2AD68\s*\(', upstream_source))
    definitions = list(later_definition.finditer(upstream_source))
    if mentions and (len(mentions) != 1 or len(definitions) != 1 or
                     definitions[0].start() <= match.end() or
                     mentions[0].start() != upstream_source.index('func_8002A168_2AD68', definitions[0].start())):
        raise ValueError('Existing callee declaration requires manual interface review: func_8002A168_2AD68')
    if re.search(r'\bfunc_8003266C_3326C\s*\(', upstream_source):
        raise ValueError('Existing callee declaration requires manual interface review: func_8003266C_3326C')
    return upstream_source[:match.start()] + declarations + '\n' + candidate_body + upstream_source[match.end():]

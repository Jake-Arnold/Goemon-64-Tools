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
    if upstream_source.count('func_80029E58_2AA58') == 0:
        raise ValueError('Adjacent upstream C function anchor missing')
    # Keep the upstream common.h and declarations; add only the two callees and
    # the function body, avoiding an extra include or edits to adjacent functions.
    candidate_body = candidate_source[candidate_source.index('s32 ' + FUNCTION + '('):].strip()
    declarations = ('s32 func_8002A168_2AD68(f32, f32, f32);\n'
                    's32 func_8003266C_3326C(f32, f32);\n')
    for name in ('func_8002A168_2AD68', 'func_8003266C_3326C'):
        if re.search(r'\b' + name + r'\s*\(', upstream_source):
            raise ValueError('Existing callee declaration requires manual interface review: ' + name)
    match = matches[0]
    return upstream_source[:match.start()] + declarations + '\n' + candidate_body + upstream_source[match.end():]

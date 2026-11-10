"""Fail-closed original-address byte checks, without distributing the ROM."""
import hashlib
import unittest
if __package__:
    from .prove_three_wrappers import check_linked_words, FUNCTIONS, verified_symbol_size_and_address
else:
    from prove_three_wrappers import check_linked_words, FUNCTIONS, verified_symbol_size_and_address


class WrapperByteGuardTests(unittest.TestCase):
    def setUp(self):
        self.reference = bytes(range(36))  # synthetic, not original ROM instructions
        self.expected = hashlib.sha256(self.reference).hexdigest()

    def test_exact_original_36_bytes_accepted(self):
        check_linked_words(self.reference + b'\x00'*8, self.reference,
                           0, len(self.reference), self.expected)

    def test_mutated_original_bytes_rejected(self):
        wrong = self.reference[:5] + bytes([self.reference[5] ^ 1]) + self.reference[6:]
        with self.assertRaisesRegex(ValueError, 'original function reference'):
            check_linked_words(wrong, wrong, 0, len(wrong), self.expected)

    def test_mutated_candidate_instruction_rejected(self):
        candidate = self.reference[:2] + bytes([self.reference[2] ^ 1]) + self.reference[3:]
        with self.assertRaisesRegex(ValueError, 'linked candidate differs'):
            check_linked_words(candidate, self.reference, 0, len(self.reference), self.expected)

    def test_short_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError, 'candidate section shorter'):
            check_linked_words(self.reference[:-4], self.reference, 0, len(self.reference), self.expected)

    def test_wrong_original_offset_rejected(self):
        with self.assertRaisesRegex(ValueError, 'original function reference'):
            check_linked_words(self.reference, b'\x00\x00\x00\x00' + self.reference,
                               0, len(self.reference), self.expected)

    def test_wrong_linked_symbol_size_or_position_rejected(self):
        function = FUNCTIONS[0][1]
        row = lambda address,size: f'  12: {address:08x}  {size} FUNC GLOBAL DEFAULT 1 {function}\n'
        verified_symbol_size_and_address(row(0x80034ED4,36), function, 0x80034ED4,36)
        with self.assertRaisesRegex(ValueError, 'size/address'):
            verified_symbol_size_and_address(row(0x80034ED4,32), function, 0x80034ED4,36)
        with self.assertRaisesRegex(ValueError, 'size/address'):
            verified_symbol_size_and_address(row(0x80034EF0,36), function, 0x80034ED4,36)
        with self.assertRaisesRegex(ValueError, 'size/address'):
            verified_symbol_size_and_address(row(0x80034ED4,36)*2, function, 0x80034ED4,36)

    def test_duplicate_or_non_main_segment_targets_absent(self):
        self.assertEqual(len(FUNCTIONS), 3)
        names = [entry[1] for entry in FUNCTIONS]
        self.assertEqual(len(set(names)), 3)
        self.assertTrue(all(int(name.split('_')[1], 16) - off == 0x7FFFF400
                            for _,name,off,_,_ in FUNCTIONS))


if __name__ == '__main__':
    unittest.main()

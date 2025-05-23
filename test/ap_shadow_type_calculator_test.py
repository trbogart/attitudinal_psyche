import unittest
from itertools import permutations

from ap_shadow_type_calculator import validate_subtype, validate_ap_type, ShadowTypes

class ApShadowTypeCalculatorTest(unittest.TestCase):

    def verify_shadow_types(self, ap_type, subtype, *expected_shadow_types):
        shadow_types = ShadowTypes(ap_type, subtype).shadow_types
        self.assertListEqual(list(expected_shadow_types), shadow_types)

    def test_validate_ap_type_invalid(self):
        with self.assertRaises(ValueError):
            validate_ap_type('ABCD')
        with self.assertRaises(ValueError):
            validate_ap_type('VLLE')
        with self.assertRaises(ValueError):
            validate_ap_type('VLEFA')
        with self.assertRaises(ValueError):
            validate_ap_type('VLE')

    def test_validate_ap_type_valid(self):
        for ap_type in permutations(['V', 'L', 'E', 'F']):
            validate_ap_type(''.join(ap_type))

    def test_validate_subtype_invalid(self):
        with self.assertRaises(ValueError):
            validate_ap_type('ABCD')
        with self.assertRaises(ValueError):
            validate_ap_type('1005')
        with self.assertRaises(ValueError):
            validate_ap_type('100')
        with self.assertRaises(ValueError):
            validate_ap_type('10041')

    def test_validate_subtype_valid(self):
        for pos1 in range(5):
            for pos2 in range(5):
                for pos3 in range(5):
                    for pos4 in range(5):
                        subtype = str(pos1) + str(pos2) + str(pos3) + str(pos4)
                        validate_subtype(subtype)

    def test_all_obscured(self):
        self.verify_shadow_types('velf', '0000', 'VELF')

    def test_all_accentuated(self):
        self.verify_shadow_types('velf', '1234', 'VELF')

    def test_accentuated_and_obscured(self):
        self.verify_shadow_types('velf', '1200', 'VELF')

    def test_swap_obscured(self):
        self.verify_shadow_types('VFEL', '1340', 'VFEL', 'VFLE', 'VLFE')

    def test_swap_nultiple_obscured(self):
        self.verify_shadow_types('vlef', '4300', 'VLEF', 'VELF', 'FELV')

    def test_skip_swap_obscured_multiple_matches(self):
        self.verify_shadow_types('FEVL', '1440', 'FEVL', 'FELV', 'FVLE')

    def test_swap_method_2(self):
        self.verify_shadow_types('LEVF', '1224', 'LEVF', 'LVEF')

    def test_swap_method_3(self):
        self.verify_shadow_types('LEVF', '1334', 'LEVF', 'LVEF')

    def test_swap_method_2_3(self):
        self.verify_shadow_types('LEVF', '1324', 'LEVF', 'LVEF')

    def test_swap_method_1(self):
        self.verify_shadow_types('FLVE', '4234', 'FLVE', 'ELVF')

    def test_swap_method_4(self):
        self.verify_shadow_types('FLVE', '1231', 'FLVE', 'ELVF')

    def test_swap_method_1_and_4(self):
        self.verify_shadow_types('FLVE', '4231', 'FLVE', 'ELVF')

    def test_dual_shadow_1(self):
        self.verify_shadow_types('LFEV', '1221', 'LFEV', 'LEFV', 'VEFL')

    def test_dual_shadow_2(self):
        self.verify_shadow_types('LFEV', '4334', 'LFEV', 'LEFV', 'VEFL')

    def test_conflictor_shadow(self):
        self.verify_shadow_types('evlf', '4124', 'EVLF', 'ELVF', 'FLVE', 'LFVE')

    def test_swap_everything(self):
        self.verify_shadow_types('FelV', '2312', 'FELV', 'FLEV', 'LFEV', 'EFLV', 'EVLF')


if __name__ == '__main__':
    unittest.main()
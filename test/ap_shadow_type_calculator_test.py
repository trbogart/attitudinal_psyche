import unittest
from itertools import permutations

from ap_shadow_type_calculator import validate_subtype, validate_ap_type, ShadowTypes

class ApShadowTypeCalculatorTest(unittest.TestCase):

    def verify_shadow_types(self, ap_type, subtype, *expected_shadow_types):
        shadow_types = ShadowTypes(ap_type, subtype).shadow_types.keys()
        self.assertListEqual(list(expected_shadow_types), list(shadow_types))

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
        self.verify_shadow_types('lvef', '1234', 'LVEF')

    def test_accentuated_and_obscured(self):
        self.verify_shadow_types('velf', '1200', 'VELF')

    def test_swap_obscured(self):
        self.verify_shadow_types('VFEL', '1240', 'VFEL', 'VFLE')

    def test_swap_multiple_obscured(self):
        self.verify_shadow_types('vlef', '4300', 'VLEF', 'VELF', 'FELV')

    def test_skip_swap_obscured_multiple_matches(self):
        self.verify_shadow_types('FEVL', '1440', 'FEVL', 'FELV', 'FVLE')

    def test_skip_obscured_first(self):
        self.verify_shadow_types('VFEL', '1340', 'VFEL', 'VFLE', 'VLFE')

    def test_swap_method1(self):
        self.verify_shadow_types('LEVF', '1224', 'LEVF', 'LVEF')
        self.verify_shadow_types('LEVF', '1334', 'LEVF', 'LVEF')
        self.verify_shadow_types('LEVF', '1324', 'LEVF', 'LVEF')

    def test_swap_method2(self):
        self.verify_shadow_types('FLVE', '4234', 'FLVE', 'ELVF')
        self.verify_shadow_types('FLVE', '1231', 'FLVE', 'ELVF')
        self.verify_shadow_types('FLVE', '4231', 'FLVE', 'ELVF')

    def test_swap_self1(self):
        self.verify_shadow_types('LEFV', '2200', 'LEFV', 'ELFV')
        self.verify_shadow_types('LEFV', '1100', 'LEFV', 'ELFV')
        self.verify_shadow_types('LEFV', '2100', 'LEFV', 'ELFV')

    def test_swap_self2(self):
        self.verify_shadow_types('LEFV', '1240', 'LEFV', 'LEVF')
        self.verify_shadow_types('LEFV', '1203', 'LEFV', 'LEVF')
        self.verify_shadow_types('LEFV', '1243', 'LEFV', 'LEVF')

    def test_swap_other1(self):
        self.verify_shadow_types('LVFE', '3200', 'LVFE', 'FVLE')
        self.verify_shadow_types('LVFE', '1210', 'LVFE', 'FVLE')
        self.verify_shadow_types('LVFE', '3210', 'LVFE', 'FVLE')

    def test_swap_other2(self):
        self.verify_shadow_types('LVFE', '1400', 'LVFE', 'LEFV')
        self.verify_shadow_types('LVFE', '1002', 'LVFE', 'LEFV')
        self.verify_shadow_types('LVFE', '1402', 'LVFE', 'LEFV')

    def test_dual_shadow_1(self):
        self.verify_shadow_types('LFEV', '1221', 'LFEV', 'LEFV', 'VEFL')

    def test_dual_shadow_2(self):
        self.verify_shadow_types('LFEV', '4334', 'LFEV', 'LEFV', 'VEFL')

    def test_swap_with_original_aspect(self):
        self.verify_shadow_types('EVLF', '4124', 'EVLF', 'ELVF', 'FLVE', 'VLFE')

    def test_swap_everything(self):
        self.verify_shadow_types('LFVE', '2111', 'LFVE', 'EFVL', 'ELVF', 'FLVE', 'VLFE')
        self.verify_shadow_types('LVEF', '2121', 'LVEF', 'LEVF', 'FEVL', 'FLVE', 'VLFE')


if __name__ == '__main__':
    unittest.main()
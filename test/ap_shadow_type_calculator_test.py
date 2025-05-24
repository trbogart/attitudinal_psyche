import unittest
from itertools import permutations

from ap_shadow_type_calculator import validate_subtype, validate_ap_type, ShadowTypes

class ApShadowTypeCalculatorTest(unittest.TestCase):

    def verify_shadow_types(self, ap_type, subtype, *expected_shadow_types):
        shadow_types = ShadowTypes(ap_type, subtype).shadow_types.keys()
        self.assertListEqual(list(expected_shadow_types), list(shadow_types))

    def test_validate_ap_type_invalid(self):
        with self.assertRaises(ValueError):
            validate_ap_type('')
        with self.assertRaises(ValueError):
            validate_ap_type('ABCD')
        with self.assertRaises(ValueError):
            validate_ap_type('VLLE')
        with self.assertRaises(ValueError):
            validate_ap_type('VLEFA')
        with self.assertRaises(ValueError):
            validate_ap_type('VLE')
        with self.assertRaises(ValueError):
            validate_ap_type('VLE F')

    def test_validate_ap_type_valid(self):
        for ap_type in permutations(['V', 'L', 'E', 'F']):
            validate_ap_type(''.join(ap_type))

    def test_validate_subtype_invalid(self):
        with self.assertRaises(ValueError):
            validate_ap_type('')
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
        self.verify_shadow_types('VELF', '0000', 'VELF')

    def test_all_accentuated(self):
        self.verify_shadow_types('VEFL', '1234', 'VEFL')

    def test_accentuated_and_obscured(self):
        self.verify_shadow_types('FLEV', '1200', 'FLEV')
        self.verify_shadow_types('FLEV', '1030', 'FLEV')

    def test_common_types(self):
        self.verify_shadow_types('EVFL', '1200', 'EVFL')
        self.verify_shadow_types('EVFL', '1220', 'EVFL', 'EFVL')
        self.verify_shadow_types('EVFL', '1204', 'EVFL')

    def test_swap_multiple_obscured(self):
        self.verify_shadow_types('VLEF', '4300', 'VLEF', 'VELF', 'FELV')

    def test_skip_obscured_multiple_matches(self):
        self.verify_shadow_types('FEVL', '1440', 'FEVL', 'FELV', 'FVLE')

    def test_swap_obscured_first(self):
        self.verify_shadow_types('VFEL', '1340', 'VFEL', 'VFLE', 'VLFE')

    def test_method_2_3(self):
        self.verify_shadow_types('LEVF', '1224', 'LEVF', 'LVEF')
        self.verify_shadow_types('LEVF', '1334', 'LEVF', 'LVEF')
        self.verify_shadow_types('LEVF', '1324', 'LEVF', 'LVEF')

    def test_method_1_4(self):
        self.verify_shadow_types('FLVE', '4234', 'FLVE', 'ELVF')
        self.verify_shadow_types('FLVE', '1231', 'FLVE', 'ELVF')
        self.verify_shadow_types('FLVE', '4231', 'FLVE', 'ELVF')

    def test_self_1_2(self):
        self.verify_shadow_types('LEFV', '2200', 'LEFV', 'ELFV')
        self.verify_shadow_types('LEFV', '1100', 'LEFV', 'ELFV')
        self.verify_shadow_types('LEFV', '2100', 'LEFV', 'ELFV')

    def test_self_3_4(self):
        self.verify_shadow_types('VLFE', '1240', 'VLFE', 'VLEF')
        self.verify_shadow_types('VLFE', '1203', 'VLFE', 'VLEF')
        self.verify_shadow_types('VLFE', '1243', 'VLFE', 'VLEF')

    def test_other_1_3(self):
        self.verify_shadow_types('LVFE', '3200', 'LVFE', 'FVLE')
        self.verify_shadow_types('LVFE', '1210', 'LVFE', 'FVLE')
        self.verify_shadow_types('LVFE', '3210', 'LVFE', 'FVLE')

    def test_other_2_4(self):
        self.verify_shadow_types('ELFV', '1400', 'ELFV', 'EVFL')
        self.verify_shadow_types('ELFV', '1002', 'ELFV', 'EVFL')
        self.verify_shadow_types('ELFV', '1402', 'ELFV', 'EVFL')

    def test_dual_shadow(self):
        self.verify_shadow_types('LFEV', '1221', 'LFEV', 'LEFV', 'VEFL')
        self.verify_shadow_types('FELV', '4334', 'FELV', 'FLEV', 'VLEF')
        self.verify_shadow_types('FELV', '4300', 'FELV', 'FLEV', 'VLEF')
        self.verify_shadow_types('LFEV', '0021', 'LFEV', 'VFEL', 'VEFL')

    def test_conflictor_shadow(self):
        self.verify_shadow_types('LEVF', '0212', 'LEVF', 'VELF', 'VFLE')
        self.verify_shadow_types('LEVF', '3404', 'LEVF', 'VELF', 'VFLE')
        self.verify_shadow_types('LEVF', '4412', 'LEVF', 'FEVL', 'VEFL', 'VLFE', 'VFLE')
        self.verify_shadow_types('LEVF', '4442', 'LEVF', 'FEVL', 'FELV', 'FVLE', 'VFLE')

    def test_swap_with_original_aspect(self):
        self.verify_shadow_types('EVLF', '4124', 'EVLF', 'ELVF', 'FLVE', 'VLFE')

    def test_max_shadow_types(self):
        self.verify_shadow_types('LFVE', '2111', 'LFVE', 'EFVL', 'ELVF', 'FLVE', 'VLFE')
        self.verify_shadow_types('LVEF', '2121', 'LVEF', 'LEVF', 'FEVL', 'FLVE', 'VLFE')

    def test_all_ones(self):
        self.verify_shadow_types('FVLE', '1111', 'FVLE', 'EVLF', 'VELF', 'LEVF')

    def test_all_twos(self):
        self.verify_shadow_types('FVEL', '2222', 'FVEL', 'FEVL', 'EFVL', 'ELVF')

    def test_all_threes(self):
        self.verify_shadow_types('FLVE', '3333', 'FLVE', 'FVLE', 'FVEL', 'EVFL')

    def test_all_fours(self):
        self.verify_shadow_types('ELVF', '4444', 'ELVF', 'FLVE', 'FLEV', 'FVEL')

    def test_case(self):
        self.verify_shadow_types('evfl', '1234', 'EVFL')
        self.verify_shadow_types('eFVl', '1234', 'EFVL')

    def test_extra_space(self):
        self.verify_shadow_types(' VLFE ', ' 1204 ', 'VLFE')

    def test_invalid_ap_type(self):
        with self.assertRaises(ValueError):
            ShadowTypes('', '0000')
        with self.assertRaises(ValueError):
            ShadowTypes('ABCD', '0000')
        with self.assertRaises(ValueError):
            ShadowTypes('VLLE', '0000')
        with self.assertRaises(ValueError):
            ShadowTypes('VLEFA', '0000')
        with self.assertRaises(ValueError):
            ShadowTypes('VLE', '0000')
        with self.assertRaises(ValueError):
            ShadowTypes('VLE F', '0000')

    def test_invalid_subtype(self):
        with self.assertRaises(ValueError):
            ShadowTypes('VLEF', '')
        with self.assertRaises(ValueError):
            ShadowTypes('VLEF', 'ABCD')
        with self.assertRaises(ValueError):
            ShadowTypes('VLEF', '1005')
        with self.assertRaises(ValueError):
            ShadowTypes('VLEF', '100')
        with self.assertRaises(ValueError):
            ShadowTypes('VLEF', '10041')

if __name__ == '__main__':
    unittest.main()
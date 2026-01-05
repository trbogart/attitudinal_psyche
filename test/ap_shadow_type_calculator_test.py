import unittest
from itertools import permutations

from ap_shadow_type_calculator import validate_subtype, validate_ap_type, ShadowTypes, calculate_shadow_types


class ApShadowTypeCalculatorTest(unittest.TestCase):

    def verify_shadow_types(self, ap_type, subtype, *expected_shadow_types):
        shadow_types = ShadowTypes(ap_type, subtype).shadow_types.keys()
        self.assertListEqual(list(expected_shadow_types), list(shadow_types))

    def test_validate_all_valid_ap_types(self):
        for ap_type in self.all_valid_ap_types():
            validate_ap_type(ap_type)

    def test_validate_all_valid_subtypes(self):
        for subtype in self.all_valid_subtypes():
            validate_subtype(subtype)

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
        self.verify_shadow_types('LFEV', '0021', 'LFEV', 'VFEL', 'VEFL')
        self.verify_shadow_types('LFEV', '0301', 'LFEV', 'VFEL', 'VEFL')
        self.verify_shadow_types('FELV', '4334', 'FELV', 'FLEV', 'VLEF')
        self.verify_shadow_types('FELV', '4300', 'FELV', 'FLEV', 'VLEF')
        self.verify_shadow_types('FELV', '4020', 'FELV', 'FLEV', 'VLEF')

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

    def test_all_valid_ap_types(self):
        for ap_type in self.all_valid_ap_types():
            ShadowTypes(ap_type, '0000')

    def test_all_valid_subtypes(self):
        for subtype in self.all_valid_subtypes():
            ShadowTypes('EFVL', subtype)

    def test_invalid_ap_type(self):
        subtype = '0000'
        with self.assertRaises(ValueError):
            ShadowTypes('', subtype)
        with self.assertRaises(ValueError):
            ShadowTypes('ABCD', subtype)
        with self.assertRaises(ValueError):
            ShadowTypes('VLLE', subtype)
        with self.assertRaises(ValueError):
            ShadowTypes('VLEFA', subtype)
        with self.assertRaises(ValueError):
            ShadowTypes('VLE', subtype)
        with self.assertRaises(ValueError):
            ShadowTypes('VLE F', subtype)

    def test_invalid_subtype(self):
        ap_type = 'VLEF'
        with self.assertRaises(ValueError):
            ShadowTypes(ap_type, '')
        with self.assertRaises(ValueError):
            ShadowTypes(ap_type, 'ABCD')
        with self.assertRaises(ValueError):
            ShadowTypes(ap_type, '1005')
        with self.assertRaises(ValueError):
            ShadowTypes(ap_type, '100')
        with self.assertRaises(ValueError):
            ShadowTypes(ap_type, '10041')

    def test_json_no_shadow_type(self):
        ap_type_str = 'VELF'
        subtype_str = '1234'
        shadow_types_json = calculate_shadow_types(ap_type_str, subtype_str)
        expected = {
            'ap_type': ap_type_str,
            'subtype': subtype_str,
            'shadow_types': [
                {'shadow_type': ap_type_str, 'description': 'AP type'}
            ],
            'functions': [
                '1+2 - Lifeblood (Self+) - Conceptualist (V+E): Idealizing, Glorifying, Influencing, Exalting',
                '1+3 - Security (Others-) - Strategist (V+L): Projecting, Modeling, Pathing, Hypothesizing',
                '1+4 - Launch (Result) - Experiencer (V+F): Maneuvering, Locating, Perceiving, Positioning',
                '2+3 - Spin-out (Process) - Evaluator (L+E): Judging, Valuing, Ranking, Labeling',
                '2+4 - Haphazard (Others+) - Reactivist (E+F): Responding, Performing, Acting, Emoting',
                '3+4 - Burnout (Self-) - Realist (L+F): Measuring, Correcting, Tinkering, Improvising',
            ]
        }
        self.assertDictEqual(shadow_types_json, expected)

    def test_json_with_one_shadow_type(self):
        ap_type_str = 'FVLE'
        subtype_str = '0220'
        shadow_types_json = calculate_shadow_types(ap_type_str, subtype_str)

        expected = {
            'ap_type': ap_type_str,
            'subtype': subtype_str,
            'shadow_types': [
                {'shadow_type': ap_type_str, 'description': 'AP type'},
                {'shadow_type': 'FLVE', 'description': 'Swapped 3L-2 (method)'},
            ],
            'functions': [
                '1+2 - Lifeblood (Self+) - Experiencer (V+F): Maneuvering, Locating, Perceiving, Positioning',
                '1+3 - Security (Others-) - Realist (L+F): Measuring, Correcting, Tinkering, Improvising',
                '1+4 - Launch (Result) - Reactivist (E+F): Responding, Performing, Acting, Emoting',
                '2+3 - Spin-out (Process) - Strategist (V+L): Projecting, Modeling, Pathing, Hypothesizing',
                '2+4 - Haphazard (Others+) - Conceptualist (V+E): Idealizing, Glorifying, Influencing, Exalting',
                '3+4 - Burnout (Self-) - Evaluator (L+E): Judging, Valuing, Ranking, Labeling',
            ]
        }
        self.assertDictEqual(shadow_types_json, expected)

    def test_json_with_multiple_shadow_types(self):
        ap_type_str = 'LVEF'
        subtype_str = '4343'
        shadow_types_json = calculate_shadow_types(ap_type_str, subtype_str)

        expected = {
            'ap_type': ap_type_str,
            'subtype': subtype_str,
            'shadow_types': [
                {'shadow_type': ap_type_str, 'description': 'AP type'},
                {'shadow_type': 'LEVF', 'description': 'Swapped 2V-3 (method)'},
                {'shadow_type': 'FEVL', 'description': 'Swapped 1L-4 (method)'},
                {'shadow_type': 'FLVE', 'description': 'Swapped 3E-4 (self)'},
                {'shadow_type': 'VLFE', 'description': 'Swapped 4F-3 (self)'},
            ],
            'functions': [
                '1+2 - Lifeblood (Self+) - Strategist (V+L): Projecting, Modeling, Pathing, Hypothesizing',
                '1+3 - Security (Others-) - Evaluator (L+E): Judging, Valuing, Ranking, Labeling',
                '1+4 - Launch (Result) - Realist (L+F): Measuring, Correcting, Tinkering, Improvising',
                '2+3 - Spin-out (Process) - Conceptualist (V+E): Idealizing, Glorifying, Influencing, Exalting',
                '2+4 - Haphazard (Others+) - Experiencer (V+F): Maneuvering, Locating, Perceiving, Positioning',
                '3+4 - Burnout (Self-) - Reactivist (E+F): Responding, Performing, Acting, Emoting',
            ]
        }
        self.assertDictEqual(shadow_types_json, expected)

    @staticmethod
    def all_valid_subtypes():
        for pos1 in range(5):
            for pos2 in range(5):
                for pos3 in range(5):
                    for pos4 in range(5):
                        yield str(pos1) + str(pos2) + str(pos3) + str(pos4)

    @staticmethod
    def all_valid_ap_types():
        for ap_type in permutations('VELF'):
            yield ''.join(ap_type)


if __name__ == '__main__':
    unittest.main()

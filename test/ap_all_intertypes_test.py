import unittest
from itertools import permutations

from ap_all_intertype import get_all_intertypes

class ApIntertypeTest(unittest.TestCase):
    def test_get_all_intertypes(self):
        intertypes = get_all_intertypes('FVLE')
        self.assertEqual(len(intertypes), 17)
        self.assertEqual(intertypes['Dual'], 'FVLE <—> ELVF (shared sexta)')
        self.assertEqual(intertypes['Identical'], 'FVLE <—> FVLE (shared sexta)')
        self.assertEqual(intertypes['Solution'], 'FVLE <—> EVLF (shared sexta)')
        self.assertEqual(intertypes['Sister'], 'FVLE <—> FLVE (shared sexta)')
        self.assertEqual(intertypes['Radiance'], 'EFVL <—> FVLE <—> VLEF (square)')
        self.assertEqual(intertypes['Instruction'], 'ELFV —> FVLE —> LEVF (square)')
        self.assertEqual(intertypes['Invention'], 'FLEV —> FVLE —> FEVL (triangular)')
        self.assertEqual(intertypes['Assistance'], 'EVFL —> FVLE —> LVEF (triangular)')
        self.assertEqual(intertypes['Enhancement'], 'EFLV —> FVLE —> VELF (triangular)')
        self.assertEqual(intertypes['Regulation'], 'VLFE —> FVLE —> LFVE (triangular)')
        self.assertEqual(intertypes['Near-Identical'], 'FVLE <—> VFLE (linear)')
        self.assertEqual(intertypes['Cousin'], 'FVLE <—> FVEL (linear)')
        self.assertEqual(intertypes['Customary'], 'FVLE <—> FELV (linear)')
        self.assertEqual(intertypes['Specificity'], 'FVLE <—> LVFE (linear)')
        self.assertEqual(intertypes['Faux-Identical'], 'FVLE <—> VFEL (opposed sexta)')
        self.assertEqual(intertypes['Suffocation'], 'VEFL <—> FVLE <—> LFEV (opposed sexta, square)')
        self.assertEqual(intertypes['Conflict'], 'FVLE <—> LEFV (opposed sexta)')

    def test_all_types_present(self):
        for ap_type in self.all_valid_ap_types():
            intertypes = get_all_intertypes(ap_type)

            for other_type in self.all_valid_ap_types():
                count = sum(value.split().count(other_type) for value in intertypes.values())
                if other_type == ap_type:
                    # type is found in every row, plus twice in Identical
                    self.assertEqual(count, len(intertypes) + 1)
                else:
                    # all other types are found exactly once
                    self.assertEqual(count, 1)

    @staticmethod
    def all_valid_ap_types():
        for ap_type in permutations('VELF'):
            yield ''.join(ap_type)
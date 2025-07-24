import unittest
from itertools import permutations

from ap_all_intertype import get_all_intertypes
from ap_intertype import get_intertype

from enum import Enum

class Direction(Enum):
    SYMMETRICAL = 0
    TO = 1
    FROM = 2


class ApIntertypeTest(unittest.TestCase):
    def _validate(self, ap_type1, ap_type2, intertype_relation, relation_type, direction = Direction.SYMMETRICAL, reversed = False):
        result = get_intertype(ap_type1, ap_type2)

        if direction == Direction.SYMMETRICAL:
            intertype = f'{ap_type1} <—> {ap_type2} ({relation_type})'
        elif direction == Direction.FROM:
            intertype = f'{ap_type2} —> {ap_type1} ({relation_type})'
        else:
            intertype = f'{ap_type1} —> {ap_type2} ({relation_type})'

        expected = f'{intertype_relation}: {intertype}'
        self.assertEqual(result, expected)

        if not reversed:
            if direction == Direction.FROM:
                reversed_direction = Direction.TO
            elif direction == Direction.TO:
                reversed_direction = Direction.FROM
            else:
                reversed_direction = direction
            self._validate(ap_type2, ap_type1, intertype_relation, relation_type, reversed_direction, reversed = True)

    def test_get_intertype_dual(self):
        self._validate('FVLE', 'ELVF', 'Dual', 'shared sexta')

    def test_get_intertype_identical(self):
        self._validate('FVLE', 'FVLE', 'Identical', 'shared sexta')

    def test_get_intertype_solution(self):
        self._validate('FVLE', 'EVLF', 'Solution', 'shared sexta')

    def test_get_intertype_sister(self):
        self._validate('FVLE', 'FLVE', 'Sister', 'shared sexta')

    def test_get_intertype_radiance1(self):
        self._validate('FVLE', 'VLEF', 'Radiance', 'square')

    def test_get_intertype_radiance2(self):
        self._validate('FVLE', 'EFVL', 'Radiance', 'square')

    def test_get_intertype_instruction1(self):
        self._validate('FVLE', 'LEVF', 'Instruction', 'square', direction = Direction.TO)

    def test_get_intertype_instruction2(self):
        self._validate('FVLE', 'ELFV', 'Instruction', 'square', direction = Direction.FROM)

    def test_get_intertype_invention1(self):
        self._validate('FVLE', 'FEVL', 'Invention', 'triangular', direction = Direction.TO)

    def test_get_intertype_invention2(self):
        self._validate('FVLE', 'FLEV', 'Invention', 'triangular', direction = Direction.FROM)

    def test_get_intertype_assistance1(self):
        self._validate('FVLE', 'LVEF', 'Assistance', 'triangular', direction = Direction.TO)

    def test_get_intertype_assistance2(self):
        self._validate('FVLE', 'EVFL', 'Assistance', 'triangular', direction = Direction.FROM)

    def test_get_intertype_enhancement1(self):
        self._validate('FVLE', 'VELF', 'Enhancement', 'triangular', direction = Direction.TO)

    def test_get_intertype_enhancement2(self):
        self._validate('FVLE', 'EFLV', 'Enhancement', 'triangular', direction = Direction.FROM)

    def test_get_intertype_regular1(self):
        self._validate('FVLE', 'VLFE', 'Regulation', 'triangular', direction = Direction.FROM)

    def test_get_intertype_regular2(self):
        self._validate('FVLE', 'LFVE', 'Regulation', 'triangular', direction = Direction.TO)

    def test_get_intertype_near_identical(self):
        self._validate('FVLE', 'VFLE', 'Near-Identical', 'linear')

    def test_get_intertype_cousin(self):
        self._validate('FVLE', 'FVEL', 'Cousin', 'linear')

    def test_get_intertype_customary(self):
        self._validate('FVLE', 'FELV', 'Customary', 'linear')

    def test_get_intertype_specificity(self):
        self._validate('FVLE', 'LVFE', 'Specificity', 'linear')

    def test_get_intertype_faux_identical(self):
        self._validate('FVLE', 'VFEL', 'Faux-Identical', 'opposed sexta')

    def test_get_intertype_suffocation1(self):
        self._validate('FVLE', 'LFEV', 'Suffocation', 'opposed sexta, square', direction = Direction.SYMMETRICAL)

    def test_get_intertype_suffocation2(self):
        self._validate('FVLE', 'VEFL', 'Suffocation', 'opposed sexta, square', direction = Direction.SYMMETRICAL)

    def test_get_intertype_conflict(self):
        self._validate('FVLE', 'LEFV', 'Conflict', 'opposed sexta')

    def test_get_all_intertypes(self):
        # test get_all_intertypes() for a specific AP type
        intertype_relations = get_all_intertypes('FVLE')
        self.assertEqual(len(intertype_relations), 17)
        self.assertEqual(intertype_relations['Dual'], 'FVLE <—> ELVF (shared sexta)')
        self.assertEqual(intertype_relations['Identical'], 'FVLE <—> FVLE (shared sexta)')
        self.assertEqual(intertype_relations['Solution'], 'FVLE <—> EVLF (shared sexta)')
        self.assertEqual(intertype_relations['Sister'], 'FVLE <—> FLVE (shared sexta)')
        self.assertEqual(intertype_relations['Radiance'], 'EFVL <—> FVLE <—> VLEF (square)')
        self.assertEqual(intertype_relations['Instruction'], 'ELFV —> FVLE —> LEVF (square)')
        self.assertEqual(intertype_relations['Invention'], 'FLEV —> FVLE —> FEVL (triangular)')
        self.assertEqual(intertype_relations['Assistance'], 'EVFL —> FVLE —> LVEF (triangular)')
        self.assertEqual(intertype_relations['Enhancement'], 'EFLV —> FVLE —> VELF (triangular)')
        self.assertEqual(intertype_relations['Regulation'], 'VLFE —> FVLE —> LFVE (triangular)')
        self.assertEqual(intertype_relations['Near-Identical'], 'FVLE <—> VFLE (linear)')
        self.assertEqual(intertype_relations['Cousin'], 'FVLE <—> FVEL (linear)')
        self.assertEqual(intertype_relations['Customary'], 'FVLE <—> FELV (linear)')
        self.assertEqual(intertype_relations['Specificity'], 'FVLE <—> LVFE (linear)')
        self.assertEqual(intertype_relations['Faux-Identical'], 'FVLE <—> VFEL (opposed sexta)')
        self.assertEqual(intertype_relations['Suffocation'], 'VEFL <—> FVLE <—> LFEV (opposed sexta, square)')
        self.assertEqual(intertype_relations['Conflict'], 'FVLE <—> LEFV (opposed sexta)')

    def test_all_types_count(self):
        # each AP type is mapped to each other AP type exactly once
        for ap_type in self.all_valid_ap_types():
            intertype_relations = get_all_intertypes(ap_type)

            for other_type in self.all_valid_ap_types():
                count = sum(value.split().count(other_type) for value in intertype_relations.values())
                if other_type == ap_type:
                    # type is found in every row, plus twice in Identical
                    self.assertEqual(count, len(intertype_relations) + 1)
                else:
                    # all other types are found exactly once
                    self.assertEqual(count, 1)

    def test_all_types(self):
        # test that get_intertype() and get_all_intertypes() are consistent for all types
        for ap_type in self.all_valid_ap_types():
            intertypes = get_all_intertypes(ap_type)
            for relation, text in intertypes.items():
                tokens = text.split()
                if 'square' in text or 'triangular' in text:
                    if tokens[1] == '<—>':
                        # symmetrical
                        other_type1 = tokens[0]
                        expected1 = f'{relation}: {ap_type} <—> {other_type1} {' '.join(tokens[5:])}'
                        self.assertEqual(get_intertype(ap_type, other_type1), expected1)

                        other_type2 = tokens[4]
                        expected2 = f'{relation}: {ap_type} <—> {other_type2} {' '.join(tokens[5:])}'
                        self.assertEqual(get_intertype(ap_type, other_type2), expected2)
                    else:
                        # asymmetrical
                        other_type1 = tokens[0]
                        expected1 = f'{relation}: {other_type1} —> {ap_type} {' '.join(tokens[5:])}'
                        self.assertEqual(get_intertype(ap_type, other_type1), expected1)

                        other_type2 = tokens[4]
                        expected2 = f'{relation}: {ap_type} —> {other_type2} {' '.join(tokens[5:])}'
                        self.assertEqual(get_intertype(ap_type, other_type2), expected2)
                else:
                    other_type = tokens[2]
                    expected = f'{relation}: {text}'
                    self.assertEqual(get_intertype(ap_type, other_type), expected)

    @staticmethod
    def all_valid_ap_types():
        for ap_type in permutations('VELF'):
            yield ''.join(ap_type)
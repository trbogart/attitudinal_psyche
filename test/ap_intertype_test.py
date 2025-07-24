import unittest

from ap_intertype import get_intertype

from enum import Enum

class Direction(Enum):
    SYMMETRICAL = 0
    TO = 1
    FROM = 2


class ApIntertypeTest(unittest.TestCase):
    def _validate(self, ap_type1, ap_type2, name, suffix, direction = Direction.SYMMETRICAL, reversed = False):
        result = get_intertype(ap_type1, ap_type2)

        if direction == Direction.SYMMETRICAL:
            intertype = f'{ap_type1} <—> {ap_type2} ({suffix})'
        elif direction == Direction.FROM:
            intertype = f'{ap_type2} —> {ap_type1} ({suffix})'
        else:
            intertype = f'{ap_type1} —> {ap_type2} ({suffix})'

        expected = f'{name}: {intertype}'
        self.assertEqual(result, expected)

        if not reversed:
            if direction == Direction.FROM:
                reversed_direction = Direction.TO
            elif direction == Direction.TO:
                reversed_direction = Direction.FROM
            else:
                reversed_direction = direction
            self._validate(ap_type2, ap_type1, name, suffix, reversed_direction, reversed = True)

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

# temporary script to calculate function/blocks that have been found with new typings
import itertools


class TypingStats:
    # typing videos with new definitions
    celebrity_typings = [
        # From Celebrity Typing videos
        'EFVL', # 10.1 - Chappell Roan
        'VLEF', # 10.1 - Grimes
        'FLVE', # 10.1 - Jenna Ortega
        'VELF', # 10.1 - Rihanna
        'FVLE', # 10.1 - Matthew Bellamy
        'VLFE', # 10.1 - Philip DeFranco
        'LVFE', # 10.1 - Sandra Bullock
        'FELV', # 10.1 - Aaron Paul
        'VFLE', # 10.1 - Gillian Anderson (? TBD)
        'VELF', # 10.1 - Madonna
        'EVFL', # 33 - Mr. Rogers
        'VLEF', # 34 - Neil DeGrasse Tyson
        'FVLE', # 35 - Adriana Lima
        'FEVL', # 36.1 - Kate Moss
        'FLVE', # 37 - Bailey Sarian
        'VLFE', # 38 - Azealia Banks
        'FVEL', # 39 - Sofia Isella
        'FVEL', # 40 - Adrianne Lenker
        'VLFE', # 41 - Owen Cook
        'LVFE', # 42 - Nick LS De Cesare
        'VEFL', # 43 - Kobe Bryant
        'FVEL', # 44 - Bjork
        'EFVL', # 45 - HRH Collection
        'VLFE', # 46 - Bo Burnham
        'VELF', # 47 - Seal
        'FLEV', # 48 - Kurt Cobain
        'VELF', # 49 - Paris Hilton
        'VEFL', # 50 - Vic DiCara
        'FEVL', # 51 - David Lynch
        'VLFE', # 52 - Courtney Love
        'EFLV', # 53 - Trisha Paytas
        'FELV', # 54 - JMSN
        'LFVE', # 55 - Carl Jung
        'VELF', # 56 - Hayley Williams

        # From Theory videos
        'ELVF',  # Asmongold (4F: Refusing To Process the Aspect)
    ]
    paid_typings = {
        # as of 12/16/2025
        'FVLE': 5,
        'FLVE': 9,
        'EVLF': 2,
        'ELVF': 4,
        'LVFE': 2,
        'LFVE': 1,
        'EVFL': 1,
        'EFVL': 1,
        'VLFE': 7,
        'VFLE': 3,
        'ELFV': 0,
        'EFLV': 0,
        'VFEL': 3,
        'VEFL': 4,
        'LFEV': 0,
        'LEFV': 0,
        'VLEF': 4,
        'VELF': 3,
        'FLEV': 4,
        'FELV': 3,
        'LVEF': 4,
        'LEVF': 1,
        'FVEL': 7,
        'FEVL': 6,
    }
    valid_types = sorted('FELV')

    def __init__(self, include_celebrities: bool = True, include_paid: bool = False):
        for ap_type in self.celebrity_typings:
            self.validate_ap_type(ap_type)
        for ap_type in self.paid_typings.keys():
            self.validate_ap_type(ap_type)

        if include_celebrities:
            self.all_typings = self.celebrity_typings
        else:
            self.all_typings = []
        if include_paid:
            for ap_type, count in self.paid_typings.items():
                self.all_typings.extend(itertools.repeat(ap_type, count))

        unique_type_count = len(set(self.all_typings))

        attitude_counts = self.calculate_attitude_counts()
        type_counts = self.calculate_type_counts()
        sexta_counts = self.calculate_sexta_counts()
        sexta_1pos_counts = self.calculate_sexta_1pos_counts()
        missing_types = [ap_type for ap_type, count in type_counts.items() if count == 0]

        # init variables calculated by calculate_functions_by_block
        self.missing_pairs = []
        self.missing_pairs_dir = []
        self.functions_by_block = []

        # blocks
        self.calculate_functions_by_block('Strategist', 'V', 'L')
        self.calculate_functions_by_block('Reactivist', 'F', 'E')

        self.calculate_functions_by_block('Experiencer', 'V', 'F')
        self.calculate_functions_by_block('Evaluator', 'L', 'E')

        self.calculate_functions_by_block('Conceptualist', 'V', 'E')
        self.calculate_functions_by_block('Realist', 'L', 'F')

        print('Summary:')
        print(f'- {len(self.all_typings)} total typings ({len(self.all_typings) - unique_type_count} duplicate types)')
        missing_types_suffix = self.get_missing_suffix(missing_types)
        print(f'- {unique_type_count} of 24 types{missing_types_suffix}')
        missing_pairs_suffix = self.get_missing_suffix(self.missing_pairs)
        print(f'- {36 - len(self.missing_pairs)} of 36 function/block pairs{missing_pairs_suffix}')
        missing_pairs_dir_suffix = self.get_missing_suffix(self.missing_pairs_dir)
        print(
            f'- {72 - len(self.missing_pairs_dir)} of 72 function/block pairs (directional){missing_pairs_dir_suffix}')

        print()
        print(f'Type counts ({len(missing_types)} missing)')
        for ap_type, count in type_counts.items():
            print(f'- {ap_type}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Attitude counts ({self.get_missing_count(attitude_counts)} missing):')
        for key, count in attitude_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Sexta counts ({self.get_missing_count(sexta_counts)} missing):')
        for key, count in sexta_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Sexta counts with 1st attitude ({self.get_missing_count(sexta_1pos_counts)} missing):')
        for key, count in sexta_1pos_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        for functions in self.functions_by_block:
            print()
            for function in functions:
                print(function)

    @staticmethod
    def get_missing_suffix(missing_list: list) -> str:
        if len(missing_list) > 0:
            list_str = f'{', '.join(missing_list)}' if len(missing_list) > 0 else 'None'
            return f' - missing {len(missing_list)}: {list_str}'
        return ''

    @staticmethod
    def get_missing_count(counts: dict[str, int]) -> int:
        return sum(1 for count in counts.values() if count == 0)

    def calculate_type_counts(self):
        type_counts = {}

        # iterate over paid_typings, which includes all types in standard order
        for ap_type in self.paid_typings:
            type_counts[ap_type] = 0

        for ap_type in self.all_typings:
            type_counts[ap_type] += 1
        return dict(sorted(type_counts.items(), key=lambda item: item[1], reverse=True))

    def calculate_sexta_counts(self):
        sexta_counts = {}
        sexta_map = {
            # key is results aspects in alphabetical order
            'EF': 'Ena',
            'EL': 'Dio',
            'EV': 'Tria',
            'LV': 'Tessera',
            'FV': 'Pente',
            'FL': 'Exi'
        }
        for sexta in sexta_map.values():
            sexta_counts[sexta] = 0

        for ap_type in self.all_typings:
            results_aspects = ''.join(sorted([ap_type[0], ap_type[3]]))
            sexta = sexta_map[results_aspects]
            sexta_counts[sexta] += 1
        return dict(sorted(sexta_counts.items(), key=lambda item: item[1], reverse=True))

    def calculate_sexta_1pos_counts(self):
        sexta_1st_att_counts = {}
        sexta_map = {
            # key is unsorted results aspects
            'FE': 'Ena 1F 4E',
            'EF': 'Ena 1E 4F',
            'LE': 'Dio 1L 4E',
            'EL': 'Dio 1E 4L',
            'VE': 'Tria 1V 4E',
            'EV': 'Tria 1E 4V',
            'VL': 'Tessera 1V 4L',
            'LV': 'Tessera 1L 4V',
            'VF': 'Pente 1V 4F',
            'FV': 'Pente 1F 4V',
            'LF': 'Exi 1L 4F',
            'FL': 'Exi 1F 4L',
        }
        for sexta in sexta_map.values():
            sexta_1st_att_counts[sexta] = 0

        for ap_type in self.all_typings:
            results_aspects = f'{ap_type[0]}{ap_type[3]}'
            sexta = sexta_map[results_aspects]
            sexta_1st_att_counts[sexta] += 1
        return dict(sorted(sexta_1st_att_counts.items(), key=lambda item: item[1], reverse=True))

    def get_percentage(self, count: int) -> str:
        if len(self.all_typings) > 0:
            return f'{round(100 * count / len(self.all_typings))}%'
        return 'N/A'

    def calculate_attitude_counts(self):
        attitude_counts = {}
        for pos in range(1, 5):
            for aspect in ['V', 'L', 'F', 'E']:
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] = 0
        for ap_type in self.all_typings:
            for pos in range(1, 5):
                aspect = ap_type[pos - 1]
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] += 1
        return dict(sorted(attitude_counts.items(), key=lambda item: item[1], reverse=True))

    def calculate_functions_by_block(self, block: str, aspect1: str, aspect2: str):
        functions = [f'Functions with {block} block ({aspect1}+{aspect2})']
        for i in range(4):
            for j in range(i + 1, 4):
                count1 = sum(
                    1 for _ in filter(lambda type: type[i] == aspect1 and type[j] == aspect2, self.all_typings))
                count2 = sum(
                    1 for _ in filter(lambda type: type[i] == aspect2 and type[j] == aspect1, self.all_typings))

                aspect_string = f'{i + 1}+{j + 1}|{aspect1}+{aspect2}'
                aspect1_string = f'{i + 1}{aspect1}+{j + 1}{aspect2}'
                aspect2_string = f'{i + 1}{aspect2}+{j + 1}{aspect1}'

                def get_count_string(count, s):
                    if count == 0:
                        return f'no {s}'
                    return f'{count} {s} ({self.get_percentage(count)})'

                count1_string = get_count_string(count1, aspect1_string)
                count2_string = get_count_string(count2, aspect2_string)
                count_strings = [count1_string, count2_string]

                if count1 == 0 and count2 == 0:
                    aspects_string = 'None'
                    self.missing_pairs.append(aspect_string)
                    self.missing_pairs_dir.append(aspect1_string)
                    self.missing_pairs_dir.append(aspect2_string)
                else:
                    if count1 == 0:
                        self.missing_pairs_dir.append(aspect1_string)
                    elif count2 == 0:
                        self.missing_pairs_dir.append(aspect2_string)
                    if count2 > count1:
                        count_strings = reversed(count_strings)
                    total_string = f'{(count1 + count2)} ({self.get_percentage(count1 + count2)}) total'
                    aspects_string = f'{total_string} - {' and '.join(count_strings)}'

                functions.append(f'- {i + 1}+{j + 1}: {aspects_string}')
        self.functions_by_block.append(functions)

    def validate_ap_type(self, ap_type: str):
        if sorted(ap_type) != self.valid_types:
            raise ValueError(f'Invalid AP type: {ap_type}')


if __name__ == '__main__':
    TypingStats(include_celebrities=True, include_paid=False)

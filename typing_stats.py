# temporary script to calculate function/blocks that have been found with new typings
import itertools
from datetime import date


class TypingStats:
    # typing videos with new definitions
    celebrity_typings = [
        # From Celebrity Typing videos
        'EFVL',  # Chappell Roan
        'VLEF',  # Grimes
        'FLVE',  # Jenna Ortega
        'VELF',  # Rihanna
        'FVLE',  # Matthew Bellamy
        'VLFE',  # Philip DeFranco
        'LVFE',  # Sandra Bullock
        'FELV',  # Aaron Paul
        'VFLE',  # Gillian Anderson (? TBD)
        'VELF',  # Madonna
        'EVFL',  # Mr. Rogers
        'VLEF',  # Neil DeGrasse Tyson
        'FVLE',  # Adriana Lima
        'FEVL',  # Kate Moss
        'FLVE',  # Bailey Sarian
        'VLFE',  # Azealia Banks
        'FVEL',  # Sofia Isella
        'FVEL',  # Adrianne Lenker
        'VLFE',  # Owen Cook
        'LVFE',  # Nick LS De Cesare
        'VEFL',  # Kobe Bryant
        'FVEL',  # Bjork
        'EFVL',  # HRH Collection
        'VLFE',  # Bo Burnham
        'VELF',  # Seal
        'FLEV',  # Kurt Cobain
        'VELF',  # Paris Hilton
        'VEFL',  # Vic DiCara
        'FEVL',  # David Lynch
        'VLFE',  # Courtney Love
        'EFLV',  # Trisha Paytas
        'FELV',  # JMSN
        'LFVE',  # Carl Jung
        'VELF',  # Hayley Williams
        'VFEL',  # Chino Moreno
        'EVLF',  # Yorgos Lanthimos
        'EVLF',  # Taylor Swift
        'FEVL',  # Addison Rae
        'VELF',  # PinkPantheress
        'EVFL',  # Chester Bennington
        'FEVL',  # Michelle Pfeiffer
        'VELF',  # Brit Marling
        'EFVL',  # Nicki Minaj
        'FVLE',  # Lucy Lawless

        # From Theory videos
        'ELVF',  # Asmongold (4F: Refusing To Process the Aspect)
    ]
    community_typings = {
        # as of 3/14/2026
        'FVLE': 15,
        'FLVE': 13,
        'EVLF': 5,
        'ELVF': 5,
        'LVFE': 5,
        'LFVE': 2,
        'EVFL': 6,
        'EFVL': 6,
        'VLFE': 10,
        'VFLE': 11,
        'ELFV': 1,
        'EFLV': 2,
        'VFEL': 5,
        'VEFL': 6,
        'LFEV': 1,
        'LEFV': 0,
        'VLEF': 7,
        'VELF': 11,
        'FLEV': 5,
        'FELV': 5,
        'LVEF': 7,
        'LEVF': 2,
        'FVEL': 11,
        'FEVL': 6,
    }
    sorted_aspects = sorted('FELV')

    function_names = {
        '1+2': 'Lifeblood',
        '1+3': 'Security',
        '1+4': 'Launch',
        '2+3': 'Spin-out',
        '2+4': 'Haphazard',
        '3+4': 'Burnout'
    }

    def __init__(self, include_celebrities: bool = True, include_community: bool = False):
        typing_types = []
        for ap_type in self.celebrity_typings:
            self.validate_ap_type(ap_type)
        for ap_type in self.community_typings.keys():
            self.validate_ap_type(ap_type)

        if include_celebrities:
            typing_types.append('Celebrity')
            self.all_typings = self.celebrity_typings
        else:
            self.all_typings = []
        if include_community:
            typing_types.append('Paid')
            for ap_type, count in self.community_typings.items():
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
        self.block_counts = []
        self.functions_by_block = []

        # blocks
        self.calculate_blocks('Experiencer', 'V', 'F')
        self.calculate_blocks('Evaluator', 'L', 'E')

        self.calculate_blocks('Strategist', 'V', 'L')
        self.calculate_blocks('Reactivist', 'F', 'E')

        self.calculate_blocks('Conceptualist', 'V', 'E')
        self.calculate_blocks('Realist', 'L', 'F')

        print(f'{' & '.join(typing_types)} Typing Stats {date.today()}')

        print('Summary:')
        print(f'- {len(self.all_typings)} total typings')
        missing_types_suffix = self.get_missing_suffix(missing_types)
        print(f'- {unique_type_count} of 24 types{missing_types_suffix}')
        missing_pairs_suffix = self.get_missing_suffix(self.missing_pairs)
        print(f'- {36 - len(self.missing_pairs)} of 36 function/block pairs{missing_pairs_suffix}')
        missing_pairs_dir_suffix = self.get_missing_suffix(self.missing_pairs_dir)
        print(
            f'- {72 - len(self.missing_pairs_dir)} of 72 function/block pairs (directional){missing_pairs_dir_suffix}')

        print()
        print(f'Type counts{self.get_missing_suffix(missing_types)}')
        for ap_type, count in type_counts.items():
            print(f'- {ap_type}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Attitude counts{self.get_missing_suffix(attitude_counts)}')
        for key, count in attitude_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Sexta counts{self.get_missing_suffix(sexta_counts)}')
        for key, count in sexta_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        print()
        print(f'Sexta counts with 1st attitude{self.get_missing_suffix(sexta_1pos_counts)}')
        for key, count in sexta_1pos_counts.items():
            print(f'- {key}: {count} ({self.get_percentage(count)})')

        for i, block in enumerate(self.block_counts):
            if i % 2 == 0:
                print()
            print(block)

        for functions in self.functions_by_block:
            print()
            for function in functions:
                print(function)

    @staticmethod
    def get_missing_suffix(missing_list_or_counts) -> str:
        if isinstance(missing_list_or_counts, dict):
            missing_items = [key for key, count in missing_list_or_counts.items() if count == 0]
        else:
            missing_items = missing_list_or_counts

        if len(missing_items) == 0:
            return ''
        return f' - missing {len(missing_items)}: {', '.join(missing_items)}'

    @staticmethod
    def get_missing_count(counts: dict[str, int]) -> int:
        return sum(1 for count in counts.values() if count == 0)

    def calculate_type_counts(self):
        type_counts = {}

        # iterate over community_typings, which includes all types in standard order
        for ap_type in self.community_typings:
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
            for aspect in self.sorted_aspects:
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] = 0
        for ap_type in self.all_typings:
            for pos in range(1, 5):
                aspect = ap_type[pos - 1]
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] += 1
        return dict(sorted(attitude_counts.items(), key=lambda item: item[1], reverse=True))

    def calculate_blocks(self, block: str, aspect1: str, aspect2: str):
        functions = ['']  # placeholder
        first_aspect_count = 0
        for i in range(4):
            for j in range(i + 1, 4):
                count1 = sum(
                    1 for _ in filter(lambda t: t[i] == aspect1 and t[j] == aspect2, self.all_typings))
                count2 = sum(
                    1 for _ in filter(lambda t: t[i] == aspect2 and t[j] == aspect1, self.all_typings))

                if i == 0:
                    first_aspect_count += count1 + count2

                aspects = f'{i + 1}+{j + 1}'

                aspect_string = f'{aspects}|{aspect1}+{aspect2}'
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

                functions.append(f'- {aspects} ({self.function_names[aspects]}): {aspects_string}')
        functions[0] = f'Functions with {block} block ({aspect1}+{aspect2})'
        self.block_counts.append(f'{first_aspect_count} {block}s ({self.get_percentage(first_aspect_count)})')
        self.functions_by_block.append(functions)

    def validate_ap_type(self, ap_type: str):
        if sorted(ap_type) != self.sorted_aspects:
            raise ValueError(f'Invalid AP type: {ap_type}')


if __name__ == '__main__':
    TypingStats(include_celebrities=True, include_community=False)

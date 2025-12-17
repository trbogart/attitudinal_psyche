# temporary script to calculate function/blocks that have been found with new typings
import itertools


class TypingStats:
    # typing videos with new definitions
    celebrity_typings = [
        'FVLE',  # Adriana Lima 9/8
        # 'VFEL', # Kate Moss 9/15
        'FLVE',  # Bailey Sarian 9/22
        'VLFE',  # Azealia Banks 9/23
        'FVEL',  # Sofia Isella 9/29
        'FVEL',  # Adrianne Lenker 10/3
        'VLFE',  # Owen Cook 10/6
        'LVFE',  # Nick LS De Cesare 10/10
        'VEFL',  # Kobe Bryant 10/14
        'FVEL',  # Bjork 10/18
        'EFVL',  # HRH Collection 10/21
        'VLFE',  # Bo Burnham 10/27
        'VELF',  # Seal 11/3
        'ELVF',  # Asmongold 11/6 (theory)
        'FLEV',  # Kurt Cobain 11/10
        'FEVL',  # Kate Moss 11/17
        'VELF',  # Paris Hilton 11/30
        'VEFL',  # Vic DiCara 12/8
        'FEVL',  # David Lynch 12/12
        'VLFE',  # Courtney Love 12/15
    ]
    paid_typings = {
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

        self.type_set = set(self.all_typings)
        self.pair_count = 0
        self.pair_count_directional = 0

        self.attitude_counts = self.calculate_attitude_counts()

        self.missing_types = [ap_type for ap_type in self.paid_typings.keys() if ap_type not in self.type_set]

        print(f'Missing types ({len(self.missing_types)})')
        if len(self.missing_types) == 0:
            print('- None')
        else:
            for ap_type in self.missing_types:
                print(f'- {ap_type}')
        print()

        print(f'Attitude counts:')
        for key, count in self.attitude_counts.items():
            print(f'- {key}: {count}')
        print()

        # blocks
        self.print_blocks('Strategist', 'V', 'L')
        self.print_blocks('Reactivist', 'F', 'E')

        self.print_blocks('Experiencer', 'V', 'F')
        self.print_blocks('Evaluator', 'L', 'E')

        self.print_blocks('Conceptualist', 'V', 'E')
        self.print_blocks('Realist', 'L', 'F')

        print('Summary:')
        print(f'- {len(self.all_typings)} typings')
        print(f'- {len(self.type_set)} of 24 types ({len(self.all_typings) - len(self.type_set)} duplicates)')
        print(f'- {self.pair_count} of 36 unique function/block pairs')
        print(f'- {self.pair_count_directional} of 72 unique function/block pairs (directional)')

    def calculate_attitude_counts(self):
        attitude_counts = {}
        for pos in range(1, 5):
            for aspect in ['V', 'L', 'F', 'E']:
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] = 0
        for ap_type in self.all_typings:
            for pos in range(1, 5):
                aspect = ap_type[pos-1]
                attitude = f'{pos}{aspect}'
                attitude_counts[attitude] += 1
        return dict(sorted(attitude_counts.items(), key=lambda item: item[1], reverse=True))

    def print_blocks(self, block: str, aspect1: int, aspect2: int):
        print(f'Functions with {block} block ({aspect1}+{aspect2})')
        for i in range(4):
            for j in range(i+1, 4):
                aspect_counts = []
                count1 = sum(1 for _ in filter(lambda type: type[i] == aspect1 and type[j] == aspect2, self.all_typings))
                count2 = sum(1 for _ in filter(lambda type: type[i] == aspect2 and type[j] == aspect1, self.all_typings))

                if count1 > 0:
                    aspect_counts.append(f'{count1} {i+1}{aspect1}+{j+1}{aspect2}')
                if count2 > 0:
                    aspect_counts.append(f'{count2} {i+1}{aspect2}+{j+1}{aspect1}')
                if aspect_counts:
                    self.pair_count = self.pair_count + 1
                    self.pair_count_directional = self.pair_count_directional + len(aspect_counts)
                    aspects_string = f'{count1 + count2} total ({' and '.join(aspect_counts)})'
                else:
                    aspects_string = 'None'
                print(f'- {i+1}+{j+1}: {aspects_string}')
        print()

    def validate_ap_type(self, ap_type: str):
        if sorted(ap_type) != self.valid_types:
            raise ValueError(f'Invalid AP type: {ap_type}')

if __name__ == '__main__':
    TypingStats(include_celebrities=True, include_paid=False)
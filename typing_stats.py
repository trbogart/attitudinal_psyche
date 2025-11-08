# temporary script to calculate function/blocks that have been found with new typings

# typing videos with function/block
typing_videos = [
    'FVLE', # Adriana Lima 9/8
    'VFEL', # Kate Moss 9/15
    'FLVE', # Bailey Sarian 9/22
    'VLFE', # Azealia Banks 9/23
    'FVEL', # Sofia Isella 9/29
    'FVEL', # Adrianne Lenker 10/3
    'VLFE', # Owen Cook 10/6
    'LVFE', # Nick LS De Cesare 10/10
    'VEFL', # Kobe Bryant 10/14
    'FVEL', # Bjork 10/18
    'EFVL', # HRH Collection 10/21
    'VLFE', # Bo Burnham 10/27
    'VELF', # Seal 11/3
    'ELVF', # Asmongold 11/6 (theory)
]

class TypingStats:
    # TODO keep track of counts and/or specific types
    def __init__(self):
        self.type_set = set(typing_videos)
        self.pair_count = 0
        self.pair_count_directional = 0

        self.missing_attitudes = self.calculate_missing_attitudes()

        from itertools import permutations
        self.missing_types = [''.join(ap_type) for ap_type in permutations('VLFE') if ''.join(ap_type) not in self.type_set]

        print(f'Missing attitudes ({len(self.missing_attitudes)}):')
        if len(self.missing_attitudes) == 0:
            print('- None')
        else:
            for attitude in self.missing_attitudes.keys():
                print(f'- {attitude}')
        print()

        print(f'Missing types ({len(self.missing_types)})')
        if len(self.missing_types) == 0:
            print('- None')
        else:
            for ap_type in self.missing_types:
                print(f'- {ap_type}')
        print()

        # blocks
        self.print_blocks('Strategist', 'V', 'L')
        self.print_blocks('Reactivist', 'F', 'E')

        self.print_blocks('Experiencer', 'V', 'F')
        self.print_blocks('Evaluator', 'L', 'E')

        self.print_blocks('Conceptualist', 'V', 'E')
        self.print_blocks('Realist', 'L', 'F')

        print('Summary:')
        print(f'- {len(typing_videos)} typing videos with functions and blocks')
        print(f'- {len(self.type_set)} of 24 types')
        print(f'- {16-len(self.missing_attitudes)} of 16 attitudes')
        print(f'- {self.pair_count} of 36 unique function/block pairs')
        print(f'- {self.pair_count_directional} of 72 unique function/block pairs (directional)')

    def calculate_missing_attitudes(self):
        missing_attitudes = {}
        for pos in range(1, 5):
            for aspect in ['V', 'L', 'F', 'E']:
                attitude = f'{pos}{aspect}'
                missing_attitudes[attitude] = None
        for typings in self.type_set:
            for i, aspect in enumerate(typings):
                attitude = f'{i + 1}{aspect}'
                if attitude in missing_attitudes:
                    del missing_attitudes[attitude]
        return missing_attitudes

    def print_blocks(self, block, aspect1, aspect2):
        print(f'Functions with {block} ({aspect1}+{aspect2})')
        for i in range(4):
            for j in range(i+1, 4):
                aspects = []
                if any(type[i] == aspect1 and type[j] == aspect2 for type in self.type_set):
                    aspects.append(f'{aspect1}{aspect2}')
                if any(type[i] == aspect2 and type[j] == aspect1 for type in self.type_set):
                    aspects.append(f'{aspect2}{aspect1}')
                if aspects:
                    self.pair_count = self.pair_count + 1
                    self.pair_count_directional = self.pair_count_directional + len(aspects)
                    aspects_string = ' and '.join(aspects)
                else:
                    aspects_string = 'None'
                print(f'- {i+1}+{j+1} {block}: {aspects_string}')
        print()

if __name__ == '__main__':
    TypingStats()
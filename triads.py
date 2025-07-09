import argparse
import sys

# List triad counts, nicknames, and other information for Enneagram trifixes ([234][567][891] in any order) or
# Expanded Instincts (EI) archetypes, e.g. SY-CY-FD, also in any order.

# For EI, an optional center stacking (any permutation of SIP) may be used to override the ordering.

# group of 3 triads
class TriadGroup:
    def __init__(self, name: str, triads_and_values: dict[str, list[str]]):
        self.name = name
        self.triads_and_values = triads_and_values

        # build reverse map by value (Enneagram type or EI instinct)
        self.triads_by_value = {}
        self.triad_counts = {}
        for triad, values in triads_and_values.items():
            self.triad_counts[triad] = 0
            for value in values:
                self.triads_by_value[value] = triad

    def max_count(self) -> int:
        return max(self.triad_counts.values())

    def add(self, value: str) -> None:
        self.triad_counts[self.triads_by_value[value]] += 1

    def __repr__(self) -> str:
        sorted_counts_by_triad = sorted(self.triad_counts.items(), key=lambda item: item[1], reverse=True)
        counts = ', '.join([f'{count}x {triad}' for triad, count in sorted_counts_by_triad])

        return f'{self.name}: {counts}'

class Centers(TriadGroup):
    def __init__(self, name: str, triads_and_values: dict[str, list[str]]):
        super().__init__(name, triads_and_values)
        self.canonical_values = {}

    def get_canonical_values(self) -> list[str]:
        return [self.canonical_values[triad] for triad in self.triads_and_values.keys()]

    def add(self, value: str) -> None:
        super().add(value)
        self.canonical_values[self.triads_by_value[value]] = value

    # validate that there is exactly one value in each triad
    def validate_centers(self) -> None:
        for key, count in self.triad_counts.items():
            if count != 1:
                raise ValueError()

def order_triads(triad_groups: list[TriadGroup]) -> list[TriadGroup]:
    # Put group with a triple first (max 1), then groups with a double, then evenly divided groups
    # In practice, there will either be a single group with a triple value (e.g. 3x attachment) and other groups with 1x each,
    # or all 3 groups will contain 2x/1x/0x pattern.
    return sorted(triad_groups, key=lambda group: group.max_count(), reverse=True)

def get_results(triad_groups: list[TriadGroup]) -> list[str]:
    return [str(group) for group in order_triads(triad_groups)]

class InvalidValue(ValueError):
    def __init__(self, trifix_or_archetype: str):
        super().__init__(f'Invalid trifix (e.g. "369") or EI archetype with optional center stacking (e.g. "BG-FD-EX" or "SPI SY-CY-UN"): {trifix_or_archetype}')

# triads for enneagram trifix, e.g. 592
def get_trifix_triads(input: str) -> list[str]:
    # validate trifix
    if len(input) != 3:
        raise InvalidValue(input)
    trifix = input.upper()

    # centers, used for validation only
    centers = Centers('centers', {
        'gut': ['8', '9', '1'],
        'image': ['2', '3', '4'],
        'head': ['5', '6', '7']
    })

    try:
        for enneagram_type in trifix:
            centers.add(enneagram_type)
        centers.validate_centers()
    except:
        raise InvalidValue(input)

    object_relation_triads = TriadGroup('Object relation triads', {
        'frustration': ['1', '4', '7'],
        'rejection': ['2', '5', '8'],
        'attachment': ['3', '6', '9']
    })

    harmonic_triads = TriadGroup('Harmonic triads', {
        'competency': ['1', '3', '5'],
        'positive outlook': ['2', '7', '9'],
        'reactive': ['4', '6', '8']
    })

    hornevian_triads = TriadGroup('Hornevian triads', {
        'superego': ['1', '2', '6'],
        'assertive': ['3', '7', '8'],
        'withdrawn': ['4', '5', '9']
    })
    for enneagram_type in trifix:
        object_relation_triads.add(enneagram_type)
        harmonic_triads.add(enneagram_type)
        hornevian_triads.add(enneagram_type)

    canonical_trifix = ''.join(sorted(trifix))
    nicknames = {
        '125': 'Friendzone/Librarian',
        '126': 'Ball Buster/OK Boomer',
        '127': 'Cool Teacher',
        '135': 'Robo-Celibate',
        '136': 'Middle Manager',
        '137': 'Welcome to My Ted Talk',
        '145': 'Insectoid',
        '146': 'Big Pain',
        '147': 'Princess and the Pea',
        '258': 'Cult Classic',
        '259': 'Spineless Saint',
        '268': 'I Want Her To Fly',
        '269': 'Stockholm Syndrome',
        '278': 'Smothering Jazz Hands',
        '279': 'Hippie Burnout',
        '358': 'American Psycho',
        '359': 'Flatlined',
        '368': 'Kyle/Kylie',
        '369': 'Bermuda Triangle',
        '378': 'Chad/Stacie',
        '379': 'DJ',
        '458': 'Useless Beast',
        '459': 'Hateful Ghost',
        '468': 'Public Display of Affliction',
        '469': 'Whiny Tears',
        '478': 'Revolving Door Rehab',
        '479': 'Huh?',
    }

    results = [f'Triads for {canonical_trifix} trifix ({nicknames[canonical_trifix]}):']
    results.extend(get_results([object_relation_triads, harmonic_triads, hornevian_triads]))
    return results

# get triads for Expanded Instincts archetype
def get_archetype_triads(input: str) -> list[str]:
    if ' ' in input:
        # center stacking given explicitly
        tokens = input.upper().split(' ')
        center_stacking = tokens[0]
        archetype = tokens[1]
    else:
        center_stacking = None # will be calculated later
        archetype = input.upper()

    instincts = archetype.split('-')
    # validate archetype
    if len(instincts) != 3:
        raise InvalidValue(input)

    # centers, used for validation only
    centers = Centers('centers', {
        'SUR': ['FD', 'SY', 'SM'],
        'INT': ['AY', 'CY', 'BG'],
        'PUR': ['SS', 'EX', 'UN']
    })

    try:
        for instinct in instincts:
            centers.add(instinct)
        centers.validate_centers()
    except:
        raise InvalidValue(input)

    experiential_triads = TriadGroup('Experiential triads', {
        'memorial': ['SM', 'BG', 'UN'],
        'immersion': ['AY', 'SS', 'FD'],
        'distinction': ['SY', 'CY', 'EX']
    })

    movement_triads = TriadGroup('Movement triads', {
        'escaping (yin)': ['SY', 'AY', 'UN'],
        'aligning (neutral)': ['SM', 'CY', 'SS'],
        'directing (yang)': ['FD', 'BG', 'EX']
    })

    source_triads = TriadGroup('Source triads', {
        'internalizing': ['SY', 'BG', 'SS'],
        'externalizing': ['FD', 'CY', 'UN'],
        'exchanging': ['SM', 'AY', 'EX']
    })
    for instinct in instincts:
        experiential_triads.add(instinct)
        movement_triads.add(instinct)
        source_triads.add(instinct)

    nicknames = {
        'SY-CY-EX': 'Existence Catalog',
        'SY-CY-SS': 'Center of the Universe',
        'SY-CY-UN': 'Tweaked-out Architect',
        'SY-AY-EX': 'Whiny Popstar',
        'SY-BG-EX': 'Soap Opera',
        'SY-AY-SS': 'Sex Vortex',
        'SY-BG-UN': 'Pixelated Dreamscape',
        'SY-AY-UN': 'Dance, Monkey!',
        'SY-BG-SS': 'Constant Inner Voice',
        'FD-CY-EX': 'Clown Car CEO',
        'FD-CY-SS': 'Rags-to-Riches',
        'FD-CY-UN': 'Apocalypse Adventurer',
        'FD-AY-EX': 'Soul Harvester',
        'FD-BG-EX': 'Social Experiment',
        'FD-AY-SS': 'Rubberneck Trainwreck',
        'FD-BG-UN': 'Dazzling Kamikaze',
        'FD-AY-UN': 'Astral Succubus',
        'FD-BG-SS': 'Domination Station',
        'SM-CY-EX': 'NPC Theatre Kid',
        'SM-CY-SS': 'Kiss The Ring',
        'SM-CY-UN': 'Spiritual Fuckboi',
        'SM-AY-EX': 'Doppelgänger',
        'SM-BG-EX': 'Otherworldly Communion',
        'SM-AY-SS': 'Tesla Sexbot',
        'SM-BG-UN': 'Delayed Response Unit',
        'SM-AY-UN': 'Edgers Anonymous',
        'SM-BG-SS': 'Perfect Delusion'
    }
    if center_stacking:
        # given center stacking, so recalculate archetype based on center stacking
        fixed_instincts = []
        for center in center_stacking:
            for instinct in instincts:
                if centers.triads_by_value[instinct][0] == center:
                    fixed_instincts.append(instinct)
                    break
        archetype = '-'.join(fixed_instincts)
    else:
        # calculate center stacking based on instincts (use first letter of center, e.g. INT to I)
        center_stacking = ''.join(map(lambda instinct: centers.triads_by_value[instinct][0], instincts))

    canonical_archetype = '-'.join(centers.get_canonical_values()) # sort in SUR-INT-PUR order
    header = f'Triads for {center_stacking} {archetype} ({nicknames[canonical_archetype]}):'
    results = [header]
    results.extend(get_results([experiential_triads, movement_triads, source_triads]))

    # resonant/dissonant with center stacking
    resonant_instincts = {
        'SIP': ['FD', 'CY'],
        'SPI': ['SM', 'EX'],
        'IPS': ['AY', 'EX'],
        'ISP': ['BG', 'SY'],
        'PSI': ['SS', 'SY'],
        'PIS': ['UN', 'CY'],
    }
    dissonant_instincts = {
        'SIP': ['SM', 'BG'],
        'SPI': ['FD', 'SS'],
        'IPS': ['UN', 'BG'],
        'ISP': ['AY', 'FD'],
        'PSI': ['UN', 'SS'],
        'PIS': ['AY', 'SM'],
    }

    def get_instincts(instincts_by_center: dict[str, list[str]]) -> str:
        instincts_for_center = instincts_by_center[center_stacking]
        stacking_instincts = list(filter(lambda instinct: instinct in instincts_for_center, instincts))
        if stacking_instincts:
            return '/'.join(stacking_instincts)
        return 'none'

    results.append(f'Resonant instincts for {center_stacking}: {get_instincts(resonant_instincts)} '
                   f'(most resonant {'/'.join(resonant_instincts[center_stacking])})')
    results.append(f'Dissonant instincts for {center_stacking}: {get_instincts(dissonant_instincts)} '
                   f'(most dissonant {'/'.join(dissonant_instincts[center_stacking])})')

    return results

def get_triads(trifix_or_archetype: str) -> list[str]:
    if len(trifix_or_archetype) == 3:
        return get_trifix_triads(trifix_or_archetype)
    else:
        return get_archetype_triads(trifix_or_archetype)

def run_interactive() -> None:
    while True:
        try:
            trifix_or_archetype = input('Enter trifix (e.g. 936) or EI archetype (e.g. EX-SY-BG), in any order (Q to quit): ')
            if trifix_or_archetype == 'Q':
                sys.exit(0)
            print('\n- '.join(get_triads(trifix_or_archetype)))
        except ValueError as e:
            print(f'{e.args[0]}')
        print()

def run_with_args(trifix_or_archetype: str) -> None:
    try:
        print('\n- '.join(get_triads(trifix_or_archetype)))
    except ValueError as e:
        sys.stderr.write(f'{e.args[0]}\n')
        exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # interactive mode, ask user for Enneagram trifix (e.g. 548) or Expanded Instincts type (e.g. UN-SY-FD)
        while True:
            run_interactive()
    else:
        parser = argparse.ArgumentParser(
            prog = 'ap_shadow_type_calculator',
            usage = 'Calculate AP shadow types (no arguments to run interactively)',
            add_help = True, # add -h/--help option
        )
        parser.add_argument('trifix_or_archetype', help = 'Enneagram trifix (e.g. 925) or EI archetype (e.g. EX-SY-BG), in any order')
        args = parser.parse_args()
        run_with_args(args.trifix_or_archetype)

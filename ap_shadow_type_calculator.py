# Licensed under the Creative Commons BY license:
# https://creativecommons.org/licenses/by/4.0/

# To run the script in interactive mode:
#   python ap_shadow_type_calculator.py
# To run the script with arguments:
#   python ap_shadow_type_calculator.py [AP type] [subtype]

import argparse
import sys

verbose = False

class SubType:
    def __init__(self, ap_type, source_pos, target_pos):
        self.source_pos = source_pos
        self.target_pos = target_pos
        self.aspect = ap_type[source_pos - 1]

    def get_type(self):
        if self.source_pos == self.target_pos:
            return 'Accentuated'
        elif self.target_pos == 0:
            return 'obscured'
        elif self.is_subtype_type(2, 3) or self.is_subtype_type(1, 4):
            return 'method'
        elif self.is_subtype_type(1, 2) or self.is_subtype_type(3, 4):
            return 'self'
        elif self.is_subtype_type(1, 3) or self.is_subtype_type(2, 4):
            return 'others'
        else:
            raise ValueError(f'Invalid subtype: {self}') # shouldn't happen

    # string form, including aspect, e.g. 1E-1
    def __repr__(self):
        return f'{self.source_pos}{self.aspect}-{self.target_pos} ({self.get_type()})'

    def __hash__(self):
        return hash((self.source_pos, self.target_pos))

    def __eq__(self, other):
        return self.source_pos == other.source_pos and self.target_pos == other.target_pos

    def is_subtype_type(self, pos1, pos2):
        return (self.source_pos == pos1 and self.target_pos == pos2 or
                self.source_pos == pos2 and self.target_pos == pos1)

class ShadowTypes:
    def __init__(self, ap_type_str: str, subtype_str: str):
        self.ap_type_str = ap_type_str.strip().upper()
        self.subtype_str = subtype_str.strip()

        validate_ap_type(self.ap_type_str)
        validate_subtype(self.subtype_str)

        self.last_shadow_type = list(self.ap_type_str) # will be mutated to latest shadow type
        self.original_ap_type = self.last_shadow_type[:]

        self.subtypes = [SubType(self.last_shadow_type, i + 1, int(c)) for i, c in enumerate(self.subtype_str)]

        self.shadow_types = {self.ap_type_str: "AP type"}
        self.swapped_to_obscured = set() # set of SubTypes that have already been swapped

        # attenuated and obscured aspects are not moved

        # swap subtypes pointing to an obscured aspect first, unless it has another aspect pointing at it
        # these would be swapped later anyway, but do it early in this case
        for subtype in self.subtypes:
            if subtype.target_pos == 0: # obscured
                self.swap_obscured_shadow_type(subtype)

        # swap method subtypes
        self.swap_shadow_type(2, 3) # 2-3 or 3-2
        self.swap_shadow_type(1, 4) # 1-4 or 4-1

        # swap self subtypes
        self.swap_shadow_type(1, 2) # 1-2 or 2-1
        self.swap_shadow_type(3, 4) # 3-4 or 4-3

        # swap others subtypes
        self.swap_shadow_type(1, 3) # 1-3 or 3-1
        self.swap_shadow_type(2, 4) # 2-4 or 4-2

    def description(self) -> str:
        return f'{self.ap_type_str} {self.subtype_str}'

    def swap(self, subtype: SubType, obscured_subtype: SubType = None) -> None:
        if subtype in self.swapped_to_obscured:
            debug(f'Skipped {subtype} - already swapped')
            return

        pos1 = self.last_shadow_type.index(subtype.aspect) + 1 # position currently containing aspect
        pos2 = subtype.target_pos

        if pos1 == pos2:
            # subtypes in the same pair, e.g. 2-3 or 3-2, ignore
            # this case will usually produce the same result, but can
            shadow_type_str = ''.join(self.last_shadow_type)
            # this can happen for subtypes in the same pair, e.g. 2-3 and 3-2
            debug(f'Already swapped {subtype}')
            self.shadow_types[shadow_type_str] = f'{self.shadow_types[shadow_type_str]} and {subtype}'
        else:
            self.last_shadow_type[pos1 - 1], self.last_shadow_type[pos2 - 1] = self.last_shadow_type[pos2 - 1], self.last_shadow_type[pos1 - 1]
            shadow_type_str = ''.join(self.last_shadow_type)
            debug(f'swapped {subtype} -> {shadow_type_str}')
            if obscured_subtype:
                self.shadow_types[shadow_type_str] = f'swapped {subtype} for {obscured_subtype}'
            else:
                self.shadow_types[shadow_type_str] = f'swapped {subtype}'

    def swap_obscured_shadow_type(self, obscured_subtype: SubType) -> None:
        swap_subtype = None
        for other_subtype in self.subtypes:
            if other_subtype.target_pos == obscured_subtype.source_pos: # obscured
                if swap_subtype:
                    # multiple matches, do not swap
                    debug(f'Skipped {obscured_subtype} - multiple matches')
                    return
                swap_subtype = other_subtype
        if swap_subtype:
            self.swap(swap_subtype, obscured_subtype)
            self.swapped_to_obscured.add(swap_subtype)
        else:
            debug(f'Skipped {obscured_subtype} - no matches')

    def swap_shadow_type(self, pos1: int, pos2: int):
        for subtype in self.subtypes:
            if subtype.is_subtype_type(pos1, pos2):
                self.swap(subtype)

def input_ap_type() -> str:
    while True:
        ap_type_str = input('Enter AP type (q to quit): ').strip()
        if ap_type_str in {'q', 'Q'}:
            sys.exit(0)
        try:
            validate_ap_type(ap_type_str)
            return ap_type_str
        except ValueError as e:
            print(f'{e.args[0]}')

def input_subtype() -> str:
    while True:
        subtype_str = input('Enter AP subtype (q to quit): ').strip()
        if subtype_str in {'q', 'Q'}:
            exit(0)
        try:
            validate_subtype(subtype_str)
            return subtype_str
        except ValueError as e:
            print(f'{e.args[0]}')

def validate_ap_type(ap_type_str: str) -> None:
    if len(ap_type_str) != 4 or sorted(ap_type_str.upper()) != ['E', 'F', 'L', 'V']:
        raise ValueError(f'Invalid AP type {ap_type_str}')

def validate_subtype(subtype_str: str) -> None:
    if len(subtype_str) != 4 or not all(map(lambda c: '0' <= c <= '4', subtype_str)):
        raise ValueError(f'Invalid subtype {subtype_str}')

def print_shadow_types(ap_type_str: str, subtype_str: str) -> None:
    shadow_types = ShadowTypes(ap_type_str, subtype_str)
    print(f'Shadow types for {shadow_types.description()}')
    for shadow_type, reason in shadow_types.shadow_types.items():
        print(f'- {shadow_type}: {reason}')

def run_interactive() -> None:
    ap_type_str = input_ap_type()
    subtype_str = input_subtype()
    print_shadow_types(ap_type_str, subtype_str)
    print()

def run_with_args(ap_type_str: str, subtype_str: str) -> None:
    try:
        print_shadow_types(ap_type_str, subtype_str)
    except ValueError as e:
        sys.stderr.write(f'{e.args[0]}\n')
        exit(1)

def debug(s) -> None:
    if verbose:
        print(s)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # interactive mode, ask user for AP type and subtype, repeating until q is entered
        while True:
            run_interactive()
    else:
        parser = argparse.ArgumentParser(
            'ap_shadow_type_calculator',
            'Calculate AP shadow types (no arguments to run interactively)',
        )
        parser.add_argument('ap_type')
        parser.add_argument('subtype')
        args = parser.parse_args()
        run_with_args(args.ap_type, args.subtype)

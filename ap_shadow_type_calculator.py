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
        if source_pos == target_pos:
            self.subtype_type = 'A'
            self.type_description = 'Accentuated'
        elif target_pos == 0:
            self.subtype_type = 'O' # obscured
            self.type_description = 'obscured'
        elif self._is_subtype_type(2, 3):
            self.subtype_type = 'M1' # method priority 1 (2-3 or 3-2)
            self.type_description = 'method'
        elif self._is_subtype_type(1, 4):
            self.subtype_type = 'M2' # method priority 2 (1-4 or 4-1)
            self.type_description = 'method'
        elif self._is_subtype_type(1, 2):
            self.subtype_type = 'S1'  # self priority 1 (1-2 or 2-1)
            self.type_description = 'self'
        elif self._is_subtype_type(3, 4):
            self.subtype_type = 'S2'  # self priority 2 (3-4 or 4-3)
            self.type_description = 'self'
        elif self._is_subtype_type(1, 3):
            self.subtype_type = 'O1'  # self priority 1 (1-3 or 3-1)
            self.type_description = 'others'
        elif self._is_subtype_type(2, 4):
            self.subtype_type = 'O2'  # self priority 2 (2-4 or 4-2)
            self.type_description = 'others'
        else:
            raise ValueError(f'Invalid subtype: {self}')

    def __repr__(self):
        return f'{self.source_pos}{self.aspect}-{self.target_pos} ({self.type_description})'

    def __hash__(self):
        return hash((self.source_pos, self.target_pos))

    def __eq__(self, other):
        return self.source_pos == other.source_pos and self.target_pos == other.target_pos

    def _is_subtype_type(self, pos1, pos2):
        return (self.source_pos == pos1 and self.target_pos == pos2 or
                self.source_pos == pos2 and self.target_pos == pos1)

class ShadowTypes:
    def __init__(self, ap_type_str: str, subtype_str: str):
        validate_ap_type(ap_type_str)
        validate_subtype(subtype_str)

        self.ap_type_str = ap_type_str.upper()
        self.last_shadow_type_str = list(self.ap_type_str) # will be mutated to latest shadow type
        self.original_ap_type = self.last_shadow_type_str[:]

        self.subtype_str = subtype_str
        self.subtypes = [SubType(self.last_shadow_type_str, i + 1, int(c)) for i, c in enumerate(subtype_str)]

        self.shadow_types = {self.ap_type_str: "AP type"}
        self.swapped_to_obscured = set() # set of SubTypes that have already been swapped

        # Do subtypes pointing to an obscured aspect first, unless it has another aspect pointing at it
        for subtype in self.subtypes:
            if subtype.subtype_type == 'O':
                self.swap_obscured_shadow_type(subtype)

        self.swap_shadow_type('M1') # Method 2-3 or 3-2
        self.swap_shadow_type('M2') # Method 1-4 or 4-1

        self.swap_shadow_type('S1') # Self 1-2 or 2-1
        self.swap_shadow_type('S2') # Self 3-4 or 4-3

        self.swap_shadow_type('O1') # Other 1-3 or 3-1
        self.swap_shadow_type('O2') # Other 2-4 or 4-2

    def description(self) -> str:
        return f'{self.ap_type_str} {self.subtype_str}'

    def swap(self, subtype: SubType, obscured_subtype: SubType = None) -> None:
        if subtype in self.swapped_to_obscured:
            debug(f'Skipped {subtype} - already swapped')
            return

        pos1 = self.last_shadow_type_str.index(subtype.aspect) + 1
        pos2 = subtype.target_pos

        if pos1 == pos2:
            # subtypes in the same pair, e.g. 2-3 or 3-2, will usually produce the same result, ignore
            shadow_type_str = ''.join(self.last_shadow_type_str)
            # this can happen for subtypes in the same pair, e.g. 2-3 and 3-2
            debug(f'Already swapped {subtype}')
            self.shadow_types[shadow_type_str] = f'{self.shadow_types[shadow_type_str]} and {subtype}'
        else:
            self.last_shadow_type_str[pos1 - 1], self.last_shadow_type_str[pos2 - 1] = self.last_shadow_type_str[pos2 - 1], self.last_shadow_type_str[pos1 - 1]
            shadow_type_str = ''.join(self.last_shadow_type_str)
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

    def swap_shadow_type(self, subtype_type: str):
        for subtype in self.subtypes:
            if subtype.subtype_type == subtype_type:
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

# Licensed under the Creative Commons BY license:
# https://creativecommons.org/licenses/by/4.0/

# To run the script in interactive mode:
#   python ap_shadow_type_calculator.py
# To run the script with arguments:
#   python ap_shadow_type_calculator.py [AP type] [subtype]

import argparse
import sys

class ShadowTypes:
    def __init__(self, ap_type_str: str, subtype_str: str):
        validate_ap_type(ap_type_str)
        validate_subtype(subtype_str)

        self.ap_type_str = ap_type_str.upper()
        self.shadow_type = list(self.ap_type_str)

        self.subtype_str = subtype_str
        self.subtype = {i + 1: int(c) for i, c in enumerate(subtype_str)}

        self.steps = []
        self.shadow_types = [self.ap_type_str]
        self.swapped_pairs = set()

        # Step 1 - Accentuated - Ignore

        # Step 2 - Obscured - Any aspect pointing at an obscured position (x-0) switches
        # with it, unless it has another aspect pointing at it
        for pos, pos_subtype in self.subtype.items():
            if pos_subtype == 0:  # obscured
                self.swap_obscured_shadow_type(pos)

        # Step 3 - Method - Switch aspects in this order: 2-3 or 3-2 > 1-4 or 4-1
        self.swap_shadow_type('Method 2-3', 2, 3)
        self.swap_shadow_type('Method 1-4', 1, 4)

        # Step 4 - Self - Switch aspects in this order: 1-2 or 2-1 > 3-4 or 4-3
        self.swap_shadow_type('Self 1-2', 1, 2)
        self.swap_shadow_type('Self 3-4', 3, 4)

        # Step 5 - Others - Switch aspects in this order: 1-3 or 3-1 > 2-4 or 4-2
        self.swap_shadow_type('Others 1-3', 1, 3)
        self.swap_shadow_type('Others 2-4', 2, 4)


    def description(self):
        return f'{self.ap_type_str} {self.subtype_str}'

    def swap_positions(self, description: str, pos1: int, pos2: int):
        if pos1 > pos2:
            pair = f'{pos2}-{pos1}'
        else:
            pair = f'{pos1}-{pos2}'
        if pair in self.swapped_pairs:
            self.steps.append(f'Skip {description} - already swapped')
            return

        self.swapped_pairs.add(pair)

        self.shadow_type[pos1 - 1], self.shadow_type[pos2 - 1] = self.shadow_type[pos2 - 1], self.shadow_type[pos1 - 1]
        shadow_type_str = ''.join(self.shadow_type)
        self.steps.append(f'Swap {description} -> {shadow_type_str}')
        self.shadow_types.append(shadow_type_str)

    def swap_obscured_shadow_type(self, pos: int):
        swap_pos = 0
        for other_pos, pos_subtype in self.subtype.items():
            if pos_subtype == pos:
                if swap_pos > 0:
                    # multiple matches, do not swap
                    self.steps.append(f'Skip Obscured {pos} - multiple matches')
                    return
                swap_pos = other_pos
        if swap_pos > 0:
            self.swap_positions(f'Obscured {pos}-{swap_pos}', pos, swap_pos)
        else:
            self.steps.append(f'Skip Obscured {pos} - no matches')

    def swap_shadow_type(self, description: str, pos1: int, pos2: int):
        if self.subtype[pos1] == pos2 or self.subtype[pos2] == pos1:
            self.swap_positions(description, pos1, pos2)
        else:
            self.steps.append(f'Skip {description}')

def input_ap_type() -> str:
    while True:
        ap_type_str = input('Enter AP type (q to quit): ')
        if ap_type_str in {'q', 'Q'}:
            sys.exit(0)
        try:
            validate_ap_type(ap_type_str)
            return ap_type_str
        except ValueError as e:
            print(f'{e.args[0]}')

def input_subtype() -> str:
    while True:
        subtype_str = input('Enter AP subtype (q to quit): ')
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

def print_shadow_types(ap_type_str: str, subtype_str: str):
    shadow_types = ShadowTypes(ap_type_str, subtype_str)
    print(f'Steps:')
    for step in shadow_types.steps:
        print(f'- {step}')
    print()
    print(f'Shadow types for {shadow_types.description()}')
    for shadow_type in shadow_types.shadow_types:
        print(f'- {shadow_type}')

def run_interactive():
    ap_type_str = input_ap_type()
    subtype_str = input_subtype()
    print_shadow_types(ap_type_str, subtype_str)
    print()

def run_with_args(ap_type_str: str, subtype_str: str):
    try:
        print_shadow_types(ap_type_str, subtype_str)
    except ValueError as e:
        sys.stderr.write(f'{e.args[0]}\n')
        exit(1)

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

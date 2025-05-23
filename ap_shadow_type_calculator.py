# Licensed under the Creative Commons BY license:
# https://creativecommons.org/licenses/by/4.0/

# To run the script in interactive mode:
#   python ap_shadow_type_calculator.py
# To run the script with arguments:
#   python ap_shadow_type_calculator.py [AP type] [subtype]

import argparse
import sys


def input_ap_type():
    while True:
        ap_type_str = input('Enter AP type (q to quit): ')
        if ap_type_str in {'q', 'Q'}:
            sys.exit(0)
        try:
            return parse_ap_type(ap_type_str)
        except ValueError as e:
            print(f'{e.args[0]}')


def input_subtype():
    while True:
        subtype_str = input('Enter AP subtype (q to quit): ')
        if subtype_str in {'q', 'Q'}:
            exit(0)
        try:
            return parse_subtype(subtype_str)
        except ValueError as e:
            print(f'{e.args[0]}')


def swap_positions(description, shadow_types, swapped, ap_type, pos1, pos2):
    if pos1 > pos2:
        pair = f'{pos2}-{pos1}'
    else:
        pair = f'{pos1}-{pos2}'
    if pair in swapped:
        print(f'Skip {description} - already swapped')
        return

    swapped.add(pair)

    ap_type[pos1 - 1], ap_type[pos2 - 1] = ap_type[pos2 - 1], ap_type[pos1 - 1]
    shadow_type = ''.join(ap_type)
    print(f'Swap {description}: {shadow_type}')
    shadow_types.append(shadow_type)


def swap_obscured_shadow_type(ap_type, shadow_types, swapped, subtype, pos):
    swap_pos = 0
    for other_pos, pos_subtype in subtype.items():
        if pos_subtype == pos:
            if swap_pos > 0:
                # multiple matches, do not swap
                print(f'Skip Obscured {pos} - multiple matches')
                return
            swap_pos = other_pos
    if swap_pos > 0:
        swap_positions(f'Obscured {pos}-{swap_pos}', shadow_types, swapped, ap_type, pos, swap_pos)
    else:
        print(f'Skip Obscured {pos} - no matches')


def swap_shadow_type(description, shadow_types, swapped, ap_type, subtype, pos1, pos2):
    if subtype[pos1] == pos2 or subtype[pos2] == pos1:
        swap_positions(description, shadow_types, swapped, ap_type, pos1, pos2)
    else:
        print(f'Skip {description}')

def print_shadow_types(ap_type, subtype):
    subtype_str = ''.join(map(str, subtype.values()))
    original_ap_type = ''.join(ap_type)
    shadow_types = [original_ap_type]
    swapped = set()
    print(f'Shadow types for {original_ap_type} {subtype_str}:')

    # Step 1 - Accentuated - Ignore

    # Step 2 - Obscured - Any aspect pointing at an obscured position (x-0) switches
    # with it, unless it has another aspect pointing at it
    for pos, pos_subtype in subtype.items():
        if pos_subtype == 0: # obscured
            swap_obscured_shadow_type(ap_type, shadow_types, swapped, subtype, pos)

    # Step 3 - Method - Switch aspects in this order: 2-3 or 3-2 > 1-4 or 4-1
    swap_shadow_type('Method 2-3', shadow_types, swapped, ap_type, subtype, 2, 3)
    swap_shadow_type('Method 1-4', shadow_types, swapped, ap_type, subtype, 1, 4)

    # Step 4 - Self - Switch aspects in this order: 1-2 or 2-1 > 3-4 or 4-3
    swap_shadow_type('Self 1-2', shadow_types, swapped, ap_type, subtype, 1, 2)
    swap_shadow_type('Self 3-4', shadow_types, swapped, ap_type, subtype, 3, 4)

    # Step 5 - Others - Switch aspects in this order: 1-3 or 3-1 > 2-4 or 4-2
    swap_shadow_type('Others 1-3', shadow_types, swapped, ap_type, subtype, 1, 3)
    swap_shadow_type('Others 2-4', shadow_types, swapped, ap_type, subtype, 2, 4)

    print(f'Shadow types: {", ".join(shadow_types)}')


def parse_ap_type(ap_type_str):
    ap_type_str = ap_type_str.upper()
    if len(ap_type_str) == 4 and sorted(ap_type_str) == ['E', 'F', 'L', 'V']:
        return list(ap_type_str)
    else:
        raise ValueError(f'Invalid AP type {ap_type_str}')


def parse_subtype(subtype_str):
    if len(subtype_str) == 4 and all(map(lambda c: '0' <= c <= '4', subtype_str)):
        return {i + 1: int(c) for i, c in enumerate(subtype_str)}
    else:
        raise ValueError(f'Invalid subtype {subtype_str}')


def run_interactive():
    ap_type = input_ap_type()
    subtype = input_subtype()
    print_shadow_types(ap_type, subtype)
    print()


def run_with_args(ap_type_str, subtype_str):
    try:
        ap_type = parse_ap_type(ap_type_str)
        subtype = parse_subtype(subtype_str)
        print_shadow_types(ap_type, subtype)
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



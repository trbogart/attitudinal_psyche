# Licensed under the Creative Commons BY license:
# https://creativecommons.org/licenses/by/4.0/

import argparse
import sys


def input_ap_type():
    while True:
        ap_type_str = input('Enter AP type (q to quit): ')
        if ap_type_str in {'q', 'Q'}:
            sys.exit(0)
        ap_type = validate_ap_type(ap_type_str)
        if ap_type:
            return ap_type
        else:
            print('Invalid AP type')


def input_subtype():
    while True:
        subtype_str = input('Enter AP subtype (q to quit): ')
        if subtype_str in {'q', 'Q'}:
            exit(0)
        subtype = validate_subtype(subtype_str)
        if subtype:
            return subtype
        else:
            print('Invalid subtype')


def print_shadow_types(ap_type, subtype):
    original_ap_type = ''.join(ap_type)
    subtype_str = ''.join(map(str, subtype.values()))
    shadow_types = get_shadow_types(ap_type, subtype)
    print(f'Shadow types for {original_ap_type} {subtype_str}:')
    for shadow_type in shadow_types:
        print(shadow_type)


def swap_positions(shadow_types, ap_type, pos1, pos2):
    ap_type[pos1 - 1], ap_type[pos2 - 1] = ap_type[pos2 - 1], ap_type[pos1 - 1]
    shadow_type = ''.join(ap_type)
    if shadow_type not in shadow_types:
        shadow_types.append(''.join(ap_type))


def swap_obscured_shadow_type(shadow_types, ap_type, subtype, pos):
    swap_pos = 0
    for other_pos, pos_subtype in subtype.items():
        if pos_subtype == pos:
            if swap_pos > 0:
                # multiple matches, do not swap
                return
            swap_pos = other_pos
    if swap_pos > 0:
        swap_positions(shadow_types, ap_type, pos, swap_pos)


def swap_shadow_type(shadow_types, ap_type, subtype, pos1, pos2):
    if subtype[pos1] == pos2 or subtype[pos2] == pos1:
        swap_positions(shadow_types, ap_type, pos1, pos2)


def get_shadow_types(ap_type, subtype):
    shadow_types = [''.join(ap_type)]

    # Step 1 - Accentuated - Ignore

    # Step 2 - Obscured - Any aspect pointing at an obscured position (x-0) switches
    # with it, unless it has another aspect pointing at it
    for pos, pos_subtype in subtype.items():
        if pos_subtype == 0: # obscured
            swap_obscured_shadow_type(shadow_types, ap_type, subtype, pos)

    # Step 3 - Method - Switch aspects in this order: 2-3 or 3-2 > 1-4 or 4-1
    swap_shadow_type(shadow_types, ap_type, subtype, 2, 3)
    swap_shadow_type(shadow_types, ap_type, subtype, 1, 4)

    # Step 4 - Self - Switch aspects in this order: 1-2 or 2-1 > 3-4 or 4-3
    swap_shadow_type(shadow_types, ap_type, subtype, 1, 2)
    swap_shadow_type(shadow_types, ap_type, subtype, 3, 4)

    # Step 5 - Others - Switch aspects in this order: 1-3 or 3-1 > 2-4 or 4-2
    swap_shadow_type(shadow_types, ap_type, subtype, 1, 3)
    swap_shadow_type(shadow_types, ap_type, subtype, 2, 4)

    return shadow_types


def validate_ap_type(type_str):
    type_str = type_str.upper()
    if len(type_str) == 4 and sorted(type_str) == ['E', 'F', 'L', 'V']:
        return list(type_str)
    else:
        return None


def validate_subtype(subtype_str):
    if len(subtype_str) == 4 and all(map(lambda c: '0' <= c <= '4', subtype_str)):
        return {i + 1: int(c) for i, c in enumerate(subtype_str)}
    else:
        return None


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # interactive mode, ask user for AP type and subtype, repeating until q is entered
        while True:
            ap_type = input_ap_type()
            subtype = input_subtype()
            print_shadow_types(ap_type, subtype)
            print()
    else:
        parser = argparse.ArgumentParser(
            'ap_shadow_type_calculator',
            'Calculate AP shadow types (no arguments to run interactively)',
        )
        parser.add_argument('ap_type')
        parser.add_argument('subtype')
        args = parser.parse_args()

        # at least 1 argument given, get missing argument, if any
        ap_type = validate_ap_type(args.ap_type)
        if not ap_type:
            sys.stderr.write(f'Invalid AP type: {args.ap_type}\n')
            exit(1)

        subtype = validate_subtype(args.subtype)
        if not subtype:
            sys.stderr.write(f'Invalid subtype: {args.subtype}\n')
            exit(1)

        print_shadow_types(ap_type, subtype)

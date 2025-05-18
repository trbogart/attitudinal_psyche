import argparse
from shadow_types import get_shadow_types
import sys

def input_ap_type():
    while True:
        ap_type_str = input('Enter AP type (q to quit): ')
        if ap_type_str in ['q', 'Q']:
            sys.exit(0)
        ap_type = validate_and_parse_ap_type(ap_type_str)
        if ap_type:
            return ap_type
        else:
            print('Invalid subtype')

def validate_and_parse_ap_type(type_str):
    type_str = type_str.upper()
    if len(type_str) == 4 and sorted(type_str) == ['E', 'F', 'L', 'V']:
        return list(type_str)
    else:
        return None

def input_subtype():
    while True:
        subtype_str = input('Enter AP subtype (q to quit): ')
        if subtype_str in ['q', 'Q']:
            exit(0)
        subtype = validate_and_parse_subtype(subtype_str)
        if subtype:
            return subtype
        else:
            print('Invalid subtype')

def validate_and_parse_subtype(subtype_str):
    if len(subtype_str) == 4 and all(map(lambda c: '0' <= c <= '4', subtype_str)):
        return {i + 1: int(c) for i, c in enumerate(subtype_str)}
    else:
        return None

def print_shadow_types(ap_type, subtype):
    original_ap_type = ''.join(ap_type)
    subtype_str = ''.join(map(str, subtype.values()))
    shadow_types = get_shadow_types(ap_type, subtype)
    print(f'Shadow types for {original_ap_type} {subtype_str}:')
    for shadow_type in shadow_types:
        print(shadow_type)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # interactive mode
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
        ap_type = validate_and_parse_ap_type(args.ap_type)
        if not ap_type:
            sys.stderr.write(f'Invalid AP type: {args.ap_type}\n')
            exit(1)

        subtype = validate_and_parse_subtype(args.subtype)
        if not subtype:
            sys.stderr.write(f'Invalid subtype: {args.subtype}\n')
            exit(1)

        print_shadow_types(ap_type, subtype)

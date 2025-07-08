import argparse
import sys
from ap_shadow_type_calculator import validate_ap_type, input_ap_type

mapping_dict = {
    '4321': 'Dual: {0} <—> {1} (shared sexta)',
    '1234': 'Identical: {0} <—> {1} (shared sexta)',
    '4231': 'Solution: {0} <—> {1} (shared sexta)',
    '1324': 'Sister: {0} <—> {1} (shared sexta)',
    '4123': 'Radiance: {0} <—> {1} (square)',
    '2341': 'Radiance: {1} <—> {0} (square)',
    '4312': 'Instruction: {1} —> {0} (square)',
    '3421': 'Instruction: {0} —> {1} (square)',
    '1342': 'Invention: {1} —> {0} (triangular)',
    '1423': 'Invention: {0} —> {1} (triangular)',
    '4213': 'Assistance: {1} —> {0} (triangular)',
    '3241': 'Assistance: {0} —> {1} (triangular)',
    '4132': 'Enhancement: {1} —> {0} (triangular)',
    '2431': 'Enhancement: {0} —> {1} (triangular)',
    '2314': 'Regulation: {1} —> {0} (triangular)',
    '3124': 'Regulation: {0} —> {1} (triangular)',
    '2134': 'Near-Identical: {0} <—> {1} (linear)',
    '1243': 'Cousin: {0} <—> {1} (linear)',
    '1432': 'Customary: {0} <—> {1} (linear)',
    '3214': 'Specificity: {0} <—> {1} (linear)',
    '2143': 'Faux-Identical: {0} <—> {1} (opposed sexta)',
    '2413': 'Suffocation: {0} <—> {1} (opposed sexta, square)',
    '3142': 'Suffocation: {0} <—> {1} (opposed sexta, square)',
    '3412': 'Conflict: {0} <—> {1} (opposed sexta)',
}

def get_mapping(ap_type1_str: str, ap_type2_str: str) -> str:
    return ''.join([str(1+ap_type1_str.find(c)) for c in ap_type2_str])

def get_intertype(ap_type1_str: str, ap_type2_str: str) -> str:
    validate_ap_type(ap_type1_str)
    validate_ap_type(ap_type2_str)
    mapping = get_mapping(ap_type1_str, ap_type2_str)
    return mapping_dict[mapping].format(ap_type1_str, ap_type2_str)

def run_interactive() -> None:
    ap_type1_str = input_ap_type('Enter AP type 1 (q to quit): ')
    ap_type2_str = input_ap_type('Enter AP type 2 (q to quit): ')
    print(get_intertype(ap_type1_str, ap_type2_str))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # interactive mode, ask user for AP type and subtype, repeating until q is entered
        while True:
            run_interactive()
    else:
        parser = argparse.ArgumentParser(
            prog = 'ap_shadow_type_calculator',
            usage = 'Calculate AP shadow types (no arguments to run interactively)',
            add_help = True, # add -h/--help option
        )
        parser.add_argument('ap_type1', help = 'AP type 1 (any permutation of FLEV)')
        parser.add_argument('ap_type1', help = 'AP type 2 (any permutation of FLEV)')
        parser.add_argument('-v', '--verbose', action='store_true', help = 'print verbose messages')
        args = parser.parse_args()
        print(get_intertype(args.ap_type1.upper().strip(), args.ap_type2.upper().strip()))

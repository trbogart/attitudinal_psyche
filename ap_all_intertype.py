import argparse
from ap_shadow_type_calculator import validate_ap_type

def modify(ap_type_str: str, map_str: str) -> str:
    ap_type = list(ap_type_str)
    return ''.join([ap_type[int(i)-1] for i in map_str])

def get_all_intertypes(ap_type_str: str) -> dict[str, str]:
    validate_ap_type(ap_type_str)
    results = {}
    results['Dual'] = f'{ap_type_str} <—> {modify(ap_type_str, "4321")} (shared sexta)'
    results['Identical'] = f'{ap_type_str} <—> {ap_type_str} (shared sexta)'
    results['Solution'] = f'{ap_type_str} <—> {modify(ap_type_str, "4231")} (shared sexta)'
    results['Sister'] = f'{ap_type_str} <—> {modify(ap_type_str, "1324")} (shared sexta)'
    radiance_1 = modify(ap_type_str, '4123')
    radiance_2 = modify(ap_type_str, '2341')
    results['Radiance'] = f'{radiance_1} <—> {ap_type_str} <—> {radiance_2} (square)'
    instruction_1 = modify(ap_type_str, '4312')
    instruction_2 = modify(ap_type_str, '3421')
    results['Instruction'] = f'{instruction_1} —> {ap_type_str} —> {instruction_2} (square)'
    invention_1 = modify(ap_type_str, '1342')
    invention_2 = modify(ap_type_str, '1423')
    results['Invention'] = f'{invention_1} —> {ap_type_str} —> {invention_2} (triangular)'
    assistance_1 = modify(ap_type_str, '4213')
    assistance_2 = modify(ap_type_str, '3241')
    results['Assistance'] = f'{assistance_1} —> {ap_type_str} —> {assistance_2} (triangular)'
    enhancement_1 = modify(ap_type_str, '4132')
    enhancement_2 = modify(ap_type_str, '2431')
    results['Enhancement'] = f'{enhancement_1} —> {ap_type_str} —> {enhancement_2} (triangular)'
    regulation_1 = modify(ap_type_str, '2314')
    regulation_2 = modify(ap_type_str, '3124')
    results['Regulation'] = f'{regulation_1} —> {ap_type_str} —> {regulation_2} (triangular)'
    results['Near-Identical'] = f'{ap_type_str} <—> {modify(ap_type_str, "2134")} (linear)'
    results['Cousin'] = f'{ap_type_str} <—> {modify(ap_type_str, "1243")} (linear)'
    results['Customary'] = f'{ap_type_str} <—> {modify(ap_type_str, "1432")} (linear)'
    results['Specificity'] = f'{ap_type_str} <—> {modify(ap_type_str, "3214")} (linear)'
    results['Faux-Identical'] = f'{ap_type_str} <—> {modify(ap_type_str, "2143")} (opposed sexta)'
    suffocation_1 = modify(ap_type_str, '2413')
    suffocation_2 = modify(ap_type_str, '3142')
    results['Suffocation'] = f'{suffocation_1} <—> {ap_type_str} <—> {suffocation_2} (opposed sexta, square)'
    results['Conflict'] = f'{ap_type_str} <—> {modify(ap_type_str, "3412")} (opposed sexta)'
    return results

def get_all_intertypes_str(ap_type_str: str) -> str:
    relations = []
    for relation, ap_type in get_all_intertypes(ap_type_str).items():
        tag = f'{relation}:'
        relations.append(f'{tag:15s} {ap_type}')
    return '\n'.join(relations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = 'ap_intertype_calculator',
        usage = 'List AP intertype relations of given AP type',
        add_help = True, # add -h/--help option
    )
    parser.add_argument('ap_type', nargs='?', help = 'AP type (any permutation of FLEV)')
    args = parser.parse_args()
    if args.ap_type is None:
        ap_type_str = input('Enter AP type: ')
    else:
        ap_type_str = args.ap_type
    print(get_all_intertypes_str(ap_type_str.upper().strip()))
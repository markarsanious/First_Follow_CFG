import argparse


def parse_input(file):
    input_rules_dict = dict()
    with open(file, "r") as file:
        lines = file.readlines()
        lines = [[element.strip() for element in line.replace("\n","").split(":")] for line in lines]
        for line in lines:
            rule_to = [element.strip() for element in line[1].split("|")]
            input_rules_dict[line[0]] = rule_to
    return input_rules_dict


def print_output_to_file(input_rules_map, output_file):
    for rule in input_rules_map:
        output_file.write(rule + " : " + ' '.join(input_rules_map[rule][0]) + " : " + ' '.join(input_rules_map[rule][1]) + "\n")


def first_of(variable, input_rules_map):
    first = []
    if variable.isupper():
        rules = input_rules_map[variable]
        for rule in rules:
            counter = 0
            rule_array = rule.split(' ')

            #CASE 1: if the rule goes to a terminal which is not epsilon, add it to first array
            if (rule_array[0].islower() or not rule_array[0].isalpha()) and not (rule == 'epsilon'):
                first.append(rule_array[0])

            #CASE 2: if the rule goes to epsilon, add it to first array
            if rule == 'epsilon':
                first.append('epsilon')

            #CASE 3: if the rule goes to a variable
            if rule_array[0].isupper():

                #if this variable is the same as you and it goes to epsilon, skip it until you find another variable
                while rule_array[counter] == variable and counter<len(rule_array)-1:
                    if 'epsilon' in rules:
                        counter+=1
                    else:
                        break;
                first += first_of(rule_array[counter], input_rules_map)

                #as long as epsilon exist in the first so far, include the first of the following variables
                while ('epsilon' in first) and (counter < len(rule_array)-1):
                    counter+=1
                    first.remove('epsilon')
                    if not (rule_array[counter] == variable):
                        first += first_of(rule_array[counter], input_rules_map)

    return first

def follow_of(variable, start_variable, input_rules_map):
    follow = []
    if variable.isupper():
        # CASE 1: if it is the start variable add $ to the follow
        if variable == start_variable:
            follow.append('$')

        for row in input_rules_map:
            rules = input_rules_map[row]
            for rule in rules:
                counter = 0
                if variable in rule:
                    rule_array = rule.split(' ')
                    index = rule_array.index(variable)
                    #CASE 2: if the variable we are getting its follow is found and followed by other symbols
                    if index < len(rule_array)+counter-1:
                        followed_symbol = rule_array[index+1+counter]
                        counter+=1

                        #CASE 2 A: if followed by a terminal, add it to follow array
                        if (followed_symbol[0].islower() or not followed_symbol[0].isalpha()) and followed_symbol not in follow:
                            follow.append(followed_symbol)

                        #CASE 2 B: if followed by a variable, add the first of next variable to your follow array
                        if followed_symbol[0].isupper():
                            first_of_next = first_of(followed_symbol, input_rules_map)
                            while ('epsilon' in first_of_next) and (index+1+counter<len(rule_array)):
                                first_of_next.remove('epsilon')
                                follow += first_of_next
                                followed_symbol = rule_array[index + 1 + counter]
                                if followed_symbol[0].islower() or not followed_symbol[0].isalpha() and followed_symbol not in follow:
                                    follow.append(followed_symbol)
                                if followed_symbol[0].isupper():
                                    first_of_next = first_of(followed_symbol, input_rules_map)

                                counter+=1
                            #if first of next contains epsilon, add $ to your follow array
                            if 'epsilon' in first_of_next:
                                first_of_next.remove('epsilon')
                                first_of_next.append('$')
                            follow += first_of_next

                        #CASE 2 C: if followed by a variable that goes to epsilon,
                        #add follow of the current row symbol to your follow array
                        if 'epsilon' in first_of(followed_symbol, input_rules_map) and not (row == variable):
                            follow += follow_of(row, start_variable, input_rules_map)

                    #CASE 3: if the variable we are computing its follow is the last symbol in the rule (same as CASE 2 C)
                    if index == len(rule_array) -1 and not (row == variable):
                        follow += follow_of(row, start_variable, input_rules_map)

    return follow



def first_follow(input_rules_map):
    output_rules_map = dict()
    start_variable = list(input_rules_map.keys())[0]
    #compute first
    for rule in input_rules_map:
        first = first_of(rule, input_rules_map)
        first = sorted(set(first))
        output_rules_map[rule] = [first]
    #compute follow
    for rule_index, rule in enumerate(input_rules_map):
        follow = follow_of(rule, start_variable, input_rules_map)
        follow = sorted(set(follow))
        output_rules_map[rule].append(follow)
    return output_rules_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")
    args = parser.parse_args()
    output_file = open("task_5_1_result.txt", "w+")

    input_rules_map = parse_input(args.file)

    output_rules_map = first_follow(input_rules_map)
    print_output_to_file(output_rules_map, output_file)
#!/usr/bin/env python3
import random
from termcolor import colored, COLORS
import argparse

def colorize(line, block_colors, color_names):
    block_type = line.split(':')[1]
    if block_type not in block_colors:
        color = random.choice(color_names)
        block_colors[block_type] = color
        color_names.remove(color)
    return ('\033[1m' + colored(line, block_colors[block_type]) + '\033[0m')

def process_ical(args, color_names, block_colors):
    block = '\n' if args.block else ''
    begins = []
    output = []

    for line in args.ical_file:
        colored_line = ''

        if line.startswith("BEGIN"):
            modified_line = colorize(line.rstrip(), block_colors, color_names) if args.save is None else line.rstrip()
            colored_line = block + ' ' * int(args.indent) * len(begins) + modified_line
            begins.append(line.split(':')[1])
        elif line.startswith("END"):
            end_type = line.split(':')[1]
            modified_line = colorize(line.rstrip(), block_colors, color_names) if args.save is None else line.rstrip()
            colored_line = ' ' * int(args.indent) * (len(begins) - 1) + modified_line + block
            if end_type not in begins:
                raise ValueError(f"Unmatched BEGIN found for {end_type}")
            begins.remove(end_type)
        else:
            colored_line = ' ' * int(args.indent) * len(begins) + line.rstrip()

        output.append(colored_line)

    if args.save:
        with open(args.save, 'w') as file:
            file.write('\n'.join(output))
        print("Saved to file: " + args.save)
    else:
        print('\n'.join(output))

def get_args():
    parser = argparse.ArgumentParser(description="Pretty print ical files")
    parser.add_argument('ical_file', type=argparse.FileType('r'), help="Path to the iCalendar file")
    parser.add_argument('-s', '--save', type=str, help="Path to save the output file", default=None)
    parser.add_argument('-i', '--indent', type=str, help="Number of indents for each block", default=2)
    parser.add_argument('-b', '--block', action='store_true' ,help="Add a space between each property block")

    return parser.parse_args()

def main():
    block_colors = {}

    args = get_args()

    # Ensure the save path ends with .ics
    if args.save and not args.save.endswith('.ics'):
        args.save += '.ics'

    color_names = list(COLORS.keys())
    process_ical(args, color_names, block_colors)

if __name__ == "__main__":
    main()


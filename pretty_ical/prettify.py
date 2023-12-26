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

def process_ical(file, color_names, block_colors, save_path=None, indent=2):
    begins = []
    output = []

    for line in file:
        colored_line = ''

        if line.startswith("BEGIN"):
            modified_line = colorize(line.strip(), block_colors, color_names) if save_path is None else line.strip()
            colored_line = ' ' * int(indent) * len(begins) + modified_line
            begins.append(line.split(':')[1])
        elif line.startswith("END"):
            end_type = line.split(':')[1]
            modified_line = colorize(line.strip(), block_colors, color_names) if save_path is None else line.strip()
            colored_line = ' ' * int(indent) * (len(begins) - 1) + modified_line
            if end_type not in begins:
                raise ValueError(f"Unmatched BEGIN found for {end_type}")
            begins.remove(end_type)
        else:
            colored_line = ' ' * int(indent) * len(begins) + line.strip()

        output.append(colored_line)

    if save_path:
        with open(save_path, 'w') as file:
            file.write('\n'.join(output))
        print("Saved to file: " + save_path)
    else:
        print('\n'.join(output))

def get_args():
    parser = argparse.ArgumentParser(description="Pretty print ical files")
    parser.add_argument('ical_file', type=argparse.FileType('r'), help="Path to the iCalendar file")
    parser.add_argument('-s', '--save', type=str, help="Path to save the output file", default=None)
    parser.add_argument('-i', '--indent', type=str, help="Path to save the output file", default=2)

    return parser.parse_args()

def main():
    block_colors = {}

    args = get_args()

    # Ensure the save path ends with .ics
    if args.save and not args.save.endswith('.ics'):
        args.save += '.ics'

    color_names = list(COLORS.keys())
    process_ical(args.ical_file, color_names, block_colors, args.save, args.indent)

if __name__ == "__main__":
    main()


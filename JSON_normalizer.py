"""
This script normalizes the json files in the current directory
by making the offset equal to 4 intervals (1 indent) for each nested level.
"""

import json
import glob
import os.path


def main():
    files = glob.glob('./*.json')
    for file in files:
        with open(file, encoding='utf-8') as f:
            data = json.load(f)

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()


"""Assemble the manuscript: number [@key] citations in order of first appearance (Vancouver),
append the reference list, tables and figure legends.

python paper/build.py            -> paper/manuscript.md (+ .docx and .pdf if pandoc is present)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANG = sys.argv[1] if len(sys.argv) > 1 else 'en'


def read(name):
    with open(os.path.join(HERE, name)) as fh:
        return fh.read().strip() + '\n'


def section(text, drop_first_heading=False):
    if drop_first_heading:
        text = re.sub(r'\A# [^\n]*\n', '', text)
    return text


def refs():
    out = {}
    for line in open(os.path.join(HERE, 'references_verified.md')):
        m = re.match(r'- \[(\w+)\] (.*)', line.strip())
        if m:
            out[m.group(1)] = m.group(2)
    return out


def number(text, R):
    order = []

    def rep(mo):
        keys = [k.strip().lstrip('@') for k in mo.group(1).split(';')]
        nums = []
        for k in keys:
            if k not in R:
                raise KeyError(f'unknown reference key {k}')
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        nums = sorted(set(nums))
        parts, i = [], 0
        while i < len(nums):          # compress runs: 3,4,5 -> 3–5
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            parts.append(f'{nums[i]}–{nums[j]}' if j - i >= 2 else ','.join(map(str, nums[i:j + 1])))
            i = j + 1
        return '^' + ','.join(parts) + '^'

    text = re.sub(r'\[(@[^\]]+)\]', rep, text)
    return text, order


def main():
    R = refs()
    sfx = '' if LANG == 'en' else '_ru'
    body = [read(f'front{sfx}.md'),
            '# Introduction\n', section(read(f'intro{sfx}.md'), True),
            '# Methods\n', section(read(f'methods{sfx}.md'), True),
            '# Results\n', section(read(f'results_descriptive{sfx}.md'), True),
            read(f'results_outcome{sfx}.md'),
            '# Discussion\n', section(read(f'discussion{sfx}.md'), True),
            section(read(f'discussion_draft{sfx}.md'), True),
            read(f'back{sfx}.md')]
    text = '\n'.join(body)
    text, order = number(text, R)
    head = '# References\n' if LANG == 'en' else '# Литература\n'
    text += '\n' + head + '\n' + '\n'.join(f'{i}. {R[k]}' for i, k in enumerate(order, 1)) + '\n'
    text += '\n' + read(f'tables{sfx}.md')
    out = os.path.join(HERE, f'manuscript{sfx}.md')
    with open(out, 'w') as fh:
        fh.write(text)
    words = len(re.sub(r'\n# References.*', '', text, flags=re.S).split())
    print(out, f'{len(order)} references, ~{words} words incl. abstract/declarations')


if __name__ == '__main__':
    main()

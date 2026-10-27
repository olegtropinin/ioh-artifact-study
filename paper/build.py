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
BRACKETS = os.environ.get('CITE', 'brackets') == 'brackets'
SUPCAPS = {
    'en': ['Figure S1. Flow of patients.', 'Figure S2. Specification curve of 420 pipeline specifications.',
           'Figure S3. Probability that a recorded episode is waveform-flagged, by final duration and nadir.',
           'Figure S4. Ratio of odds ratios by filter, exposure metric and threshold (post hoc display).'],
    'ru': ['Рисунок S1. Отбор пациентов.', 'Рисунок S2. Кривая спецификаций: 420 вариантов обработки.',
           'Рисунок S3. Вероятность того, что эпизод помечен как артефакт, по длительности и минимуму.',
           'Рисунок S4. Отношение отношений шансов по фильтру, метрике и порогу (апостериорно).'],
}
CAPTIONS = {
    'en': ['Recorded hypotension that is waveform-flagged artefact: waveform and monitor MAP.',
           'Arterial artefact around non-invasive cuff measurements, by artefact type.',
           'Spurious minutes among recorded minutes with MAP < 65 mmHg, by filter and resolution.',
           'Ratio of odds ratios for AKI for every filter × resolution combination.'],
    'ru': ['Записанная гипотония, помеченная по кривой как артефакт: кривая и САД монитора.',
           'Артефакты артериальной кривой вокруг измерений манжетой, по типам артефакта.',
           'Ложные минуты среди записанных минут с САД < 65 мм рт. ст. по фильтрам и разрешению.',
           'Отношение отношений шансов ОПП для каждой комбинации фильтра и разрешения.'],
}


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
        return '[' + ', '.join(parts) + ']' if BRACKETS else '^' + ','.join(parts) + '^'

    if BRACKETS:   # journal style: number in square brackets, before the punctuation mark
        text = re.sub(r'([.,;:])\[(@[^\]]+)\]', r' [\2]\1', text)
        text = re.sub(r'(?<=\w)\[(@[^\]]+)\]', r' [\1]', text)
    text = re.sub(r'\[(@[^\]]+)\]', rep, text)
    return text, order


def main():
    R = refs()
    sfx = '' if LANG == 'en' else '_ru'
    body = [read(f'front{sfx}.md'), read(f'intro{sfx}.md'), read(f'methods{sfx}.md'),
            read(f'results{sfx}.md'), read(f'discussion{sfx}.md'), read(f'back{sfx}.md')]
    text = '\n'.join(body)
    text = re.sub(r'(?m)^(?!\s*[-*] |\s*\d+\. |\s*$|\s*\|)(.+)\n(\s*(?:- |\d+\. ))', r'\1\n\n\2', text)
    text, order = number(text, R)
    head = '# References\n' if LANG == 'en' else '# Литература\n'
    text += '\n' + head + '\n' + '\n'.join(f'{i}. {R[k]}' for i, k in enumerate(order, 1)) + '\n'
    text += '\n' + read(f'tables{sfx}.md')
    caps = CAPTIONS[LANG]
    figs = ['fig1_examples', 'fig5_nibp_cuff', 'fig2_spurious', 'fig6_forest']
    text += '\n# ' + ('Figures' if LANG == 'en' else 'Рисунки') + '\n\n'
    text += '\n\n'.join(f'![{c}](figures/{f}{sfx}.png){{width=100%}}' for f, c in zip(figs, caps)) + '\n'
    # supplement: methods, tables, figures, protocol (citations numbered with the main list)
    # captions already carry "Figure S<n>", so the LaTeX "Figure <n>:" label is suppressed,
    # and the wide supplementary tables are set in a smaller font
    sup = ('---\nheader-includes: |\n  \\usepackage{caption}\n  \\captionsetup[figure]{labelformat=empty}\n'
           '  \\usepackage{etoolbox}\n  \\AtBeginEnvironment{longtable}{\\small\\setlength{\\tabcolsep}{3pt}}\n---\n\n'
           + read(f'supp_methods{sfx}.md') + '\n' + read(f'supplement_tables{sfx}.md'))
    sup += '\n# ' + ('Supplementary figures' if LANG == 'en' else 'Дополнительные рисунки') + '\n\n'
    for f, cap in zip(['figS1_flow', 'fig3_spec_curve', 'fig4_episode_probability', 'fig3_depth_heatmap'],
                      SUPCAPS[LANG]):
        sup += f'![{cap}](figures/{f}{sfx}.png){{width=90%}}\n\n'
    proto = open(os.path.join(HERE, '..', 'docs', f'protocol{sfx}.md')).read()
    sup += '\n# ' + ('Supplementary Protocol' if LANG == 'en' else 'Дополнительный протокол') + '\n\n' + \
        re.sub(r'(?m)^#', '##', proto)
    sup = sup.replace('→', '->').replace('∈', ' in ')
    with open(os.path.join(HERE, f'supplement{sfx}.md'), 'w') as fh:
        fh.write(sup)
    out = os.path.join(HERE, f'manuscript{sfx}.md')
    with open(out, 'w') as fh:
        fh.write(text)
    words = len(re.sub(r'\n# References.*', '', text, flags=re.S).split())
    print(out, f'{len(order)} references, ~{words} words incl. abstract/declarations')


if __name__ == '__main__':
    main()

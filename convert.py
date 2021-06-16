from sys import argv
import re
from bs4 import BeautifulSoup

with open(argv[1]) as f:
    html = BeautifulSoup(f.read(), features='lxml')

special_ps = html.select('p.zenoPC')
title = special_ps[0].text
setting = special_ps[1].text

transforms = [(r'\.\.\.', r'\\ldots{}'),
              (r'<i>(.+)</i>', r'\\direction{\1}'),
              ('\u8211|–', '---'),
              (r'<a.*>.*</a>', '')]

characters = {'DIRNE': r'\dirne',
              'SOLDAT': r'\soldat',
              'STUBENMÄDCHEN': r'\maedchen',
              'DAS STUBENMÄDCHEN': r'\maedchen',
              'DER JUNGE HERR': r'\herr',
              'DIE JUNGE FRAU': r'\frau',
              'DER GATTE': r'\gatte',
              'DAS SÜSSE MÄDEL': r'\suesse',
              'DER DICHTER': r'\dichter',
              'DICHTER': r'\dichter',
              'SCHAUSPIELERIN': r'\schauspielerin',
              'GRAF': r'\graf'}

characterlist = [r'\the'+v[1:] for k, v in characters.items()
                 if re.search(k, title, re.IGNORECASE)]

print(f"\\scene{{{title}}}")
print(f"\\characterlist{{{', '.join(characterlist)}}}")
print(f"\\setting{{{setting}}}")
print(r"\begin{play}")

ignored = []
for line in html.find_all('p'):
    parsed_line = re.match(r'<p>(?P<character>[A-ZÄÜÖ ]+)\.? ?(?P<line>.+)</p>',
                           str(line))
    if not parsed_line:
        parsed_line = re.match(r'<p class="zenoPC">(?P<line><i>.+</i>)</p>', str(line))
        if parsed_line:
            pass
        elif re.match('<p>(– ?)+</p>', str(line)):
            print('\t'+r'\hiat')
            print()
            continue
        else:
            ignored.append(str(line))
            continue
    parsed_line = parsed_line.groupdict()

    content = parsed_line['line']
    for pattern, repl in transforms:
        content = re.sub(pattern, repl, content)

    if 'character' in parsed_line and parsed_line['character']:
        try:
            print('\t'+characters[parsed_line['character'].strip()])
        except KeyError:
            print("% TODO")
            print(parsed_line['character'])
    print('\t'+content)
    print()

print(r"\end{play}")


print("\n% TODO")
print(''.join('% '+l+'\n' for l in ignored))

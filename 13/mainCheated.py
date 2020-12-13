with open("input.txt") as f:
    lines = list(f)

ids = list(lines[1].rstrip().split(','))
print('https://www.wolframalpha.com/input/?i=0+%3D+' + '+%3D+'.join(
    ['((n+%2B+{})+mod+{})'.format(i, n) for i, n in enumerate(ids) if n != 'x']))

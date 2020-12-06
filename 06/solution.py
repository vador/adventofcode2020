with open(r'input.txt') as file:
    lines = file.read().strip().split("\n\n")
print(lines)
groups = [set(line.replace("\n", "")) for line in lines]
print(sum([len(answers) for answers in groups]))

counter = 0
for line in lines:
    answers = line.split("\n")
    first = set(answers[0])

    for ans in answers[1:]:
        first = first.intersection(ans)
    counter += len(first)

print(counter)

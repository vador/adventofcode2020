import logging
import re

from loadValues import LoadValues


def parse_container(str_bag):
    res = re.match(r"^([a-z]*) ([a-z]*) bags", str_bag)
    tint = res.groups()[0]
    color = res.groups()[1]
    logging.debug((tint, color))
    return (tint, color)


def parse_contains(str_bag):
    parsed = []
    if str_bag == "no other bags":
        return parsed
    # coords = [tuple(map(int, list(re.findall(r'-?\d+', ln)))) for ln in raw]
    res = re.findall((r"(\d+) ([a-z]+) ([a-z]+) bag"), str_bag)
    parsed = [((tint, color), nb) for (nb, tint, color) in res]
    logging.debug("Contains : " + str(parsed))
    return parsed


def parse_bag_desc(line):
    cont_def = re.match(r"^(.*) contain (.*)$", line)
    logging.debug(line)
    container = cont_def.groups()[0]
    contains = cont_def.groups()[1]
    logging.debug((container, contains))
    container = parse_container(container)
    contains = parse_contains(contains)
    return (container, contains)


def build_graph(lines):
    descendants = {}
    ascendants = {}
    for line in lines:
        (container, contains) = parse_bag_desc(line)
        if container in descendants:
            descendants[container].append(contains)
        else:
            descendants[container] = contains
        for (bag, nb) in contains:
            if bag in ascendants:
                ascendants[bag].append(container)
            else:
                ascendants[bag] = [container]
    return (ascendants, descendants)


def count_ascendants(bag, ascendants):
    cnt = []
    for asc in ascendants[bag]:
        cnt.append(asc)
        if asc in ascendants:
            cnt += count_ascendants(asc, ascendants)
    return cnt


def count_descendants(bag, descendants):
    cnt = 1
    for (des, nb) in descendants[bag]:
        cntdes = count_descendants(des, descendants)
        cnt += int(nb) * cntdes
        logging.debug("des:" + str((des, nb, cntdes)))
    if cnt == 0:
        cnt = 1
    return cnt


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started')
    lv = LoadValues("test.txt")
    lines = lv.strip_lines()
    graph = build_graph(lines)
    print(graph)
    cnt = count_ascendants(('shiny', 'gold'), graph[0])
    print("Star 1 : ", len(set(cnt)))
    cnt = count_descendants(('shiny', 'gold'), graph[1])
    print("Star 2 : ", cnt - 1)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

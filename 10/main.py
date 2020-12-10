import logging
import re
import cProfile

from loadValues import LoadValues

path_store = {}


def build_adapters_graph(adapters):
    graph = {}
    for (i, adapter) in enumerate(adapters[:-1]):
        graph[adapter] = [adapters[i + 1]]
    for (i, adapter) in enumerate(adapters[:-2]):
        if adapters[i + 2] - adapter <= 3:
            graph[adapter].append(adapters[i + 2])
    for (i, adapter) in enumerate(adapters[:-3]):
        if adapters[i + 3] - adapter <= 3:
            graph[adapter].append(adapters[i + 3])
    logging.debug(graph)
    return graph


def count_paths(start, end, graph):
    logging.debug((start, end))
    if (start, end) in path_store:
        return path_store[(start, end)]
    nb = 0
    nodes = graph[start]
    if end in nodes:
        return 1
    for next in nodes:
        nb += count_paths(next, end, graph)
    path_store[(start, end)] = nb
    return nb

def main():
    lv = LoadValues()
    numbers = lv.list_to_intlist()
    logging.debug(len(numbers))
    adapters = [0] + numbers + [max(numbers) + 3]
    logging.debug(adapters)

    adapters.sort()
    logging.debug(adapters)
    diff = [adapters[i + 1] - adapters[i] for i in range(len(adapters) - 1)]
    logging.debug(diff)

    one = sum([i == 1 for i in diff])
    three = sum([i == 3 for i in diff])
    logging.debug((one, three, one * three))
    print("Star 1 : ", one * three)

    graph = build_adapters_graph(adapters)
    number = count_paths(0, max(adapters), graph)
    print("Star 2 : ", number)

    logging.info('Finished')


##
if __name__ == '__main__':
    pr = cProfile.Profile()
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    pr.enable()
    main()
    pr.disable()
    logging.info('Finished')
    pr.print_stats()

import logging

from loadValues import LoadValues


def list_questions_for_group_union(group):
    result = set()
    for person in group:
        res_person = set(person)
        logging.debug(res_person)
        result = result.union(res_person)
    logging.debug("Result group:" + str(result))
    return len(result)


def list_questions_for_group_intersection(group):
    result = set(list("abcdefghijklmnopqrstuvwxyz"))
    for person in group:
        res_person = set(person)
        logging.debug(res_person)
        result = result.intersection(res_person)
    logging.debug("Result group:" + str(result))
    return len(result)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('Started')
    lv = LoadValues(groups=True)

    groups = [line for line in lv.raw_values]
    logging.debug(groups)
    res = [(list_questions_for_group_union(group)) for group in groups]
    cnt = sum(res)
    print("Star 1 : ", cnt)
    res = [(list_questions_for_group_intersection(group)) for group in groups]
    cnt = sum(res)
    print("Star 2 : ", cnt)

    logging.info('Finished')


##
if __name__ == '__main__':
    main()

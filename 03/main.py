from loadValues import LoadValues

lv = LoadValues().strip_lines()

height = len(lv)
width = len(lv[0])

print(height, width, lv)


def convertw(y):
    (div, mod) = divmod(y, width)
    return mod


def trees_for_slope(slopex, slopey):
    (posx, posy) = (0, 0)
    cnt = 0
    while (posx < height - 1):
        posx += slopex
        posy += slopey
        print(posx, posy, convertw(posy))
        if (lv[posx][convertw(posy)] == "#"):
            cnt += 1
    return (cnt)


cnt1 = trees_for_slope(1, 1)
cnt2 = trees_for_slope(1, 3)
cnt3 = trees_for_slope(1, 5)
cnt4 = trees_for_slope(1, 7)
cnt5 = trees_for_slope(2, 1)
print(cnt1, cnt2, cnt3, cnt4, cnt5)
print(cnt1 * cnt2 * cnt3 * cnt4 * cnt5)

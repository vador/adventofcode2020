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
        # print(posx, posy, convertw(posy))
        if (lv[posx][convertw(posy)] == "#"):
            cnt += 1
    return (cnt)


slope = trees_for_slope(1, 3)
print("1 star : ", slope)

slope1 = trees_for_slope(1, 1)
slope2 = trees_for_slope(1, 3)
slope3 = trees_for_slope(1, 5)
slope4 = trees_for_slope(1, 7)
slope5 = trees_for_slope(2, 1)
print(slope1, slope2, slope3, slope4, slope5)
print("2 stars : ", slope1 * slope2 * slope3 * slope4 * slope5)

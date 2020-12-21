from unittest import TestCase
from loadValues import LoadValues
from tile import Tile
from tile import TileList
from tile import Side


class TestTile(TestCase):
    tiles = None

    def setUp(self):
        lv = LoadValues("test.txt", groups=True)

        self.tiles = {}
        for tile in lv.raw_values:
            cur_tile = Tile(tile)
            self.tiles[cur_tile.tileId] = cur_tile

    def test_get_all_sides(self):
        t = self.tiles[2311]
        res = [Side(tile=2311, direction=0, flipped=False, side='..##.#..#.'),
               Side(tile=2311, direction=1, flipped=False, side='...#.##..#'),
               Side(tile=2311, direction=2, flipped=False, side='###..###..'),
               Side(tile=2311, direction=3, flipped=False, side='.#..#####.'),
               Side(tile=2311, direction=0, flipped=True, side='..###..###'),
               Side(tile=2311, direction=1, flipped=True, side='#..##.#...'),
               Side(tile=2311, direction=2, flipped=True, side='.#..#.##..'),
               Side(tile=2311, direction=3, flipped=True, side='.#####..#.')]

        self.assertEqual(res, t.get_all_sides())

    def test_get_side_no_flip_no_rotate(self):
        t = self.tiles[2311]
        my_sides = []
        for i in range(4):
            my_sides.append(t.get_side(i))
        res = [Side(tile=2311, direction=0, flipped=False, side='..##.#..#.'),
               Side(tile=2311, direction=1, flipped=False, side='...#.##..#'),
               Side(tile=2311, direction=2, flipped=False, side='###..###..'),
               Side(tile=2311, direction=3, flipped=False, side='.#..#####.')]

        self.assertEqual(res, my_sides)

    def test_get_side_rotate_one(self):
        t = self.tiles[2311]
        my_sides = []
        t.rotate(1)
        for i in range(4):
            my_sides.append(t.get_side(i))
        my_sides = sorted(my_sides)
        res = sorted([Side(tile=2311, direction=1, flipped=False, side='..##.#..#.'),
                      Side(tile=2311, direction=2, flipped=False, side='...#.##..#'),
                      Side(tile=2311, direction=3, flipped=False, side='###..###..'),
                      Side(tile=2311, direction=0, flipped=False, side='.#..#####.')])

        self.assertEqual(res, my_sides)

    def test_get_side_rotate(self):
        t = self.tiles[2311]
        my_sides = []
        t.rotate(1)
        my_sides.append(t.get_side(1))
        t.rotate(2)
        my_sides.append(t.get_side(3))
        t.rotate(3)
        my_sides.append(t.get_side(1))
        t.rotate(4)
        my_sides.append(t.get_side(3))
        t.rotate(0)

        print(my_sides)
        res = [Side(tile=2311, direction=1, flipped=False, side='..##.#..#.'),
               Side(tile=2311, direction=3, flipped=False, side='...#.##..#'),
               Side(tile=2311, direction=1, flipped=False, side='###..###..'),
               Side(tile=2311, direction=3, flipped=False, side='.#..#####.')]
        print(res)

        self.assertEqual(res, my_sides)

    def test_get_side_flip(self):
        t = self.tiles[2311]
        my_sides = []
        t.rotate(0)
        t.flip(True)
        my_sides.append(t.get_side(0))
        my_sides.append(t.get_side(1))
        my_sides.append(t.get_side(2))
        my_sides.append(t.get_side(3))
        t.rotate(0)
        t.flip(False)
        print(my_sides)

        res = [Side(tile=2311, direction=0, flipped=False, side='..###..###'),
               Side(tile=2311, direction=1, flipped=False, side='#..##.#...'),
               Side(tile=2311, direction=2, flipped=False, side='.#..#.##..'),
               Side(tile=2311, direction=3, flipped=False, side='.#####..#.')]
        self.assertEqual(res, my_sides)

    def test_get_side_flip_rotate_path(self):
        t = self.tiles[2311]
        my_sides = []
        print(t.get_all_sides())
        t.rotate(0)
        t.flip(True)
        my_sides.append(t.get_side(3))

        print(my_sides)

        res = [Side(tile=2311, direction=3, flipped=False, side='.#####..#.')]
        self.assertEqual(res, my_sides)
        t.rotate(0)
        t.flip(False)

    def test_get_side_flip_rotate(self):
        t = self.tiles[2311]
        my_sides = []
        t.rotate(0)
        t.flip(True)
        t.rotate(1)
        my_sides.append(t.get_side(1))
        my_sides.append(t.get_side(2))
        my_sides.append(t.get_side(3))
        my_sides.append(t.get_side(0))
        t.rotate(0)
        t.flip(False)
        print(my_sides)

        res = [Side(tile=2311, direction=1, flipped=False, side='..###..###'),
               Side(tile=2311, direction=2, flipped=False, side='#..##.#...'),
               Side(tile=2311, direction=3, flipped=False, side='.#..#.##..'),
               Side(tile=2311, direction=0, flipped=False, side='.#####..#.')]
        self.assertEqual(res, my_sides)

    def test_why(self):
        t1 = self.tiles[2729]
        t2 = self.tiles[2971]
        t3 = self.tiles[1951]
        t1.flip(True)
        t2.flip(True)
        t3.flip(True)
        t3.rotate(2)

        s1 = t1.get_side(2)
        s2 = t2.get_side(0)
        s3 = t3.get_side(2)
        print(s3)

        t1.flip(False)
        t2.flip(False)
        t3.flip(False)
        t3.rotate(0)


class TestTileList(TestCase):
    tl = None

    def setUp(self):
        lv = LoadValues("test.txt", groups=True)
        self.tl = TileList()
        for tile in lv.raw_values:
            T = Tile(tile)
            self.tl.add_tile(T)

    def test_find_neigh_in_direction(self):
        t = self.tl.tiles[3079]
        s = self.tl.find_neigh_in_direction(3079, 2)
        print(s)
        t2 = self.tl.tiles[2473]
        t2.flip(True)
        t2.rotate(3)
        print(t2.get_side(2))
        s2 = self.tl.find_neigh_in_direction(2473, 2)
        print(s2)

    def test_final_map(self):
        res = [".#.#..#.##...#.##..#####",
               "###....#.#....#..#......",
               "##.##.###.#.#..######...",
               "###.#####...#.#####.#..#",
               "##.#....#.##.####...#.##",
               "...########.#....#####.#",
               "....#..#...##..#.#.###..",
               ".####...#..#.....#......",
               "#..#.##..#..###.#.##....",
               "#.####..#.####.#.#.###..",
               "###.#.#...#.######.#..##",
               "#.####....##..########.#",
               "##..##.#...#...#.#.#.#..",
               "...#..#..#.#.##..###.###",
               ".#.#....#.##.#...###.##.",
               "###.#...#..#.##.######..",
               ".#.#.###.##.##.#..#.##..",
               ".####.###.#...###.#..#.#",
               "..#.#..#..#.#.#.####.###",
               "#..####...#.#.#.###.###.",
               "#####..#####...###....##",
               "#.##..#..#...#..####...#",
               ".#.###..##..##..####.##.",
               "...###...##...#...#..###"]

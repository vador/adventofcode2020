import logging


class SeaMap:
    map = None
    found = None
    MONSTER = ["                  # ",
               "#    ##    ##    ###",
               " #  #  #  #  #  #   "]

    def __init__(self, strMap):
        self.map = strMap.copy()

        self.found = []
        for line in strMap:
            self.found.append(list(line))

    def flip_text(self, text):
        return text[::-1]

    def rotate_text(self, text):
        return [''.join(elem) for elem in zip(*text[::-1])]

    def rotate_monster(self):
        all_m = []
        new_monster = self.MONSTER
        for i in range(4):
            all_m.append(new_monster)
            new_monster = self.rotate_text(new_monster)
        new_monster = self.flip_text(new_monster)
        for i in range(4):
            all_m.append(new_monster)
            new_monster = self.rotate_text(new_monster)
        return all_m

    def monster2offset(self, monster):
        monster_offset = []
        for (i, line) in enumerate(monster):
            for (j, char) in enumerate(line):
                if char == "#":
                    monster_offset.append((i, j))
        return monster_offset

    def find_monster_at_offset(self, offset, monster_offset):
        (i, j) = offset
        for (di, dj) in monster_offset:
            if self.map[i + di][j + dj] != '#':
                return False
        return True

    def find_monster_in_map(self, monster):
        found_pos = []
        monster_offset = self.monster2offset(monster)
        mh = len(monster)
        mw = len(monster[0])
        for i in range(len(self.map) - mh):
            for j in range(len(self.map[0]) - mw):
                if self.find_monster_at_offset((i, j), monster_offset):
                    found_pos.append((i, j))
                    self.update_found((i, j), monster_offset)
        return found_pos

    def update_found(self, offset, monster_offset):
        (i, j) = offset
        for (di, dj) in monster_offset:
            self.found[i + di][j + dj] = 'O'

    def roughness(self):
        cnt = 0
        for line in self.found:
            for char in line:
                if char == '#':
                    cnt += 1
        return cnt

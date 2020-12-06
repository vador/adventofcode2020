import cProfile
import logging
from queue import Queue

from loadValues import LoadValues

graph_logger = logging.getLogger('aoc.graph_logger')
graph_logger_graph = logging.getLogger('aoc.graph_logger.graph')
graph_logger_maze = logging.getLogger('aoc.graph_logger.maze')


class Graph:
    graph = None
    maze = None

    def __init__(self, maze):
        self.logger = logging.getLogger('aoc.graph_logger.graph')
        self.maze = maze
        if maze is not None:
            self.graph = maze.get_graph()

    def get_cell(self, pos):
        (r, c) = pos
        (rmin, cmin) = (0, 0)
        ((rmax, cmax)) = (self.maze.height, self.maze.width)
        if (rmin <= r < rmax) and (cmin <= c < cmax):
            return self.maze.maze[r][c]
        return None

    def bfs(self, pos):
        queue = Queue()
        distances = {}
        queue.put((pos, 0))
        distances[pos] = 0
        while not queue.empty():
            (cur_cell, cur_dist) = queue.get()
            self.logger.debug("BFS for cell :" + str((cur_cell, cur_dist)))
            cur_dist += 1
            for nb in self.graph[cur_cell]:
                if nb not in distances:
                    self.logger.debug("BFS adding :" + str((nb, cur_dist)))
                    distances[nb] = cur_dist
                    queue.put((nb, cur_dist))
        return distances


class Maze:
    maze = None
    width = None
    height = None
    wall_symbol = None

    def __str__(self):
        return str((self.height, self.width, self.wall_symbol)) + str(self.maze)

    def __init__(self):
        self.logger = logging.getLogger('aoc.graph_logger.maze')
        pass

    def build_maze(self, str_maze, wall_symbol='#'):
        self.maze = str_maze
        self.height = len(str_maze)
        self.width = max([len(row) for row in str_maze])
        self.wall_symbol = wall_symbol
        self.logger.debug(self)

    def get_neighbors(self, pos):
        neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighb_list = []
        (x, y) = pos
        (xmin, ymin) = (0, 0)
        ((xmax, ymax)) = (self.height, self.width)
        self.logger.debug("Neighbours for " + str(pos))
        for (dx, dy) in neighbours:
            if (xmin <= (x + dx) < xmax) and (ymin <= (y + dy) < ymax):
                self.logger.debug("Checking " + str(((x + dx), (y + dy))))

                if self.maze[x + dx][y + dy] != self.wall_symbol:
                    neighb_list.append((x + dx, y + dy))
        return neighb_list

    def get_graph(self):
        nodes = {}
        for (r, row) in enumerate(self.maze):
            for (c, cell) in enumerate(row):
                if cell != self.wall_symbol:
                    neighbors = self.get_neighbors((r, c))
                    nodes[(r, c)] = neighbors
        self.logger.debug(nodes)
        return nodes


def main():
    pr = cProfile.Profile()

    logging.basicConfig(level=logging.DEBUG)
    graph_logger_maze.setLevel(logging.INFO)
    logging.info('Started')
    pr.enable()

    lv = LoadValues()
    lv.strip_lines()
    my_maze = Maze()
    my_maze.build_maze(lv.processed_values)
    nodes = my_maze.get_graph()
    my_graph = Graph(my_maze)
    # print(my_graph.graph[(0,0)])
    # print(my_graph.get_cell((0,1)))
    print("_____________________")
    distances = my_graph.bfs((0, 0))
    dist_list = distances.items()
    print(sorted(dist_list, key=lambda dist: dist[1]))
    pr.disable()

    logging.info('Finished')
    pr.print_stats()

if __name__ == '__main__':
    logging.getLogger(__name__)

    main()

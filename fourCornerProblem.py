import itertools

class Problem:
    def __init__(self, mazeFile):
        self.xStep = 40
        self.yStep = 40
        self.readMaze(mazeFile)
        self.compute_distances() 

    def readMaze(self, mazeFile):
        self.walls = []
        self.pacman = 0
        self.food = []
        self.xMax = 0
        self.yMax = 0
        
        with open(mazeFile, 'r') as f:
            y = 0
            while True:
                s = list(f.readline())
                if s == []: break
                if s[-1] == '\n': s.pop()
                x = 0
                for k in s:
                    if k == '*': self.walls.append((x, y))
                    if k == 'P': self.pacman = (x, y)
                    if k == '.': self.food.append((x, y))
                    x += 1
                y += 1
                self.xMax = max(self.xMax, x)
            self.yMax = y
            
    def startState(self):
        return (self.pacman, self.food)

    def isGoal(self, node):
        return node[1] == []

    def transition(self, node):
        x, y = node[0]
        newState = []

        potential_moves = [((x+1, y), 'R'),
                           ((x-1, y), 'L'),
                           ((x, y+1), 'D'),
                           ((x, y-1), 'U')]

        moves = [(move, a) for move, a in potential_moves if 0 <= move[0] < self.xMax and
                 0 <= move[1] < self.yMax and move not in self.walls]
        
        for k, action in moves:
            remainingDots = node[1].copy()
            if k in remainingDots:
                remainingDots.remove(k)
            newState.append(((k, remainingDots), action, 1))

        return newState

    def compute_distances(self):
        self.dist = {}
        
        positions = [self.pacman] + self.food
        for pos1, pos2 in itertools.combinations(positions, 2):
            distance = self.BFS(pos1, pos2)
            self.dist[(pos1, pos2)] = distance
            self.dist[(pos2, pos1)] = distance  
    def BFS(self, start_pos, target_pos):
        def construct_path(node, visited):
            path = []
            while node:
                node, a = visited[node]
                if node != None: path = [a] + path
            return path

        def transition(node):
            x, y = node
            potential_moves = [((x+1, y), 'R'),
                               ((x-1, y), 'L'),
                               ((x, y+1), 'D'),
                               ((x, y-1), 'U')]

            moves = [(move, a) for move, a in potential_moves if 0 <= move[0] < self.xMax and
                     0 <= move[1] < self.yMax and move not in self.walls]
            return moves
        
        frontier = [(start_pos, None, None)]
        visited = {}
        while frontier:
            node, parent, action = frontier.pop(0)
            if node in visited: continue
            visited[node] = (parent, action)
            if node == target_pos: return len(construct_path(node, visited))
            neighbors = transition(node)
            for n, a in neighbors:
                frontier.append((n, node, a))
        return float('inf')

    def nextStates(self, node):
        neighbors = []
        for f in node[1]:
            plan_length = self.dist[(node[0], f)]
            dots = node[1].copy()
            dots.remove(f)
            neighbors.append((plan_length, (f, dots), plan_length))
        return neighbors 

    def h(self, state):
        pacman_pos = state[0]
        remaining_foods = state[1]

        if not remaining_foods:
            return 0

        mst = {food: False for food in remaining_foods}
        sumSteps = 0
        current_pos = pacman_pos

        while not all(mst.values()):
            min_distance = float('inf')
            closest_food = None
            for food in remaining_foods:
                if not mst[food]:
                    distance = self.dist.get((current_pos, food), float('inf'))
                    if distance < min_distance:
                        min_distance = distance
                        closest_food = food
            
            if closest_food:
                mst[closest_food] = True
                sumSteps += min_distance
                current_pos = closest_food

        return sumSteps

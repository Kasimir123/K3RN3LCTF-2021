#!/usr/local/bin/python
#
# Polymero
#

# PRIVATE FILE, NO SNOOPING !!!

# Local import
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

class Cell:
    def __init__(self, x, y, z, distance):
        self.x = x
        self.y = y
        self.z = z
        self.d = distance
        
    def __lt__(self, other):
        if (self.d == other.d):
            if (self.x != other.x):
                return (self.x < other.x)
            elif (self.y != other.y):
                return (self.y < other.y)
            else:
                return (self.z < other.z)
        return (self.d < other.d)

    def __eq__(self, other):
        return [self.x,self.y,self.z,self.d] == [other.x,other.y,other.z,other.d]

    def __hash__(self):
        return hash((self.x,self.y,self.z,self.d))

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.x, self.y, self.z, self.d)

    
    
class Private:
    def __init__(self):
        self.flag = FLAG
        
    def validify_zonemap(self, zonemap, verbose=False):
        Z,Y,X = len(zonemap), len(zonemap[0]), len(zonemap[0][0])
        ALP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # status, danger, bombs, empty
        space = [[[[' ', ALP.index(zonemap[k][j][i]), 0, 0] for i in range(X)] for j in range(Y)] for k in range(Z)]
        def surround_fill(space, loc, fill, skip='.#'):
            x, y, z = loc
            for zz in [z-1, z, z+1]:
                for yy in [y-1, y, y+1]:
                    for xx in [x-1, x, x+1]:
                        if zz in range(Z) and yy in range(Y) and xx in range(X):
                            if [xx,yy,zz] != [x,y,z]:
                                if space[zz][yy][xx][0] not in skip:
                                    space[zz][yy][xx][0] = fill
        def update(space):
            for z in range(Z):
                for y in range(Y):
                    for x in range(X):
                        ret = []
                        for k in [z-1, z, z+1]:
                            for j in [y-1, y, y+1]:
                                for i in [x-1, x, x+1]:
                                    if k in range(Z) and j in range(Y) and i in range(X):
                                        if [i,j,k] != [x,y,z]:
                                            ret += [space[k][j][i][0]]
                        space[z][y][x][2] = sum([1 if i == '#' else 0 for i in ret])
                        space[z][y][x][3] = sum([1 if i == ' ' else 0 for i in ret])
        def sweep_mines(space, limit=None):
            update(space)
            left = sum(1 for l in [m[0] for n in [i for j in space for i in j] for m in n] if l == ' ')
            rnd = 1
            while left:
                if verbose: print('On round {}, spaces left {}   '.format(rnd, left), end='\r', flush=True)
                for k in range(Z):
                    for j in range(Y):
                        for i in range(X):
                            if space[k][j][i][3] > 0:
                                if space[k][j][i][1] == space[k][j][i][2]:
                                    surround_fill(space, (i,j,k), '.')
                                if space[k][j][i][1] - space[k][j][i][2] == space[k][j][i][3]:
                                    surround_fill(space, (i,j,k), '#')
                update(space)
                new_left = sum(1 for l in [m[0] for n in [i for j in space for i in j] for m in n] if l == ' ')
                if new_left == left:
                    if verbose: print('Loop detected at {} left...'.format(left)+' '*32)
                    return False
                left = new_left
                rnd += 1
            assert left == 0
            if verbose: print('Solve succesfull in {} rounds!'.format(rnd)+' '*32)
            return True
        return sweep_mines(space)
    
    def solve_MCP(self, zonemap, minemap):
        # DIJKSTRA TIME!
        Z = len(zonemap)
        Y = len(zonemap[0])
        X = len(zonemap[0][0])
        copyzone = [[['ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(k) for k in j] for j in i] for i in zonemap]
        for k in range(Z):
            for j in range(Y):
                for i in range(X):
                    if minemap[k][j][i] == '#':
                        copyzone[k][j][i] = 99999
        grid = copyzone
        def inSpace(i,j,k):
            return (i in range(X) and j in range(Y) and k in range(Z))
        dis = [[[2**16 for i in range(X)] for j in range(Y)] for k in range(Z)]
        dx  = [-1, 0, 1, 0, 0, 0]
        dy  = [0, 1, 0, -1, 0, 0]
        dz  = [0, 0, 0, 0, 1, -1]
        # Cell: x, y, distance
        st = set()
        st.add(Cell(0,0,0,0))
        dis[0][0][0] = grid[0][0][0]
        parents = [[[-1 for i in range(X)] for j in range(Y)] for k in range(Z)]
        while st:
            k = st.pop()
            for i in range(6):
                x = k.x + dx[i]
                y = k.y + dy[i]
                z = k.z + dz[i]
                if not inSpace(x,y,z):
                    continue
                if (dis[z][y][x] > (dis[k.z][k.y][k.x] + grid[z][y][x])):
                    if (dis[z][y][x] != 2**16):
                        try:
                            st.remove(Cell(x,y,z,dis[z][y][x]))
                        except:
                            pass
                    dis[z][y][x] = dis[k.z][k.y][k.x] + grid[z][y][x]
                    st.add(Cell(x,y,z,dis[z][y][x]))
                    parents[z][y][x] = [k.x,k.y,k.z]
        revloc = parents[Z-1][Y-1][X-1]
        revroute = [[X-1,Y-1,Z-1]]
        while revloc != -1:
            revroute += [revloc]
            revloc = parents[revloc[2]][revloc[1]][revloc[0]]
        route = revroute[::-1]
        moves = [[route[i+1][j] - route[i][j] for j in range(3)] for i in range(len(route)-1)]
        movedic = {
            '[1, 0, 0]' : 'X',
            '[-1, 0, 0]' : 'x',
            '[0, 1, 0]' : 'Y',
            '[0, -1, 0]' : 'y',
            '[0, 0, 1]' : 'Z',
            '[0, 0, -1]' : 'z',
        }
        minpath = ''.join(movedic[str(i)] for i in moves)
        mincost = dis[Z-1][Y-1][X-1]
        return mincost, minpath
        

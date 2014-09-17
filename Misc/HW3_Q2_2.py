'''
Created on May 5, 2014

@author: Nengbao
'''
class EdgeWeightedDigraph(object):
    '''Edge weighted Directed Graph'''
    
    def __init__(self, numV):
        if numV < 0:
            raise 'Number of vertices should not be negative.'
        self.numV = numV
        self.numE = 0
        self.adj = [[] for _ in range(numV)] #NOTE: verify
        
    def V(self):
        return self.numV
    
    def E(self):
        return self.numE
    
    def addEdge(self, e):
        v = e.fro()
        self.adj[v].append(e)
        self.numE += 1
    
class DirectedEdge(object):
    '''Directed Edge'''
    
    def __init__(self, v, w, weight):
        if (v < 0 or w < 0):
            raise 'Vertex names should be nonnegative integers.'
        self.v = v
        self.w = w
        self.weight = weight
        
#     def weight(self):
#         return self.weight
    
    def fro(self):
        return self.v
    
    def to(self):
        return self.w

class EdgeWeightedDirectedCycle(object):
    ''' Detect cycles in digraph'''
    
    def __init__(self, G):
        self.onStack = [False] * G.V()
        self.edgeTo = [None] * G.V()
        self.marked = [False] * G.V()
        self.cycle = []
        
        for v in range(G.V()):
            if not self.marked[v]:
                self.dfs(G, v)
                
    def dfs(self, G, v):
        self.onStack[v] = True
        self.marked[v] = True
        for e in G.adj[v]:
            w = e.to()
            if(self.cycle != []):
                return
            elif (not self.marked[w]):
                self.edgeTo[w] = e
                self.dfs(G, w)
            elif self.onStack[w]:
                while (e.fro() != w):
                    self.cycle += [e]
                    e = self.edgeTo[e.fro()]
                self.cycle += [w] + [v]
        self.onStack[v] = False
    
    def hasCycle(self):
        return self.cycle != []
    
    def Cycle(self):
        return self.cycle
    
class CPM(object):
    '''Critical path method for longest path problem'''
    
    def CPM(self, test_in):
        utils = Utils()
        N, Dur, Pre = utils.read_file(test_in)
        G = EdgeWeightedDigraph(2*N + 2)
        s = 2*N
        t = 2*N + 1
        for i in range(N):
            G.addEdge(DirectedEdge(i, i+N, Dur[i]))
            G.addEdge(DirectedEdge(s, i, 0))
            G.addEdge(DirectedEdge(i+N, t, 0))

            for j in range(len(Pre[i])):
                successor = Pre[i][j]
                G.addEdge(DirectedEdge(i+N, successor, 0))
                
        ewdc = EdgeWeightedDirectedCycle(G)
        if ewdc.hasCycle():
            lp = None
        else:
            lp = AcyclicLP(G, s)
        utils.write_file(lp)
    
class AcyclicLP(object):
    '''Longest path in a DAG'''
    
    def __init__(self, G, s):
        self.edgeTo = [None] * G.V()
        self.distTo = [float("-inf")] * G.V()
        self.distTo[s] = 0
        
        top = Topological(G)
        for v in top.order:
            for e in G.adj[v]:
                self.relax(e)
                
    def relax(self, e):
        v = e.fro()
        w = e.to()
        if(self.distTo[w] < self.distTo[v] + e.weight):
            self.distTo[w] = self.distTo[v] + e.weight
            self.edgeTo[w] = e
            
class Topological(object):
    
    def __init__(self, G):
        finder = EdgeWeightedDirectedCycle(G)
        if(not finder.hasCycle()):
            dfs = DepthFirstOrder(G)
            self.order = dfs.reversePost()
        
#     def order(self):
#         return self.order
            
class DepthFirstOrder(object):
    
    def __init__(self, G):
        self.postorder = []
        self.preorder = []
        self.marked = [False] * G.V()
        
        for v in range(G.V()):
            if(not self.marked[v]):
                self.dfs(G, v)
                
    def dfs(self, G, v):
        self.marked[v] = True
        self.preorder.append(v)
        for e in G.adj[v]:
            w = e.to()
            if(not self.marked[w]):
                self.dfs(G, w)
        self.postorder.append(v)
        
    def reversePost(self):
        reverse = self.postorder[::-1]
        return reverse
    
class Utils(object):
    def read_file(self, test_in):
        lines = open(test_in, 'r').read().splitlines()
        N = int(lines[0])
        Dur = []
        Pre = []
        for line in lines[1:]:
            tmp = line.split()
            Dur.append(float(tmp[0]))
            tmp1 = list(map(int, tmp[1:]))
            Pre.append(tmp1)
        return N, Dur, Pre
    
    def write_file(self, lp):
        to = open('test.out', 'w')
        if lp == None:
            to.write('INFEASIBLE')
            to.close
        else:
            N = len(lp.distTo)
            N = (N-2)/2    # number of vertices
            for i in range(N):
                to.write(str(lp.distTo[i]) + '\n')
            to.close()
            print lp.distTo[:N]
cpm = CPM()                       
cpm.CPM('test.in')

        

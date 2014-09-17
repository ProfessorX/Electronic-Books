'''
Created on May 9, 2014

@author: Nengbao
'''
import Queue
from HW3_Q2_2 import EdgeWeightedDigraph 
from HW3_Q2_2 import DirectedEdge 
from HW3_Q2_2 import EdgeWeightedDirectedCycle

class BellmanFordSP(object):
    def __init__(self, G, s):
        self.distTo = [float("inf")] * G.V()
        self.distTo[s] = 0
        self.edgeTo = [None] * G.V()
        self.onQ = [False] * G.V()
        self.cost = 0
        self.q = Queue.Queue(0)
        self.cycle = []
        
        self.q.put(s)
        self.onQ[s] = True
        while (not self.q.empty() and not self.hasNegativeCycle()):
            v = self.q.get()
            self.onQ[v] = False
            self.relax(G, v)
            
    def relax(self, G, v):
        for e in G.adj[v]:
            w = e.to()
            if self.distTo[w] > self.distTo[v] + e.weight:
                self.distTo[w] = self.distTo[v] + e.weight
                self.edgeTo[w] = e
                if not self.onQ[w]:
                    self.q.put(w)
                    self.onQ[w] = True
            self.cost += 1
            if self.cost % G.V() == 0:
                self.findNegativeCycle()
                
    def findNegativeCycle(self):
        V = len(self.edgeTo)
        spt = EdgeWeightedDigraph(V)
        for v in range(V):
            if self.edgeTo[v] != None:
                spt.addEdge(self.edgeTo[v])
        finder = EdgeWeightedDirectedCycle(spt)
        self.cycle = finder.Cycle()

    def hasNegativeCycle(self):
        return self.cycle != []
    
class Utils(object):
    def read_file(self, f):
        lines = open(f, 'r').read().splitlines()
        N = int(lines[0])
        I = [[] for _ in range(N)]
        Tij = [[] for _ in range(N)]
        j = 0
        for line in lines[1:]:
            tmp = line.split()
            n = len(tmp)
            for i in range(0, n, 2):
                I[j].append(int(tmp[i]))
                Tij[j].append(float(tmp[i+1]))
            j += 1
        return N, I, Tij
    
    def write_file(self, BFSP):
        to = open('test.out', 'w')
        if BFSP == None:
            to.write('INFEASIBLE')
            to.close
        else:
            N = len(BFSP.distTo)
            N = N - 2
            for i in range(N):
                to.write(str(-BFSP.distTo[i]) + '\n') # Negate again
            to.close()
            print BFSP.distTo[:N]
            
class Main(object):
    # Main Idea:
    # 1. Construct graph (edge from i --> j (I[i] --> i) with weight -tij)
    # 2. Find shortest path
    # 3. Negate distTo
    def main(self, f):
        utils = Utils()
        N, I, Tij = utils.read_file(f)
        G = EdgeWeightedDigraph(N + 2)
        s = N
        t = N + 1
        for i in range(N):
#             G.addEdge(DirectedEdge(s, i, 0))
            G.addEdge(DirectedEdge(i, t, 0))
            
            for j in range(len(Tij[i])):
                G.addEdge(DirectedEdge(I[i][j], i, -( Tij[i][j] ) ) )     # Negate edge weight
                G.addEdge(DirectedEdge(s, I[i][j], 0))
#                 G.addEdge(DirectedEdge(I[i][j], t, 0))
                
        bfsp = BellmanFordSP(G, s)
        if bfsp.hasNegativeCycle():
            bfsp = None
        utils.write_file(bfsp)

start = Main()
start.main('test1.in')

        

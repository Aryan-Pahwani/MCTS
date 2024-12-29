from collections import defaultdict
import math

class MCTS:
    def __init__(self, c_param=1):
        self.reward = defaultdict(int)
        self.visits = defaultdict(int)
        self.children = dict()
        self.c_param = c_param

    def Selection(self, node):
        if node not in self.children:
            return node.find_random_child()
        def score(n):
            if self.visits[n] == 0:
                return float("-inf") 
            return self.reward[n] / self.visits[n]

        return max(self.children[node], key=score)
    
    def do_rollout(self, node):
        '''
        They see me rollin'

        Trains for one iteration
        '''
        path = self.Select(node)
        leaf = path[-1]
        self.Expand(leaf)
        reward = self.Simulate(leaf)
        self.Backpropogate(path, reward)

    def Select(self, node):
        '''
        Finds a new node
        '''
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self.uct_select(node) 

    def Expand(self, node):
      '''
        Updates Dict with new node
      '''
      if node in self.children:
          return  # If it has a node in children, its already expanded
      self.children[node] = node.get_children()

    def Simulate(self, node):
      '''
      Simulates and returns reward.
      '''
      invert_reward = True
      while True:
          if node.get_is_terminal():
              reward = node.reward()
              return 1 - reward if invert_reward else reward
          node = node.find_random_child()
          invert_reward = not invert_reward

    def Backpropogate(self, path, reward):
        for node in reversed(path):
            self.visits[node] += 1
            self.reward[node] += reward
            reward = 1 - reward # Good for me (X) is bad for enemy (O)

    def uct_select(self, node):
        assert all(n in self.children for n in self.children[node])

        log_visits_vertex = math.log(self.visits[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.reward[n] / self.visits[n] + self.c_param * math.sqrt(
                log_visits_vertex / self.visits[n]
            )

        return max(self.children[node], key=uct)
      

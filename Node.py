class Node:
  def get_children(self):
    '''
    All possible successors of this state
    '''
    pass

  def find_random_child(board):
    '''
    Finds a new child of current node.
    '''
    pass

  def is_terminal(self):
    '''
    Last possible node, True if Node has no children.
    '''
    pass
  def reward(self):
    '''
    Assuming that (self) is a terminal node. gives a reward from the choices [-1, 0, 1]
    '''
    pass

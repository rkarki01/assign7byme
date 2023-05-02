# masProblem.py - A Multiagent Problem
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable

class Node(Displayable):
    """A node in a search tree. It has a
    name a string
    isMax is True if it is a maximizing node, otherwise it is minimizing node
    children is the list of children
    value is what it evaluates to if it is a leaf.
    """
    def __init__(self, name, isMax):
        self.name = name
        self.isMax = isMax
        
    def is_leaf(self):
        """returns true of this is a leaf node"""
        return len(children) == 0
    
    def children(self):
        """returns the list of all children."""
        raise NotImplementedError()
    
    def evaluate(self):
        """returns the evaluation for this node if it is a leaf"""
        raise NotImplementedError()
        

class Magic_sum(Node):
    def __init__(self, xmove=True, last_move=None,
                 available=[1,2,3,4,5,6,7,8,9], x=[], o=[]):
        """This is a node in the search for the magic-sum game.
        xmove is True if the next move belongs to X.
        last_move is the number selected in the last move
        available is the list of numbers that are available to be chosen
        x is the list of numbers already chosen by x
        o is the list of numbers already chosen by o
        """
        self.isMax = self.xmove = xmove
        self.last_move = last_move
        self.available = available
        self.x = x
        self.o = o
        self.allchildren = None   #computed on demand
        lm = str(last_move)
        self.name = "start" if not last_move else "o="+lm if xmove else "x="+lm

    def children(self):
        if self.allchildren is None:
            if self.xmove:
                self.allchildren = [
                    Magic_sum(xmove = not self.xmove,
                              last_move = sel,
                              available = [e for e in self.available if e is not sel],
                              x = self.x+[sel],
                              o = self.o)
                            for sel in self.available]
            else:
                self.allchildren = [
                    Magic_sum(xmove = not self.xmove,
                              last_move = sel,
                              available = [e for e in self.available if e is not sel],
                              x = self.x,
                              o = self.o+[sel])
                            for sel in self.available]
        return self.allchildren

    def is_leaf(self):
        """A leaf has no numbers available or is a win for one of the players.
        We only need to check for a win for o if it is currently x's turn,
        and only check for a win for x if it is o's turn (otherwise it would
        have been a win earlier).
        """
        return (self.available == [] or
                (sum_to_15(self.last_move,self.o)
                 if self.xmove
                 else sum_to_15(self.last_move,self.x)))

    def evaluate(self):
        if self.xmove and sum_to_15(self.last_move,self.o):
            return -1
        elif not self.xmove and sum_to_15(self.last_move,self.x):
            return 1
        else:
            return 0
            
def sum_to_15(last,selected):
    """is true if last, toegether with two other elements of selected sum to 15.
    """
    return any(last+a+b == 15
               for a in selected if a != last
               for b in selected if b != last and b != a)


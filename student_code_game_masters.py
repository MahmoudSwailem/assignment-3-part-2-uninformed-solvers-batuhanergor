from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg_1 = self.kb.kb_ask(parse_input("fact: (on ?x peg1)"))
        peg_1_array = []
        
        if peg_1:
            for i in peg_1:
                peg_1_array.append(int(i['?x'][-1]))
            peg_1_array.sort()
    
        
        peg_2 = self.kb.kb_ask(parse_input("fact: (on ?x peg2)"))
        peg_2_array = []
        
        if peg_2:
            for i in peg_2:
                peg_2_array.append(int(i['?x'][-1]))
            peg_2_array.sort()


        peg_3 = self.kb.kb_ask(parse_input("fact: (on ?x peg3)"))
        peg_3_array = []

        if peg_3:
            for i in peg_3:
                peg_3_array.append(int(i['?x'][-1]))
            peg_3_array.sort()
        
        result = (tuple(peg_1_array), tuple(peg_2_array), tuple(peg_3_array))
        return result

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            disk = str(movable_statement.terms[0])
            in_peg = str(movable_statement.terms[1])
            tar_peg = str(movable_statement.terms[2])
            
            if self.kb.kb_ask(parse_input("fact: (ontop " + disk + " ?y)")):
                newtopfact = self.kb.kb_ask(parse_input("fact: (ontop " + disk + " ?y)"))
                newtopdisk = str(newtopfact[0].bindings[0].constant)
                self.kb.kb_assert(parse_input("fact: (top " + newtopdisk + " " + in_peg + ")"))
                self.kb.kb_retract(parse_input("fact: (ontop " + disk + " " + newtopdisk + ")"))
            else:
                self.kb.kb_assert(parse_input("fact: (empty " + in_peg + ")"))
            

            if self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + tar_peg + ")")):
                topfact = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + tar_peg + ")"))
                topdisk = str(topfact[0].bindings[0].constant)
                self.kb.kb_assert(parse_input("fact: (ontop " + disk + " " + topdisk + ")"))
                self.kb.kb_retract(parse_input("fact: (top " + topdisk + " " + tar_peg + ")"))
            else:
                self.kb.kb_retract(parse_input("fact: (empty " + tar_peg + ")"))

            self.kb.kb_retract(parse_input("fact: (on " + disk + " " + in_peg + ")"))
            self.kb.kb_retract(parse_input("fact: (top " + disk + " " + in_peg + ")"))
            self.kb.kb_assert(parse_input("fact: (on " + disk + " " + tar_peg + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + disk + " " + tar_peg + ")"))
            
                    
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))

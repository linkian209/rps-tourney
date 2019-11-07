"""classes.tourney

This module contains the Tourney class.
"""
from anytree import Node, RenderTree
from anytree.search import findall
from anytree.render import AsciiStyle
from classes.game import Game
from classes.match import Match
from classes.player import Player
from math import log2
from random import randint, shuffle


class Tourney():
    """
    This class contains the Tourney object. It creates the double elimination
    bracket when it is created. It contains methods to then run the individual
    brackets as well as the grand championship.

    Attributes:
        players (list): A list of Player objects in the tourney
        matches (list): A list of Match objects containing all matches played
        wins_needed (int): The number of wins needed to determine a winner of a match
        stages (int): The number of stages in the tourney
        upper_bracket (Node): The upper bracket tree
        lower_bracket (Node): The lower bracket tree

    Methods:
        make_upper_tree(self, stage, root): Makes upper bracket
        make_lower_tree(self, stage, root): Makes lower bracket
        print_brackets(self): Prints both brackets
        print_upper_bracket(self): Prints upper bracket
        print_lower_bracket(self): Prints lower bracket
        run_upper_bracket(self): Runs the upper bracket
        run_lower_bracket(self): Runs the lower bracket
        run_championship(self): Runs the championship
        victory_screen(self, victor): Creates the victory screen for the winner
    """
    def __init__(self, players, wins_needed=2):
        """
        This method initializes the Tourney Class. We will create the upper and
        lower brackets as well as the players in the tounrey. Raises an 
        exception if the number of players is not a power of 2.

        Arguments:
            :param self: This object
            :param players: A list of strings of names of players
            :param wins_needed: Number of wins needed to win a match. Default=2

        Raises:
            Exception: The number of players is not a power of 2
        """
        self.players = []
        self.matches = []
        self.wins_needed = wins_needed
        num_players = len(players)

        # Make sure we are a power of 2
        if(num_players is not 0 and num_players & (num_players - 1) is 0):
            self.stages = int(log2(num_players))

            print('Making a bracket with {} Stages'.format(self.stages))

            # Recursively make the trees
            self.upper_bracket = self.make_upper_tree(self.stages, Node('Stage{}'.format(self.stages+1), contestant='Upper Champ', player=None))
            if(self.stages is 1):
                self.lower_bracket = Node('Stage{}'.format(self.stages-1), contestant='Lower Champ', player=None)
            else:
                self.lower_bracket = self.make_lower_tree(self.stages - 1, Node('Stage{}-Major'.format(self.stages), contestant='Lower Champ', player=None))

            # Now populate the upper bracket to start
            shuffle(players)
            groups = zip(findall(self.upper_bracket, filter_=lambda node: node.name in ('Stage1')), players)
            for node, player in groups:
                node.contestant = player
                new_player = Player(player)
                self.players.append(new_player)
                node.player = new_player

            # We are now done! Print the brackets
            self.print_brackets()
        else:
            raise Exception('{} is not a power of 2'.format(num_players))
        
    def make_upper_tree(self, stage, root):
        """
        This method creates the upper tree. It recursively traverses down to 
        create the tree of nodes that is the upper bracket. We terminate
        the recursion at stage 1.

        Arguments:
            :param self: This tourney object
            :param stage: The stage of the tourney
            :param root: The root of this point in the tree

        Returns:
            Node: The root node
        """
        if(stage is 1):
            left = Node('Stage{}'.format(stage), parent=root, contestant='Stage{}'.format(stage-1), player=None)
            right = Node('Stage{}'.format(stage), parent=root, contestant='Stage{}'.format(stage-1), player=None)
        else:
            left = self.make_upper_tree(stage - 1, Node('Stage{}'.format(stage), parent=root, contestant='Stage{}'.format(stage-1), player=None))
            right = self.make_upper_tree(stage - 1, Node('Stage{}'.format(stage), parent=root, contestant='Stage{}'.format(stage-1), player=None))

        root.children = [left, right]
        return root

    def make_lower_tree(self, stage, root):
        """
        This method creates the lower tree. It recursively traverses down to 
        create the tree of nodes that is the lower bracket. We terminate
        the recursion at stage 1.

        The lower bracket differs from the upper bracket in that there is a
        minor and major part for each stage in the bracket.

        Arguments:
            :param self: This tourney object
            :param stage: The stage of the tourney
            :param root: The root of this point in the tree

        Returns:
            Node: The root node
        """
        if(stage is 1):
            left = Node('Stage{}-Minor'.format(stage+1), parent=root, contestant='Stage{}-Minor'.format(stage+1), player=None)
            right = Node('Stage{}-Major'.format(stage), parent=root, contestant='Stage{}-Major'.format(stage), player=None)
            sub_1 = Node('Stage{}-Major-Sub'.format(stage), parent=right, contestant='Stage{}-Major-Sub'.format(stage), player=None)
            sub_2 = Node('Stage{}-Major-Sub'.format(stage), parent=right, contestant='Stage{}-Major-Sub'.format(stage), player=None)
            right.children = [sub_1, sub_2]
        else:
            left = Node('Stage{}-Minor'.format(stage+1), parent=root, contestant='Stage{}-Minor'.format(stage+1), player=None)
            right = Node('Stage{}-Major'.format(stage), parent=root, contestant='Stage{}-Major'.format(stage), player=None)
            sub_1 = self.make_lower_tree(stage - 1, Node('Stage{}-Major-Sub'.format(stage), parent=right, contestant='Stage{}-Major-Sub'.format(stage), player=None))
            sub_2 = self.make_lower_tree(stage - 1, Node('Stage{}-Major-Sub'.format(stage), parent=right, contestant='Stage{}-Major-Sub'.format(stage), player=None))
            right.children = [sub_1, sub_2]

        root.children = [left, right]
        return root

    def print_brackets(self):
        """
        This method prints the brackets.

        Arguments:
            :param self: This object
        """
        self.print_upper_bracket()
        self.print_lower_bracket()

    def print_upper_bracket(self):
        """
        This method prints the upper bracket

        Arguments:
            :param self: This object
        """
        print('Upper Bracket')
        print('-------------')
        print(RenderTree(self.upper_bracket, style=AsciiStyle()).by_attr(attrname='contestant'))
        print('')

    def print_lower_bracket(self):
        """
        This method prints the lower bracket

        Arguments:
            :param self: This object
        """
        print('Lower Bracket')
        print('-------------')
        print(RenderTree(self.lower_bracket, style=AsciiStyle()).by_attr(attrname='contestant'))
        print('')

    def run_upper_bracket(self):
        """
        This method runs through the upper bracket. This advances through each
        stage and runs all matches required. Loses are demoted to the lower
        bracket and winners continue to the next stage.

        Arguments:
            :param self: This tourney
        """
        # Run through each stage and advance the winner as needed
        stage_num = 1
        while(stage_num <= self.stages):
            print('Upper Stage {}'.format(stage_num))
            print('---------------------------\n')
            cur_stage = stage_num + 1
            # Find the parents of all children nodes that need played
            nodes = findall(self.upper_bracket, filter_=lambda node: node.name in ('Stage{}'.format(cur_stage)))
            num_match = 1
            for node in nodes:
                player1, player2 = (x.player for x in node.children)
                cur_match = Match(player1, player2, self.wins_needed)

                print('Match {} - {} v. {}'.format(num_match, player1.name, player2.name))
                print('---------------------------------')
                results = cur_match.play_match()
                self.matches.append(cur_match)
                print('{} wins the match in {} games!\n'.format(results['winner'], results['games_played']))

                node.contestant = results['winner']
                node.player = player1 if results['winner'] == player1.name else player2

                # Move the loser down to the loser's bracket
                loser = player2 if results['winner'] == player1.name else player1
                loser.losses += 1

                # First check to see if this is the last stage
                #if(stage_num is self.stages):
                    # Since we are the last stage, we go to the minor of the previous stage
                    #lower = findall(self.lower_bracket, lambda node: node.name == 'Stage{}-Minor'.format(stage_num) and node.player is None)[0]
                    #lower.contestant = loser.name
                    #lower.player = loser
                # If we are an odd stage, we move to the major loser branch, else the minor
                #elif(stage_num % 2 is 1):
                    #lower = findall(self.lower_bracket, lambda node: node.name == 'Stage{}-Major-Sub'.format(stage_num) and node.player is None)[0]
                    #lower.contestant = loser.name
                    #lower.player = loser
                #else:
                    #lower = findall(self.lower_bracket, lambda node: node.name == 'Stage{}-Minor'.format(stage_num) and node.player is None)[0]
                    #lower.contestant = loser.name
                    #lower.player = loser

                if(stage_num is 1):
                    # Since we are the last stage, we go to the minor of the previous stage
                    lower = findall(self.lower_bracket, lambda node: node.name == 'Stage{}-Major-Sub'.format(stage_num) and node.player is None)[0]
                    lower.contestant = loser.name
                    lower.player = loser
                else:
                    lower = findall(self.lower_bracket, lambda node: node.name == 'Stage{}-Minor'.format(stage_num) and node.player is None)[0]
                    lower.contestant = loser.name
                    lower.player = loser
                num_match += 1

            # Now that this stage is done, print the brackets!
            stage_num += 1
            self.print_upper_bracket()
        # Done! Print the bracket
        print('End of Upper Bracket')
        print('---------------------------\n')
        self.print_brackets()

    def run_lower_bracket(self):
        """
        This method runs through the upper bracket. This advances through each
        stage and runs all matches required. Loses are done and winners advance
        to the next stage. The winner of the lower bracket plays in the grand
        championship.

        Arguments:
            :param self: This tourney
        """
        # Lower brackets alternate between major and minor events. If
        # applicable, we will do the minor for the stage (Stage 1 has
        # no minor), then we will do the majors
        stage_num = 1
        while(stage_num <= self.stages):
            print('Lower Stage {}'.format(stage_num))
            print('---------------------------\n')
            # If we are stage one, there is no minor
            if(stage_num is not 1):
                # Find the parents of all children nodes that need played
                nodes = findall(self.lower_bracket, filter_=lambda node: node.name == 'Stage{}-Major-Sub'.format(stage_num))
                num_match = 1
                for node in nodes:
                    print(node)
                    player1, player2 = (x.player for x in node.children)
                    cur_match = Match(player1, player2, self.wins_needed)

                    print('Match {} - {} v. {}'.format(num_match, player1.name, player2.name))
                    print('---------------------------------')
                    results = cur_match.play_match()
                    self.matches.append(cur_match)
                    print('{} wins the match in {} games!\n'.format(results['winner'], results['games_played']))

                    # Resolve Match
                    node.contestant = results['winner']
                    node.player = player1 if results['winner'] == player1.name else player2

                    # The loser is done! No more advancement. Move on to the minors.
                    loser = player2 if results['winner'] == player1.name else player1
                    loser.losses += 1

            # Now do the major
            # Find the parents of all children nodes that need played
            nodes = findall(self.lower_bracket, filter_=lambda node: node.name in ('Stage{}-Major'.format(stage_num)))
            num_match = 1
            for node in nodes:
                player1, player2 = (x.player for x in node.children)
                cur_match = Match(player1, player2, self.wins_needed)

                print('Match {} - {} v. {}'.format(num_match, player1.name, player2.name))
                print('---------------------------------')
                results = cur_match.play_match()
                self.matches.append(cur_match)
                print('{} wins the match in {} games!\n'.format(results['winner'], results['games_played']))

                # Resolve Match
                node.contestant = results['winner']
                node.player = player1 if results['winner'] == player1.name else player2

                # The loser is done! No more advancement. Move on to the minors.
                loser = player2 if results['winner'] == player1.name else player1
                loser.losses += 1

            # At the end of the stage, print the bracket
            stage_num += 1
            self.print_lower_bracket()
        
        # Done! Print the bracket
        print('End of Lower Bracket')
        print('---------------------------\n')
        self.print_brackets()

    def run_championship(self):
        """
        This method runs the grand championship match. Since this is a double
        elimination tourney, the lower bracket champion has to win 2 times in
        order to win the overall championship.

        Arguments:
            :param self: This tourney object
        """
        # Get champs
        upper = self.upper_bracket.player # pylint: disable=no-member
        lower = self.lower_bracket.player # pylint: disable=no-member

        print('Championship Match')
        print('{} v. {}'.format(upper.name, lower.name))
        print('Match 1')
        print('---------------------------------')
        cur_match = Match(upper, lower, self.wins_needed)
        results = cur_match.play_match()
        self.matches.append(cur_match)
        print('{} wins the match in {} games!\n'.format(results['winner'], results['games_played']))

        winner = upper if results['winner'] == upper.name else lower
        loser = lower if results['winner'] == upper.name else upper
        loser.losses += 1

        # If the upper lost, we need to play again
        if(loser.name == upper.name):
            print('\nMatch 2')
            print('---------------------------------')
            cur_match = Match(upper, lower, self.wins_needed)
            results = cur_match.play_match()
            self.matches.append(cur_match)
            print('{} wins the match in {} games!\n'.format(results['winner'], results['games_played']))

            winner = upper if results['winner'] == upper.name else lower
            loser = lower if results['winner'] == upper.name else upper
            loser.losses += 1

        # We can now crown the champion!
        print('\n\n')
        print('Grand Champion')
        print('---------------------------------')
        print('{}'.format(self.victory_screen(winner.name)))

    def victory_screen(self, victor):
        """
        This method returns a string for the the victory screen to crown
        the victor of the grand championship.

        Arguments:
            :param self: This tourney object
            :param victor: The name(str) of the victor of the championship

        Returns:
            str: The victory screen
        """
        victory_options = [
            '{} is victorious! Huzza!', '{} stomped some noobs.', 'Hail God Emperor {}!',
            'Bless {}! May his passing cleanse the world!'
        ]
        return victory_options[randint(0, len(victory_options)-1)].format(victor)
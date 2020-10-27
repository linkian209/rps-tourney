"""classes.qplayer

This module contains the QPlayer class.

"""
import numpy as np
from classes.enums import Choice
from classes.player import Player


class QPlayer(Player):
    """
    The QPlayer class extends the Player class to allow for Q Learning.
    The two main additions are the q table and state table. The state table
    is a large N dimensional list that translates game history into a state.
    The q-table then is a 2 dimensional array where the state and action are
    in 
    
    Inherited Attributes:
        name (str): The name of the player
        options (list): An enumeration of the options that it can throw when
                        playing
        wins (int): Number of games won
        losses (int): Number of games lost

    New Attributes:
        learning_rate (float): The learning rate for this player
        discount (float): The amount this player discounts future actions
        exploration (float): The probability for the player to randomly act
        q_table (ndarray): The Q Table for this player, its dimensions are
                           (number of states, number of actions), which is
                           (num_states, len(Choice)). However, the q_table
                           can have more states than are in num_states if we
                           load in a previous state table.
        state_table (list): A translation table to get the state number for
                            the Q Table. Based on the number of games we are
                            remembering, we have a number of layers for the
                            state table. Generally, further into the table, 
                            the more recent the game.
        num_states (int): The number of possible states

    Overridden Methods:
        throw(self, history): Throws rock, paper, or scissors based on history
                              and Q table

    New Methods:
        learn(self, history, result): Updates Q Table
        init_q_table(self, cur_level): Recursively initializes the Q table
        state_table_by_level(state_num, cur_level): Generates the state table
                                                    recursively
        load_q_table(self, filename): Load in a past Q-Table
        save_q_table(self, filename): Save this QPlayer's Q-Table
    """
    def __init__(self, name, learning_rate, discount, exploration, hist_length=3):
        """
        Initializes the QPlayer.

        Arguments:
            :param self: The object
            :param name: The name of the player
            :param hist_length: The number of games of history to keep,
                                this affects the Q table
        """
        # Start by calling the base class init function
        super().__init__(name)

        # Now initialize the deep learning values
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration = exploration
        self.hist_length = hist_length

        # Now set up the state table. There are levels of the state table based
        # on the number of games played. The passed in variable, hist_length,
        # tells us how many games at most we will store. 
        self.state_table = []
        state_num = 0
        for i in range(hist_length + 1):
            if(i is 0):
                self.state_table.append(state_num)
                state_num += 1
            else:
                state_num, new_rec = QPlayer.state_table_by_level(state_num, i)
                self.state_table.append(new_rec)
        self.num_states = state_num

        # Now set up the q-table, then we are done
        self.q_table = np.empty((state_num, len(Choice)))
        for i in range(hist_length + 1):
            if(i is  0):
                # For the first game, we have nothing to go on.
                self.q_table[0] = [1, 1, 1]
            else:
                self.init_q_table(self.state_table[i], i)
        
    def init_q_table(self, state_table, cur_level):
        """
        This method recursively initializes the Q Table. At the beginning,
        we are going to reward winning and tieing, and penalize losing. 
        Winning will be worth more than tieing.

        Arguments:
            :param self: (QPlayer) This QPlayer
            :param state_table: (list) Current level of state table
            :param cur_level: (int) Current level of recursion
        """
        if(cur_level is 1):
            for i in Choice:
                for j in Choice:
                    # In the state table, the rows are the opponent's moves, 
                    # and the columns are this QPlayer's moves
                    # Tie
                    if(i is j):
                        self.q_table[state_table[i.value][j.value], j.value] = 1
                    # Rock loses to Paper, but beats Scissors
                    elif(i is Choice.ROCK):
                        if(j is Choice.SCISSORS):
                            self.q_table[state_table[i.value][j.value], j.value] = -5
                        else:
                            self.q_table[state_table[i.value][j.value], j.value] = 3
                    # Scissors loses to Rock, but beats Paper
                    elif(i is Choice.SCISSORS):
                        if(j is Choice.PAPER):
                            self.q_table[state_table[i.value][j.value], j.value] = -5
                        else:
                            self.q_table[state_table[i.value][j.value], j.value] = 3
                    # Paper loses to Scissors, but beats Rock
                    else:
                        # Player 1 wins on a Rock
                        if(j is Choice.ROCK):
                            self.q_table[state_table[i.value][j.value], j.value] = -5
                        else:
                            self.q_table[state_table[i.value][j.value], j.value] = 3
        else:
            for i in Choice:
                for j in Choice:
                    self.init_q_table(state_table[i.value][j.value], cur_level-1)

    def load_q_table(self, filename):
        """
        This method loads a q-table from a numpy exported file. 

        Arguments:
            :param self: (QPlayer) This QPlayer
            :param filename: (str) path and filename

        Returns:
            bool: True if loaded successfully, False otherwise 
        """
        try:
            # Load in table
            loaded_table = np.load(filename)

            # If the loaded table is bigger than the current one, just
            # overwrite it.
            if(self.num_states <= loaded_table.shape[0]):
                self.q_table = loaded_table
            # If the current table has more states, only overwrite the 
            # loaded in ones
            else:
                self.q_table[:loaded_table.shape[0]] = loaded_table
        except:
            return False
        
        return True

    def save_q_table(self, filename):
        """
        This method saves a q-table to the inputted filename

        Arguments:
            :param self: (QPlayer) This QPlayer
            :param filename: (str) path and filename

        Returns:
            bool: True if saved successfully, False otherwise 
        """
        try:
            np.save(filename, self.q_table)
        except:
            return False

        return True


    @staticmethod
    def state_table_by_level(state_num, cur_level):
        """
        This method recursively generates a N-dimensional list for the state
        translation table. The base case is a 3x3 list symbolizing a the
        history of what we threw v. what our opponent threw.

        Arguments:
            :param state_num: (int) Current state number
            :param cur_level: (int) Current level number

        Returns:
            (int, list): The new state number and a list of states
        """
        if(cur_level is 1):
            return ((state_num + 9), [
                [state_num, state_num+1, state_num+2],
                [state_num+3, state_num+4, state_num+5],
                [state_num+6, state_num+7, state_num+8]
            ])

        retval = []
        for i in Choice:
            new_row = []
            for j in Choice:
                state_num, new_rec = QPlayer.state_table_by_level(state_num, cur_level-1)
                new_row.append(new_rec)
            retval.append(new_row)

        return (state_num, retval)

    def get_player_number(self, game):
        """
        This method returns the integer player number for this player based
        on the inputted game. Returns -1 if this player did not take part in
        the game.

        Arguments:
            :param self: (QPlayer) This QPlayer
            :param game: (QGame) The game to check

        Returns:
            int: The player number for this player or -1 if the player did
                 not take part in the game.
        """
        if(game.player1.name == self.name):
            return 1
        elif(game.player2.name == self.name):
            return 2
        else:
            return -1


    def throw(self, history):
        """
        This method is used to actually play rock, paper, scissors. It throws
        one of the available options in the form:
            {
                'choice': Choice,
                'str': str,
                'reward': float,
                'state': int
            }

        The player uses the state table to look up what state to use in the 
        q-table, thus indicating which choice to select.

        Arguments:
            :param self: The object
            :param history: A list of Games of the match so far

        Returns:
            dict: A dictionary containing the int representation and the
                  string representation of the choice thrown.
        """
        # First we need to figure out what state we are in
        num_games = len(history)
        state = 0

        # This is the first game, thus easy
        if(num_games is 0):
            state = self.state_table[0]
        # There have been multiple games
        else:
            # Find which player we are
            player_num = self.get_player_number(history[0])

            # Figure out where to start
            state_table = []
            if(num_games <= self.hist_length):
                state_table = self.state_table[num_games]
            else:
                state_table = self.state_table[-1]
                history = history[-self.hist_length:]

            # Now figure out what state we are in.
            my_choice = None
            opponent_choice = None
            for game in history:
                # Figure out what choices were made
                if(player_num is 1):
                    my_choice = game.player1_throw['choice']
                    opponent_choice = game.player2_throw['choice']
                else:
                    my_choice = game.player2_throw['choice']
                    opponent_choice = game.player1_throw['choice']

                # Now update the temp table
                state_table = state_table[opponent_choice.value][my_choice.value] 

            # Because of how the loop is working, we will end up with the state
            # from the state_table    
            state = state_table

        # Now that we have the state, check if we are exploring or taking the
        # max reward value
        if(self.exploration <= np.random.default_rng().random()):
            choice = Choice(np.random.default_rng().integers(len(Choice)))
        else:
            choice = Choice(np.argmax(self.q_table[state]))
        return {
            'choice': choice, 'str': self.options[choice],
            'reward': self.q_table[state, choice.value],
            'state': state
        }

    def learn(self, history, result):
        """
        This method takes in the history and result and updates the Q Table.

        Arguments:
            :param self: (QPlayer) This QPlayer
            :param history: (list(QGame)) The match history
            :param result: (QGame) The results of the game
        """
        # First get our player number
        player_num = self.get_player_number(result)
        
        # Next get current state and immediate reward from the result
        immediate_reward = 0
        cur_state = 0
        if(player_num is 1):
            immediate_reward = result.player1_throw['reward']
            cur_state = result.player1_throw['state']
        else:
            immediate_reward = result.player2_throw['reward']
            cur_state = result.player2_throw['state']
        
        # Append the result to this local copy of the history
        history.append(result)

        # Now start Q Learning, start by getting new state
        num_games = len(history)
        state = 0

        # Set up beginning state table and history
        state_table = []
        if(num_games <= self.hist_length):
            state_table = self.state_table[num_games]
        else:
            state_table = self.state_table[-1]
            history = history[-self.hist_length:]

        # Now figure out what state we are in.
        my_choice = None
        opponent_choice = None
        for game in history:
            # Figure out what choices were made
            if(player_num is 1):
                my_choice = game.player1_throw['choice']
                opponent_choice = game.player2_throw['choice']
            else:
                my_choice = game.player2_throw['choice']
                opponent_choice = game.player1_throw['choice']

            # Now update the temp table
            state_table = state_table[opponent_choice.value][my_choice.value] 

        # Because of how the loop is working, we will end up with the state
        # from the state_table    
        state = state_table

        # Now that we have the new state, get the optimal reward for this state
        optimal_future = np.max(self.q_table[state])

        # The learned value of this game is the observed immediate reward plus
        # the discounted optimal future reward
        learned_value = immediate_reward + self.discount * optimal_future

        # The update the Q Table
        self.q_table[cur_state, my_choice.value] = (1 - self.learning_rate) * self.q_table[cur_state, my_choice.value] + self.learning_rate * learned_value
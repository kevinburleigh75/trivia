#!/usr/bin/env python3

class Game:
    def __init__(self):
        self.players        = []

        self.max_num_players = 6

        self.places         = [0] * self.max_num_players
        self.purses         = [0] * self.max_num_players
        self.in_penalty_box = [0] * self.max_num_players

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        self.pop_questions     = ['Pop Question {}'.format(i)     for i in range(50)]
        self.science_questions = ['Science Question {}'.format(i) for i in range(50)]
        self.sports_questions  = ['Sports Question {}'.format(i)  for i in range(50)]
        self.rock_questions    = ['Rock Question {}'.format(i)    for i in range(50)]

        self.how_many_places          = 12
        self.coins_needed_for_victory = 6

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print('{} was added'.format(player_name))
        print('They are player number {}'.format(self.how_many_players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print('{} is the current player'.format(self.players[self.current_player]))
        print('They have rolled a {}'.format(roll))

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print('{} is getting out of the penalty box'.format(
                    self.players[self.current_player]
                ))
                self.places[self.current_player] = (self.places[self.current_player] + roll) % self.how_many_places

                print('{}\'s new location is {}'.format(
                    self.players[self.current_player],
                    self.places[self.current_player],
                ))
                print('The category is {}'.format(self._current_category))
                self._ask_question()
            else:
                print('{} is not getting out of the penalty box'.format(
                    self.players[self.current_player]
                ))
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = (self.places[self.current_player] + roll) % self.how_many_places

            print('{}\'s new location is {}'.format(
                self.players[self.current_player],
                self.places[self.current_player],
            ))
            print('The category is {}'.format(self._current_category))

            self._ask_question()

    def _ask_question(self):
        if self._current_category == 'Pop':     print(self.pop_questions.pop(0))
        if self._current_category == 'Science': print(self.science_questions.pop(0))
        if self._current_category == 'Sports':  print(self.sports_questions.pop(0))
        if self._current_category == 'Rock':    print(self.rock_questions.pop(0))

    @property
    def _current_category(self):
        if self.places[self.current_player] ==  0: return 'Pop'
        if self.places[self.current_player] ==  1: return 'Science'
        if self.places[self.current_player] ==  2: return 'Sports'
        if self.places[self.current_player] ==  3: return 'Rock'
        if self.places[self.current_player] ==  4: return 'Pop'
        if self.places[self.current_player] ==  5: return 'Science'
        if self.places[self.current_player] ==  6: return 'Sports'
        if self.places[self.current_player] ==  7: return 'Rock'
        if self.places[self.current_player] ==  8: return 'Pop'
        if self.places[self.current_player] ==  9: return 'Science'
        if self.places[self.current_player] == 10: return 'Sports'
        if self.places[self.current_player] == 11: return 'Rock'
        raise 'invalid current_player value {}'.format(self.current_player)

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print('{} now has {} Gold Coins.'.format(
                    self.players[self.current_player],
                    self.purses[self.current_player],
                ))

                game_should_continue = self._game_should_continue()
                self.current_player = (self.current_player + 1) % self.how_many_players
                return game_should_continue
            else:
                self.current_player = (self.current_player + 1) % self.how_many_players
                game_should_continue = True
                return game_should_continue
        else:
            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print('{} now has {} Gold Coins.'.format(
                self.players[self.current_player],
                self.purses[self.current_player],
            ))

            game_should_continue = self._game_should_continue()
            self.current_player = (self.current_player + 1) % self.how_many_players

            return game_should_continue

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print('{} was sent to the penalty box'.format(self.players[self.current_player]))
        self.in_penalty_box[self.current_player] = True

        self.current_player = (self.current_player + 1) % self.how_many_players
        game_should_continue = True

        return game_should_continue

    def _game_should_continue(self):
        return not (self.purses[self.current_player] == self.coins_needed_for_victory)

from random import randrange

if __name__ == '__main__':
    ##################################
    ## Check for a given random seed.
    ## This is used during testing to
    ## give predictable outputs.
    ##
    import sys
    from random import seed
    if len(sys.argv) == 2:
        seed(int(sys.argv[1]))
    ##################################

    game_should_continue = True

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while game_should_continue:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            game_should_continue = game.wrong_answer()
        else:
            game_should_continue = game.was_correctly_answered()

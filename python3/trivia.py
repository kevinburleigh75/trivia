#!/usr/bin/env python3

class Game:
    def __init__(self):
        self.players        = []
        self.places         = []
        self.purses         = []
        self.in_penalty_box = []

        self.current_player = 0
        self.is_getting_out_of_penalty_box = False

        self.number_of_questions_per_deck = 50
        self.pop_questions     = ['Pop Question {}'.format(i)     for i in range(self.number_of_questions_per_deck)]
        self.science_questions = ['Science Question {}'.format(i) for i in range(self.number_of_questions_per_deck)]
        self.sports_questions  = ['Sports Question {}'.format(i)  for i in range(self.number_of_questions_per_deck)]
        self.rock_questions    = ['Rock Question {}'.format(i)    for i in range(self.number_of_questions_per_deck)]

    def add(self, player_name):
        self.players.append(player_name)
        self.places.append(0)
        self.purses.append(0)
        self.in_penalty_box.append(False)

        print('{} was added'.format(player_name))
        print('They are player number {}'.format(len(self.players)))

        return True

    # @property
    # def how_many_players(self):
    #     return len(self.players)

    def roll(self, roll):
        def update_player_place():
            self.places[self.current_player] = (self.places[self.current_player] + roll) % 12
            print('{}\'s new location is {}'.format(
                self.players[self.current_player],
                self.places[self.current_player],
            ))
            print('The category is {}'.format(self._current_category))

        print('{} is the current player'.format(self.players[self.current_player]))
        print('They have rolled a {}'.format(roll))

        if self.in_penalty_box[self.current_player]:
            self.is_getting_out_of_penalty_box = (roll % 2 != 0)
            if self.is_getting_out_of_penalty_box:
                print('{} is getting out of the penalty box'.format(self.players[self.current_player]))
                update_player_place()
                self._ask_question()
            else:
                print('{} is not getting out of the penalty box'.format(
                    self.players[self.current_player]
                ))
        else:
            update_player_place()
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
        raise 'unknown place {}'.format(self.places[self.current_player])

    def was_correctly_answered(self):
        if not self.in_penalty_box[self.current_player] or self.is_getting_out_of_penalty_box:
            self.purses[self.current_player] += 1
            print('Answer was correct!!!!')
            print('{} now has {} Gold Coins.'.format(
                self.players[self.current_player],
                self.purses[self.current_player],
            ))

        game_should_continue = self.should_game_continue()
        self.current_player = (self.current_player + 1) % len(self.players)
        return game_should_continue

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def should_game_continue(self):
        return self.purses[self.current_player] != 6


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

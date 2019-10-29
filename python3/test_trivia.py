import os
import pytest
import trivia

trivia_seeds = [
    '1111',
    '1234',
    '2222',
    '23',
    '3333',
    '4',    ## no penalty box
    '4321',
    '4444',
    '5555',
]

@pytest.fixture(scope='module', params=trivia_seeds)
def trivia_seed(request):
    yield request.param

@pytest.mark.skip()
def test_output_for_given_seed(trivia_seed):
    cmd = 'python trivia.py {}'.format(trivia_seed)
    golden_output = open('./golden_outputs/seed_{}.txt'.format(trivia_seed), 'r').read()

    actual_output = os.popen(cmd).read()

    assert actual_output == golden_output

def test_P_notin_PB_ans_C_then_P_notin_PB():
    game = create_single_player_game(in_penalty_box=False)

    game.was_correctly_answered()

    assert game.in_penalty_box[0] == False

def test_P_notin_PB_ans_I_then_P_in_PB():
    game = create_single_player_game(in_penalty_box=False)

    game.roll(3)
    game.wrong_answer()

    assert game.in_penalty_box[0] == True

def test_P_in_PB_and_roll_even_then_P_in_PB():
    game = create_single_player_game(in_penalty_box=True)

    game.roll(4)

    assert game.in_penalty_box[0] == True

def test_P_in_PB_and_roll_even_then_not_place_advances():
    game = create_single_player_game(in_penalty_box=True, place=3)

    game.roll(4)

    assert game.places[0] == 3

def test_P_in_PB_and_roll_odd_then_P_notin_PB():
    game = create_single_player_game(in_penalty_box=True)

    game.roll(3)

    assert game.in_penalty_box[0] == False

def test_P_in_PB_and_roll_odd_then_place_advances():
    game = create_single_player_game(in_penalty_box=True, place=10)

    game.roll(3)

    assert game.places[0] == 1

def test_P_in_PB_and_roll_even_then_no_Q():
    game = create_single_player_game(in_penalty_box=True)
    orig_total_Qs = total_question_count(game)

    game.roll(2)

    new_total_Qs = total_question_count(game)

    assert new_total_Qs == orig_total_Qs

def test_P_in_PB_and_roll_odd_then_Q():
    game = create_single_player_game(in_penalty_box=True)
    orig_total_Qs = total_question_count(game)

    game.roll(3)

    new_total_Qs = total_question_count(game)

    assert new_total_Qs == orig_total_Qs - 1

def test_P_notin_PB_place_advances():
    game = create_single_player_game(in_penalty_box=False, place=10)

    game.roll(3)

    assert game.places[0] == 1

def test_P_notin_PB_and_roll_even_then_Q():
    game = create_single_player_game(in_penalty_box=False)
    orig_total_Qs = total_question_count(game)

    game.roll(2)

    new_total_Qs = total_question_count(game)

    assert new_total_Qs == orig_total_Qs - 1

def create_single_player_game(in_penalty_box=False, place=0):
    game = trivia.Game()
    game.add('SomePlayer')
    game.places[0] = place
    game.in_penalty_box[0] = in_penalty_box

    return game

def total_question_count(game):
    return len(game.pop_questions +
               game.rock_questions +
               game.science_questions +
               game.sports_questions)

import os
import pytest

trivia_seeds = [
    '1111',
    '1234',
    '2222',
    '3333',
    '4',    ## no penalty box
    '4321',
    '4444',
    '5555',
]

@pytest.fixture(scope='module', params=trivia_seeds)
def trivia_seed(request):
    yield request.param

def test_output_for_given_seed(trivia_seed):
    cmd = 'python trivia.py {}'.format(trivia_seed)
    golden_output = open('./golden_outputs/seed_{}.txt'.format(trivia_seed), 'r').read()

    actual_output = os.popen(cmd).read()

    assert actual_output == golden_output


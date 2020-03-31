game_parameters = {
    'players' : 18,
    'days' : 39,
    'jury' : 10,
    'final' : 3,
    'tribes' : 2,
}

def check_parameters(par):
    if (par['players']/par['tribes']) % 1 != 0:
        raise GameSetupError('Uneven number of players.')

class GameSetupError(Exception):
    pass

def get_params():
    check_parameters(game_parameters)
    return game_parameters

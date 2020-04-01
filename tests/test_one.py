import pytest
from surv.game.game import Game

@pytest.fixture()
def g():
    return Game()

def test_make_game(g):
    assert isinstance(g,Game)

def test_make_alliance(g):
    players = g.players[3:5]

    a = g.create_alliance(players)

    assert a.members == players
    assert a in g.alliances

def test_active_alliances(g):
    players = g.players[3:5]
    a = g.create_alliance(players)

    a.active = False

    assert a not in g.active_alliances()

def test_add_player(g):
    players = g.players[8:12]
    a = g.create_alliance(players)

    a.add_player(g.players[5])

    assert g.players[5] in a.members
    assert g.players[5].alliance == a

def test_remove_player(g):
        players = g.players[8:12]
        a = g.create_alliance(players)

        a.remove_player(g.players[10])

        assert g.players[5] not in a.members
        assert g.players[5].alliance == None

def test_swap_player(g):
        a = g.create_alliance(g.players[1:5])
        b = g.create_alliance(g.players[6:10])
        switch = g.players[9]

        a.add_player(switch)

        assert switch not in b.members
        assert switch in a.members
        assert switch.alliance == a

def test_alliance_dies(g):
        players = g.players[8:10]
        a = g.create_alliance(players)

        a.remove_player(g.players[8])

        assert g.players[8].alliance == None
        assert g.players[9].alliance == None
        assert len(a.members) == 0
        assert a.active == False
        assert a not in g.active_alliances()
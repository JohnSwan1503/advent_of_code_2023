import re
from typing import NamedTuple

class GameResults(NamedTuple):
    game_id: int
    green: int
    red: int
    blue: int

    def __gt__(self, other: 'GameResults') -> bool:  # type: ignore
        return any([ self.green > other.green
                   , self.red > other.red
                   , self.blue > other.blue])

regex = r"(?P<game_id>(?<=[Gg]ame )\d+)|(?P<green>\d+(?= green))|(?P<red>\d+(?= red))|(?P<blue>\d+(?= blue))"

def get_game_reults(game: str) -> GameResults:
    
    find_iter = re.finditer(regex, game)
    game_id, green, red, blue = 0, 0, 0, 0

    for match in find_iter:
        if match.group('game_id'):
            game_id = max(int(match.group('game_id')), game_id)
        elif match.group('green'):
            green = max(int(match.group('green')), green)
        elif match.group('red'):
            red = max(int(match.group('red')), red)
        elif match.group('blue'):
            blue = max(int(match.group('blue')), blue)

    return GameResults(game_id, green, red, blue)

with open('input.txt', 'r') as f: # I'm stuck on windows for work so make sure to update for your OS
    games = [get_game_reults(game) for game in f.readlines()]
    print(sum(game.game_id for game in games if not game > GameResults(0, 13, 12, 14)))
    print(sum(game.green * game.red * game.blue for game in games))

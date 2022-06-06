import json
import itertools 
import constants
import utils


def is_highscore(score: int) -> bool:
    leaderboard = get_leaderboard()
    if not leaderboard:
        return True

    if score > leaderboard[0][1]:
        return True


def get_leaderboard():
    highscores = get_highscores()
    if highscores is None:
        return []
    # Converting into list of tuple
    leaderboard = list(highscores.items())
    # Sort leaderboard list based on the score in descending order
    leaderboard.sort(key=lambda entry: entry[1], reverse=True)
    return leaderboard[0:10]


def get_highscores():
    # Opening JSON that we keep the highscores
    try:
        with open(constants.HIGH_SCORE_FILE, 'r') as file:
            # Returns a dictionary with the username as key and the score as value
            return json.load(file)
    except IOError:
        return None


def update_highscores(username: str, score: int):
    if utils.is_string_blank(username):
        return

    if score <= 0:
        return

    highscores = get_highscores()
    if highscores is None:
        highscores = {}

    
    if username in highscores:
        if highscores[username] < score:
            # update only if it's personal highscore
            highscores[username] = score
    else:
        highscores[username] = score

    highscores = dict(sorted(highscores.items(), key=lambda item: item[1], reverse=True))
    highscores = dict(itertools.islice(highscores.items(), 10)) 
 
    try:
        # create file if not exists and open it in write mode
        with open(constants.HIGH_SCORE_FILE, 'w+') as file:
            json.dump(highscores, file)
    except IOError:
        return None

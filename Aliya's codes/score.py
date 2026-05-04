score = 0
combo = 0

def calculate_score(correct, time_left):
    global score, combo

    if correct:
        combo += 1

        # base points
        points = 100

        # speed bonus
        points += int(time_left * 5)

        # combo bonus
        points += combo * 10

        score += points
        return f"Correct! +{points}"

    else:
        combo = 0
        return "Wrong order!"

def reset_score():
    global score, combo
    score = 0
    combo = 0

def get_score():
    return score

def get_combo():
    return combo
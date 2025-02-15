import random

CLUES = [
    "Haven-7 lies beyond the twin red stars.",
    "The safe zone is hidden near a gas giant.",
    "Avoid the icy wastelands, Haven-7 is not there.",
    "Follow the path of the ancient traders.",
    "The refuge is in the shadow of a dying sun."
]

def get_random_clue():
    return random.choice(CLUES)

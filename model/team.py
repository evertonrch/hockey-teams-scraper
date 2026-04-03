class Team:

    def __init__(self, name, year, wins, losses, ot_losses, win_percent, goals_for, goals_against, diff):
        self.name = name
        self.year = year
        self.wins = wins
        self.losses = losses
        self.ot_losses = ot_losses
        self.win_percent = win_percent
        self.goals_for = goals_for
        self.goals_against = goals_against
        self.diff = diff
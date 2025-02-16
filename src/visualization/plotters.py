import matplotlib.pyplot as plt

class PerformancePlotter:
    def __init__(self):
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def plot(self):
        plt.plot(self.scores)
        plt.title("AI Performance Over Time")
        plt.xlabel("Episodes")
        plt.ylabel("Score")
        plt.show()

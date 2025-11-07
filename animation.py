from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from janestreet_baseball import calculate_q

def update_line(line, x, y_max=0.35):
    line.set_segments([[(x, 0), (x, y_max)]])

def animate(i, state, lines):
    leftLine, rightLine, startLine, endLine = lines

    if i == 0:
        state["start"], state["end"] = 0, 1
    elif i % 2 == 0:
        leftPos = state["start"] + (state["end"] - state["start"]) / 3
        rightPos = state["end"] - (state["end"] - state["start"]) / 3
        update_line(leftLine, leftPos)
        update_line(rightLine, rightPos)
        if calculate_q(leftPos) > calculate_q(rightPos):
            state["end"] = rightPos
        else:
            state["start"] = leftPos
    else:
        update_line(startLine, state["start"])
        update_line(endLine, state["end"])

    return lines

def save_animation(filename):
    xs = np.linspace(1e-10, 1 - 1e-10, 100)
    ys = [calculate_q(Fraction(x)) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys)
    ax.set(xlabel="Probability of home run (P)",
           ylabel="Probability of full count (Q)",
           title="Probability of full count vs home run")

    state = {"start": 0, "end": 1}
    lines = [
        ax.vlines(state["start"], 0, 0.35, "g", "dashed"),
        ax.vlines(state["end"], 0, 0.35, "g", "dashed"),
        ax.vlines(state["start"], 0, 0.35, "r", "dashed"),
        ax.vlines(state["end"], 0, 0.35, "r", "dashed"),
    ]

    ani = animation.FuncAnimation(fig, animate, frames=25, interval=500, repeat=True, blit=True, fargs=(state, lines))

    writer = animation.PillowWriter(fps=2, metadata=dict(artist="Me"), bitrate=1800)
    ani.save(filename, writer=writer)

if __name__ == "__main__":
    save_animation("janestreet_baseball.gif")

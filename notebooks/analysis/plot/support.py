"""
Plotting support functions and variables.
"""

import matplotlib.pyplot as plt

light_palette = ['#ffffed', '#feefd1', '#fed6a9', '#eab799']


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def draw_fill(ax: plt.Axes, x0: float, x1: float, y0: float, y1: float, color: str):
    # Get the size of the plot.
    _, ymax = ax.get_ylim()
    # Fill the entire area.
    ax.axvspan(x0, x1, ymin=y0 / ymax, ymax=y1 / ymax, color=color)


def draw_arrow(ax: plt.Axes, x0: float, x1: float, y0: float, y1: float, color: str, **options):
    arrowstyle = options['arrowstyle'] if 'arrowstyle' in options else "->"
    linewidth = options['linewidth'] if 'linewidth' in options else 3
    linestyle = options['linestyle'] if 'linestyle' in options else "-"
    l0 = options['l0'] if 'l0' in options else None
    l1 = options['l1'] if 'l1' in options else None
    # Draw the arrow.
    ax.annotate("", xytext=(x0, y0), xy=(x1, y1),
                arrowprops=dict(arrowstyle=arrowstyle, linewidth=linewidth, linestyle=linestyle, color=color))
    # Draw the starting time.
    if l0:
        if (y0 < y1):
            ax.text(x0 + 0.05, y0 + 0.05, l0, ha='left', va='bottom', fontstyle='italic', color="gray")
        else:
            ax.text(x0 + 0.05, y0 - 0.1, l0, ha='left', va='top', fontstyle='italic', color="gray")
    if l1:
        if (y0 < y1):
            ax.text(x1 - 0.05, y1 - 0.1, l1, ha='right', va='top', fontstyle='italic', color="gray")
        else:
            ax.text(x1 - 0.05, y1 + 0.05, l1, ha='right', va='bottom', fontstyle='italic', color="gray")


def draw_middle_band(ax: plt.Axes, x0: float, x1: float, width: float, **options):
    color = options['color'] if 'color' in options else 'b'
    hatchwidth = options['hatchwidth'] if 'hatchwidth' in options else None
    linewidth = options['linewidth'] if 'linewidth' in options else 3
    if hatchwidth:
        old_hatchwidth = plt.rcParams['hatch.linewidth']
        # Set the new hatch.linewidth.
        plt.rcParams['hatch.linewidth'] = hatchwidth
        # Add a band representing the answer delay.
        ax.axvspan(x0, x1, ymin=0.5 - width, ymax=0.5 + width, linewidth=linewidth, edgecolor=color, fill=False, hatch='/')
    else:
        # Add a band representing the answer delay.
        ax.axvspan(x0, x1, ymin=0.5 - width, ymax=0.5 + width, facecolor=color)

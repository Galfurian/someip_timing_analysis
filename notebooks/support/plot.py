"""
Plot functions.
"""

from someip_timing_analysis.entities import *
from .utility import *

import matplotlib.pyplot as plt
import sys

from typing import List, Tuple

__all__ = [
    "plot_setup",
    "plot_phases",
    "plot_all_phases",
    "plot_rep_messages",
    "plot_cyc_messages",
    "plot_z",
    "plot_t_w"
]


def set_rcparams(params):
    f = plt.figure()
    plt.plot()
    plt.close(f)
    plt.rcParams.update(**params)


def plot_setup(entities: List[Entity], **options) -> Tuple[plt.Figure, plt.Axes]:
    """
    Sets up the plot.

    Args:
        entities  (List[Entity])  : The entities involved.
        width     (int, optional) : The width of the graph. Defaults to 24.
        height    (int, optional) : The height of the graph. Defaults to 4.
        fontsize (int, optional) : The font size for the graph's texts. Defaults to 22.

    Returns:
        Tuple[Figure, Axes] : A pair of figure and axes, for filling the graph.
    """
    width = options['width'] if 'width' in options else 24
    height = options['height'] if 'height' in options else 4
    fontsize = options['fontsize'] if 'fontsize' in options else 22
    dpi = options['dpi'] if 'dpi' in options else 300

    # Increase all fonts.
    set_rcparams({'font.size': fontsize, 'figure.dpi': dpi, 'savefig.dpi': dpi})

    # Create figure and plot a stem plot with the date
    fig, ax = plt.subplots(figsize=(width, height))
    # Get the last time instant.
    t_max = math.ceil(get_time_max(entities))
    # Set the X-Axis ticks.
    plt.xticks(range(0, t_max))
    # Set the X-Axis limits.
    ax.set_xlim([0, t_max])
    # Set the Y-Axis limits.
    ax.set_ylim([0, len(entities)])
    # Hide the Y-Axis.
    ax.yaxis.set_visible(False)
    # Set the axis label.
    ax.set_xlabel('Time (ms)')

    # Add the entities name.
    for yindex, entity in enumerate(entities):
        ax.text(0, ((yindex + 0) + (yindex + 1)) * 0.5, entity.name, ha='right', va='center', rotation=90, fontstyle='italic', color="gray")

    return [fig, ax]


def plot_phase(ax: plt.Axes, x0: float, x1: float, y0: float, y1: float, name: str, fill: str) -> None:
    """Plots a single phase.

    Args:
        ax   (plt.Axes) : The axes.
        x0   (float)    : The starting x coordinate.
        x1   (float)    : The ending x coordinate.
        y0   (float)    : The starting y coordinate.
        y1   (float)    : The ending y coordinate.
        name (str)      : The name of the phase.
        fill (str)      : The fill color for the phase.
    """
    # First, add the line at the beginning of the phase.
    plt.vlines(x=x0, ymin=y0, ymax=y1, color='k', linewidth=1.25)
    # Fill the entire area of the phase.
    draw_fill(ax, x0, x1, y0, y1, fill)
    # Add the name.
    ax.text((x0 + x1) * 0.5, (y0 + y1) * 0.5, name, ha='center', va='center', rotation=-20, fontstyle='italic', color="gray")


def plot_phases(ax: plt.Axes, entity: Entity, yindex: int, palette: List[str]) -> None:
    """Plots the SOME/IP phases for the given entity.

    Args:
        ax      (Axes)      : The axes.
        entity  (Entity)    : The entity of which we want to plot the phases.
        yindex  (int)       : The index of the entity on the y axis.
        palette (List[str]) : The palette we use to color each phase.
    """
    # Service goes up, client goes down.
    # Plot the phases.
    for phase, fill in zip(entity.phases, palette):
        plot_phase(ax, phase.start, phase.end, (yindex + 0), (yindex + 1), phase.label, fill)


def plot_all_phases(ax: plt.Axes, entities: List[Entity], palette: List[str]) -> None:
    """Plots the SOME/IP phases for all the entities in the list.

    Args:
        ax       (Axes)         : The axes.
        entities (List[Entity]) : The list of entities.
        palette (List[str])     : The palette we use to color each phase.
    """
    for yindex, entity in enumerate(entities):
        plot_phases(ax, entity, yindex, palette)


def plot_rep_messages(ax: plt.Axes, source: Entity, target: Entity, t_c: float, **options) -> None:
    """
    Plots repetition messages.

    Args:
        fig           (Figure)         : The figure where we plot the messages.
        ax            (Axes)           : The axes.
        source        (Entity)         : The source entity.
        target        (Entity)         : The target entity.
        t_c           (float)          : The communication delay.
    """
    if isinstance(source, Client) and not source.find_mode:
        return
    if isinstance(source, Service) and not source.offer_mode:
        return
    plot_index = options['plot_index'] if 'plot_index' in options else False
    plot_first = options['plot_first'] if 'plot_first' in options else True
    stop_at_first = options['stop_at_first'] if 'stop_at_first' in options else True
    plot_answer = options['plot_answer'] if 'plot_answer' in options else True
    hit_color = options['hit_color'] if 'hit_color' in options else 'b'
    miss_color = options['miss_color'] if 'miss_color' in options else 'r'

    # Service goes up, client goes down.
    ysrc = (1 if isinstance(source, Service) else 0)
    ydst = (0 if isinstance(source, Service) else 1)

    # Plot the Repetition Phase messages.
    for i in range(0, len(source.rep_times)):
        if (i == 0) and not plot_first:
            continue

        # The x coordinate is the time.
        x = source.rep_times[i]

        # Check if the message successfully reaches the target.
        if isinstance(source, Client) and isinstance(target, Service):
            success = ((x + t_c) >= (target.t_init))
        elif isinstance(source, Service) and isinstance(target, Client):
            success = ((x + t_c) >= (target.boot_del))
        else:
            sys.exit("Wrong pair of entities.")

        # Add the number.
        if (i > 0) and plot_index:
            ax.annotate("%s" % (ordinal(i)), xy=(x, ysrc), xytext=(x, ysrc), ha='right', va='bottom')

        # Draw the forward arrow.
        if success:
            draw_arrow(ax, x, x + t_c, ysrc, ydst, hit_color, arrowstyle="->", linewidth=3, linestyle="-")
        else:
            draw_arrow(ax, x, x + t_c, ysrc, ydst, miss_color, arrowstyle="-", linewidth=3, linestyle="--")

        # Add the answer, if the outgoing messages was successful.
        if isinstance(source, Client) and isinstance(target, Service) and success and plot_answer:
            # Get the time when the message is received from the service.
            x1 = x + t_c
            # Add a band representing the answer delay.
            draw_middle_band(ax, x1, x1 + target.ans_del, 0.02, color=hit_color)

            # Update the time when the answer is received by the client.
            x1 = x + t_c + target.ans_del
            # Add the answer.
            draw_arrow(ax, x1, x1 + t_c, ydst, ysrc, hit_color)

        # Let us stop at the first successfully sent message.
        if stop_at_first and success:
            break


def plot_cyc_messages(ax: plt.Axes, s: Service, c: Client, t_c: float, **options) -> None:
    """
    Plots cyclic messages, those sent during the main phase by the Service.

    Args:
        fig           (Figure)         : The figure where we plot the messages.
        ax            (Axes)           : The axes.
        s             (Service)        : The service.
        c             (Client)         : The client.
        t_c           (float)          : The communication delay.
        stop_at_first (bool, optional) : We stop at the first successfully received message. Defaults to True.
    """
    if not s.offer_mode:
        return
    plot_index = options['plot_index'] if 'plot_index' in options else False
    stop_at_first = options['stop_at_first'] if 'stop_at_first' in options else True
    arrival_time = options['arrival_time'] if 'arrival_time' in options else True
    hit_color = options['hit_color'] if 'hit_color' in options else 'b'
    miss_color = options['miss_color'] if 'miss_color' in options else 'r'

    if not isinstance(s, Service) or not isinstance(c, Client):
        sys.exit("Only services have cyclic messages during the Main Phase")

    # Compute the number of cyclic messages we can display.
    num_cyc = math.floor((s.phases[-1].end - s.phases[2].end) / s.cyc_del)

    for i in range(1, num_cyc):
        # The x coordinate is the time.
        x = s.phases[2].end + (i * s.cyc_del)
        # Check if the message successfully reaches the target.
        success = ((x + t_c) >= (c.boot_del))
        # Add the number.
        if plot_index:
            ax.annotate("%s" % (ordinal(i)), xy=(x, 1), xytext=(x, 1), ha='left', va='bottom')

        # Plot the message lines.
        if success:
            ax.annotate("", xytext=(x, 1), xy=(x + t_c, 0), arrowprops=dict(arrowstyle="->", linewidth=3, linestyle="-", color=hit_color))
            # If the message is successfully received by the client, add the arrival time.
            if arrival_time:
                ax.annotate("%d" % (x + t_c), xy=(x + t_c, 0), xytext=(x + t_c, 0), ha='center', va='top')
        else:
            plt.plot([x, x + t_c], [1, 0.0], linewidth=3, linestyle="--", dashes=(5, 5), color=miss_color)

        # Let us stop at the first successfully sent message.
        if stop_at_first and success:
            break


def plot_z(ax: plt.Axes, s: Service, c: Client, **options):
    """
    Plots the Z band in red.

    Args:
        fig (Figure)  : The figure where we plot the messages.
        ax  (Axes)    : The axes.
        s   (Service) : The service.
        c   (Client)  : The client.
    """
    # If the service is faster than the client.
    plt.rcParams['hatch.linewidth'] = 8
    if s.t_init < c.t_init:
        draw_middle_band(ax, c.phases[1].start, s.phases[2].start, 0.02, color='red', hatchwidth=8)
    elif s.t_init > c.t_init:
        draw_middle_band(ax, c.phases[2].start, s.phases[2].start, 0.02, color='red', hatchwidth=8)


def plot_t_w(t_w: float, **options):
    """
    Plots the start-up delay.

    Args:
        fig (Figure)  : The figure where we plot the messages.
        ax  (Axes)    : The axes.
        t_w (float)   : The start-up delay value.
    """
    color = options['color'] if 'color' in options else 'purple'
    label = options['label'] if 'label' in options else ''
    ha = options['ha'] if 'ha' in options else 'right'
    va = options['va'] if 'va' in options else 'top'
    fontsize = options['fontsize'] if 'fontsize' in options else 22

    plt.axvline(x=t_w, ls='--', color=color, linewidth=3, dashes=(5, 5))
    if ha == "left":
        t_w += 0.1
    if label:
        plt.text(t_w, 1.975, label, ha=ha, va=va, rotation=0, fontsize=fontsize)

"""
Timing analysis functions, as found in:
    J. R. Seyler, T. Streichert, M. Glaß, N. Navet and J. Teich, "Formal analysis of
    the startup delay of SOME/IP service discovery," 2015 Design, Automation & Test
    in Europe Conference & Exhibition (DATE), Grenoble, France, 2015, pp. 49-54,
    doi: 10.7873/DATE.2015.0469.
"""

from timing.entities import *
from timing.support import *

import math
import sys

__logger = create_logger("timing_ssg15")


def set_logger_level(level: int):
    __logger.setLevel(level)


def compute_z_s(s: Service, c: Client) -> float:
    """
    Computes the Z value, when the Client enters Repetition Phase before Service.

    Args:
        s (Service) : the service.
        c (Client)  : the client.

    Returns:
        float: the Z value, based on the scenario.
    """
    # Compute the result.
    result = s.t_init - c.t_init
    # Debug output and return.
    __logger.debug("compute_z_s(s.t_init: %.2f, c.t_init: %.2f) -> %.2f" % (s.t_init, c.t_init, result))
    return result


def compute_z_c(s: Service, c: Client) -> float:
    """
    Computes the Z value, when the Service enters Repetition Phase before Client.

    Args:
        s (Service) : the service.
        c (Client)  : the client.

    Returns:
        float: the Z value, based on the scenario.
    """
    # Compute the result.
    result = c.boot_del - s.t_init
    # Debug output and return.
    __logger.debug("compute_z_c(c.boot_del: %.2f, s.t_init: %.2f) -> %.2f" % (c.boot_del, s.t_init, result))
    return result


def compute_x_s(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the X value, when the Client enters Repetition Phase before Service.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already received find (X_s) messages within the Repetition Phase.
    """
    # First, compute z_s.
    z_s = compute_z_s(s, c)
    # Compute the result. In the paper they do not specify the check I'm doing
    # here, but if I do not do it, we will encounter plenty of `math domain
    # error`.
    result = math.ceil(math.log2(((z_s - t_c) / c.rep_del) + 1)) - 1 if (z_s > t_c) else 0
    # Debug output and return.
    __logger.debug("compute_x_s(z_s: %.2f, t_c: %.2f, c.rep_del: %.2f) -> %d" % (z_s, t_c, c.rep_del, result))
    return result


def compute_x_c(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the X value, when the Service enters Repetition Phase before Client.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already received offer (X_c) messages within the Repetition Phase.
    """
    # First, compute z_c.
    z_c = compute_z_c(s, c)
    # Compute the result. In the paper they do not specify the check I'm doing
    # here, but if I do not do it, we will encounter plenty of `math domain
    # error`.
    result = math.ceil(math.log2(((z_c - t_c) / s.rep_del) + 1)) - 1 if (z_c > t_c) else 0
    # Debug output and return.
    __logger.debug("compute_x_c(z_c: %.2f, t_c: %.2f, s.rep_del: %.2f) -> %d" % (z_c, t_c, s.rep_del, result))
    return result


def compute_y(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the Y value, which is the number of already sent period messages in
    the Main Phase.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already sent period messages in the Main Phase.
    """
    # First, compute z_c.
    z_c = compute_z_c(s, c)
    # Finally, compute the result.
    result = math.ceil((z_c - t_c - (math.pow(2, s.rep_max + 1) - 1) * s.rep_del) / s.cyc_del)
    # Debug output and return.
    __logger.debug("compute_y(z_c: %.2f, t_c: %.2f, s.rep_max: %.2f, s.rep_del: %.2f, s.cyc_del: %.2f) -> %d" %
                   (z_c, t_c, s.rep_max, s.rep_del, s.cyc_del, result))
    return result


def compute_x_c_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(X) value.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already received find (X_s) or offer (X_c) messages
             within the Repetition Phase.
    """
    # First, compute x_c.
    x_c = compute_x_c(s, c, t_c)
    # Compute the result (could be simplified to `min(s.rep_max, x_c)`).
    result = x_c if (x_c <= s.rep_max) else s.rep_max
    # Debug output and return.
    __logger.debug("compute_x_c_hat(s.rep_max: %d, x_c: %d) -> %d" % (s.rep_max, x_c, result))
    return result


def compute_x_s_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(X) value.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already received find (X_s) or offer (X_c) messages
             within the Repetition Phase.
    """
    # First, compute x_s.
    x_s = compute_x_s(s, c, t_c)
    # Compute the result (could be simplified to `min(c.rep_max, x_s)`).
    result = x_s if (x_s <= c.rep_max) else c.rep_max
    # Debug output and return.
    __logger.debug("compute_x_s_hat(c.rep_max: %d, x_s: %d) -> %d" % (c.rep_max, x_s, result))
    return result


def compute_y_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(Y) value.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        int: the number of already sent period messages in the Main Phase.
    """
    # First, compute y.
    y = compute_y(s, c, t_c)
    # Then, compute x_c_hat.
    x_c_hat = compute_x_c_hat(s, c, t_c)
    # Compute the result.
    result = 0 if (x_c_hat <= s.rep_max) else y
    # Debug output and return.
    __logger.debug("compute_y_hat(y: %d, x_c: %d) -> %d" % (y, x_c_hat, result))
    return result


def timing_analysis_a(s: Service, c: Client, t_c: float) -> float:
    """
    Service in Offer Mode and Client in Request Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        float: the discovery timespan.
    """

    # (A1) Client is faster than Service.
    if (s.t_init + t_c) >= c.boot_del:
        # First, we compute z_s.
        z_s = compute_z_s(s, c)
        # Compute the result.
        result = z_s + c.init_del + t_c
        # Debug output and return.
        __logger.debug("timing_analysis_a1(z_s: %.2f, c.init_del: %.2f, t_c: %.2f) -> %.2f" % (z_s, c.init_del, t_c, result))
        return result
    # (A2) Service is faster than Client.
    # First, we compute x_hat, y_hat, and z_c.
    x_hat = compute_x_c_hat(s, c, t_c)
    y_hat = compute_y_hat(s, c, t_c)
    z_c = compute_z_c(s, c)
    # Then, we compute what should actually be the length of the repetition phase.
    t_rep = (math.pow(2, x_hat + 1) - 1) * s.rep_del
    # Then, we compute what appears to be the length of the main phase.
    t_cyc = y_hat * s.cyc_del
    # Compute the result.
    result = min(t_rep + t_cyc + t_c - z_c, c.init_del + 2 * t_c + s.ans_del)
    # Debug output and return.
    __logger.debug("timing_analysis_a2(x: %d, y: %d, z_c: %.2f, s.rep_del: %.2f, s.cyc_del: %.2f, s.ans_del: %.2f, t_c: %.2f) -> %.2f" % (
        x_hat, y_hat, z_c, s.rep_del, s.cyc_del, s.ans_del, t_c, result))
    return result


def timing_analysis_b(s: Service, c: Client, t_c: float) -> float:
    """
    Service in Offer Mode and Client in Listen Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        float: the discovery timespan.
    """
    # First, we compute x_hat, y_hat, and z_c.
    x_hat = compute_x_c_hat(s, c, t_c)
    y_hat = compute_y_hat(s, c, t_c)
    z_c = compute_z_c(s, c)
    # Then, we compute what should actually be the length of the repetition phase.
    t_rep = (pow(2, x_hat + 1) - 1) * s.rep_del
    # Then, we compute what appears to be the length of the main phase.
    t_cyc = y_hat * s.cyc_del
    # Compute the result.
    result = t_rep + t_cyc + t_c - z_c
    # Debug output and return.
    __logger.debug("timing_analysis_b(x: %d, y: %d, z_c: %.2f, s.rep_del: %.2f, s.cyc_del: %.2f, s.ans_del: %.2f, t_c: %.2f) -> %.2f" % (
        x_hat, y_hat, z_c, s.rep_del, s.cyc_del, s.ans_del, t_c, result))
    return result


def timing_analysis_c(s: Service, c: Client, t_c: float) -> float:
    """
    Service in Silent Mode and Client in Request Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        float: the discovery timespan.
    """
    # (C1) Service is faster than Client.
    if (c.t_init + t_c) >= s.t_init:
        # Compute the result.
        result = c.init_del + 2 * t_c + s.ans_del
        # Debug output and return.
        __logger.debug("timing_analysis_c1(c.init_del: %.2f, s.ans_del: %.2f, t_c:%.2f) -> %.2f" % (c.init_del, s.ans_del, t_c, result))
        return result
    # (C2) Client is faster than Service.
    # First, we compute x_s.
    x_s = compute_x_s(s, c, t_c)
    # Then, we compute what should actually be the length of the repetition phase.
    t_rep = (math.pow(2, x_s + 1) - 1) * c.rep_del
    # Compute the result.
    result = c.t_init - c.boot_del + t_rep + t_c + s.ans_del + t_c
    # Debug output and return.
    __logger.debug("timing_analysis_c2(x_s: %d, t_rep: %.2f, c.t_init: %.2f, c.boot_del: %.2f, s.ans_del: %.2f, t_c: %.2f) -> %.2f" % (
        x_s, t_rep, c.t_init, c.boot_del, s.ans_del, t_c, result))
    return result


def timing_analysis(s: Service, c: Client, t_c: float) -> float:
    """
    Computes the timespan that a client running on a node needs to find the
    service to which it wants to subscribe to.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        float: the discovery timespan.
    """
    # Service in Offer Mode and Client in Request Mode
    if s.offer_mode and c.find_mode:
        __logger.debug("(a) Service in Offer Mode and Client in Request Mode")
        return timing_analysis_a(s, c, t_c)

    # Service in Offer Mode and Client in Listen Mode
    if s.offer_mode and not c.find_mode:
        __logger.debug("(b) Service in Offer Mode and Client in Listen Mode")
        return timing_analysis_b(s, c, t_c)

    # Service in Silent Mode and Client in Request Mode
    if not s.offer_mode and c.find_mode:
        __logger.debug("(c) Service in Silent Mode and Client in Request Mode")
        return timing_analysis_c(s, c, t_c)

    # Check that at least one of them is active.
    sys.exit("Either service or client must be active (sending find/offer messages)")

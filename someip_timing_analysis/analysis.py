"""
Timing analysis functions.
"""

from .entities import *
from .logger import *

import math
import sys

__logger = create_logger("timing")


def set_logger_level(level: int):
    __logger.setLevel(level)


def compute_t_rep(e: Entity, x: int) -> float:
    """
    Computes the timespan from the start of the Repetition Phase up to when the
    x-th message is sent. This does not take into account the communication
    delay.

    Args:
        e   (Entity) : The entity involved.
        x   (int)    : The number of already sent messages.
    Returns:
        float : Timespan from the start of the Repetition Phase up to when the
                x-th message is sent.
    """
    # Compute the result.
    result = (math.pow(2, x) - 1) * e.rep_del
    # Debug output and return.
    __logger.debug("compute_t_rep(e.rep_del: %.2f, x: %d) -> %.2f" % (e.rep_del, x, result))
    return result


def compute_t_cyc(s: Service, y: int) -> float:
    """
    Computes the timespan from the start of the Repetition Phase up to when the
    Y-th message is sent. This does not take into account the communication
    delay.

    Args:
        s   (Service) : The service involved.
        x   (int)     : The number of already sent messages during the Repetition Phase.
        y   (int)     : The number of already sent messages during the Main Phase.
    Returns:
        float : Timespan from the start of the Main Phase up to when the y-th
                message is sent.
    """
    # Check that we are dealing with a Service.
    assert isinstance(s, Service)
    # Compute the result.
    result = y * s.cyc_del
    # Debug output and return.
    __logger.debug("compute_t_cyc(s.cyc_del: %.2f, y: %d) -> %.2f" % (s.cyc_del, y, result))
    return result


def compute_z_s(s: Service, c: Client) -> float:
    """
    Computes the Z value, when the Client enters Repetition Phase before Service.

    Args:
        s (Service) : the service.
        c (Client)  : the client.
    Returns:
        float: the Z value, based on the scenario.
    """
    # Compute the result, and avoid producing a negative value.
    result = (s.t_init - c.t_init) if (s.t_init > c.t_init) else 0
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
    # Compute the result, and avoid producing a negative value.
    result = (c.boot_del - s.t_init) if (s.t_init < c.boot_del) else 0
    # Debug output and return.
    __logger.debug("compute_z_c(c.boot_del: %.2f, s.t_init: %.2f) -> %.2f" % (c.boot_del, s.t_init, result))
    return result


def compute_x_s(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the x value, when the Client enters Repetition Phase before Service.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.
    Returns:
        int: the number of already received find (X_s) messages within the Repetition Phase.
    """
    # First, compute z_s.
    z_s = compute_z_s(s, c)
    # Compute the result, and avoid producing a negative value.
    result = math.ceil(math.log2(((z_s - t_c) / c.rep_del) + 1)) if (z_s > t_c) else 0
    # Debug output and return.
    __logger.debug("compute_x_s(z_s: %.2f, t_c: %.2f, c.rep_del: %.2f) -> %d" % (z_s, t_c, c.rep_del, result))
    return result


def compute_x_c(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the x value, when the Service enters Repetition Phase before Client.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.
    Returns:
        int: the number of already received offer (X_c) messages within the Repetition Phase.
    """
    # First, compute z_c.
    z_c = compute_z_c(s, c)
    # Compute the result, and avoid producing a negative value.
    result = math.ceil(math.log2(((z_c - t_c) / s.rep_del) + 1)) if (z_c > t_c) else 0
    # Debug output and return.
    __logger.debug("compute_x_c(z_c: %.2f, t_c: %.2f, s.rep_del: %.2f) -> %d" % (z_c, t_c, s.rep_del, result))
    return result


def compute_x_s_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(x) value.

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
    # Compute the result.
    result = min(c.rep_max, x_s)
    # Debug output and return.
    __logger.debug("compute_x_s_hat(c.rep_max: %d, x_s: %d) -> %d" % (c.rep_max, x_s, result))
    return result


def compute_x_c_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(x) value.

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
    # Compute the result.
    result = min(s.rep_max, x_c)
    # Debug output and return.
    __logger.debug("compute_x_c_hat(s.rep_max: %d, x_c: %d) -> %d" % (s.rep_max, x_c, result))
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
    # Then, compute the length of the Repetition Phase.
    t_rep = compute_t_rep(s, s.rep_max)
    # Finally, compute the result.
    result = math.ceil((z_c - t_c - t_rep) / s.cyc_del)
    # Debug output and return.
    __logger.debug("compute_y(z_c: %.2f, t_c: %.2f, t_rep: %.2f, s.cyc_del: %.2f) -> %d" %
                   (z_c, t_c, t_rep, s.cyc_del, result))
    return result


def compute_y_hat(s: Service, c: Client, t_c: float) -> int:
    """
    Computes the hat(y) value.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.
    Returns:
        int: the number of already received find (X_s) or offer (X_c) messages
             within the Repetition Phase.
    """
    # First, compute y.
    y = compute_y(s, c, t_c)
    # Then, compute x_c_hat.
    x_c_hat = compute_x_c_hat(s, c, t_c)
    # Finally, compute the result.
    result = y if ((y >= 0) and (x_c_hat >= s.rep_max)) else 0
    # Debug output and return.
    __logger.debug("compute_y_hat(y: %d, x_c_hat: %d) -> %d" % (y, x_c_hat, result))
    return result


def timing_analysis_a(s: Service, c: Client, t_c: float) -> float:
    """
    Computes the timespan that a client running on a node needs to find the
    service to which it wants to subscribe to. The case it covers is that of
    Service in Offer Mode and Client in Listen Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.

    Returns:
        float: the discovery timespan.
    """
    # Compute x_c.
    x_c = compute_x_c_hat(s, c, t_c)
    # Compute the lenght of the Repetition Phase, up to the x_c-th message.
    t_rep = compute_t_rep(s, x_c)
    # Copmute the number of messages sent in the Main Phase, might be zero.
    y = compute_y_hat(s, c, t_c)
    # Based on y, copmute the amount of time spent in the Main Phase, might be
    # zero.
    t_cyc = compute_t_cyc(s, y)
    # Compute the result.
    result = s.t_init + t_rep + t_cyc + t_c
    # Debug output and return.
    __logger.debug("timing_analysis_a(s.t_init: %.2f, t_rep: %.2f, t_cyc: %.2f, t_c: %.2f) -> %.2f" %
                   (s.t_init, t_rep, t_cyc, t_c, result))
    return result


def timing_analysis_b(s: Service, c: Client, t_c: float) -> float:
    """
    Computes the timespan that a client running on a node needs to find the
    service to which it wants to subscribe to. The case it covers is that of
    Service in Silent Mode and Client in Request Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.
    Returns:
        float: the discovery timespan.
    """
    # Compute x_s.
    x_s = compute_x_s_hat(s, c, t_c)
    # Compute the lenght of the Repetition Phase, up to the x_s-th message.
    t_rep = compute_t_rep(c, x_s)
    # Compute the result.
    result = c.t_init + t_rep + t_c + s.ans_del + t_c
    # Debug output and return.
    __logger.debug("timing_analysis_b(c.t_init: %.2f, t_rep: %.2f, t_c: %.2f, s.ans_del: %.2f, t_c: %.2f) -> %.2f" %
                   (c.t_init, t_rep, t_c, s.ans_del, t_c, result))
    return result


def timing_analysis_c(s: Service, c: Client, t_c: float) -> float:
    """
    Computes the timespan that a client running on a node needs to find the
    service to which it wants to subscribe to. The case it covers is that of
    Service in Offer Mode and Client in Request Mode.

    Args:
        s   (Service) : the service.
        c   (Client)  : the client.
        t_c (float)   : the communication delay.
    Returns:
        float: the discovery timespan.
    """
    # Compute the timing analysis for Case A.
    timing_a = timing_analysis_a(s, c, t_c)
    # Compute the timing analysis for Case B.
    timing_b = timing_analysis_b(s, c, t_c)
    # Compute the result.
    result = min(timing_a, timing_b)
    # Debug output and return.
    __logger.debug("timing_analysis_c(timing_a: %.2f, timing_b: %.2f) -> %.2f" %
                   (timing_a, timing_b, result))
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
    # Service in Offer Mode and Client in Listen Mode
    if s.offer_mode and not c.find_mode:
        __logger.info(f"(a) Service in Offer Mode and Client in Listen Mode")
        return timing_analysis_a(s, c, t_c)
    # Service in Silent Mode and Client in Request Mode
    if not s.offer_mode and c.find_mode:
        __logger.info(f"(b) Service in Silent Mode and Client in Request Mode")
        return timing_analysis_b(s, c, t_c)
    # Service in Offer Mode and Client in Request Mode
    if s.offer_mode and c.find_mode:
        __logger.info(f"(c) Service in Offer Mode and Client in Request Mode")
        return timing_analysis_c(s, c, t_c)
    # Check that at least one of them is active.
    sys.exit("Either service or client must be active (sending find/offer messages)")


def timing_analysis_system(system: System) -> float:
    """Computes the timespan that a set of clients on a note node needs to find the
    service to which it wants to subscribe to.

    Args:
        system (System): The list of client/service pairs composing the system.

    Returns:
        float: the discovery time for the entire system.
    """
    return max([timing_analysis(entry.service, entry.client, entry.t_c) for entry in system.relations])

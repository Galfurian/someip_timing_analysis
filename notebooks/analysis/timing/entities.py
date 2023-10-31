"""
SOME/IP entities definition.
"""

import math
import json

from typing import List


class Phase(object):
    """
    Represents a SOME/IP phase (e.g., Boot, InitalWait, Repetition, etc.).

    Parameters:
        start    (float) : The time when the phase starts.
        end      (float) : The time when the phase ends.
        duration (float) : The duration of the phase.
        label    (str)   : The lable identifying the phase.
    """
    start: float
    end: float
    duration: float
    label: str

    def __init__(self, start: float, duration: float, label: str) -> None:
        """
        The constructor for SOME/IP phases.

        Args:
            start    (float): The starting instant of the phase.
            duration (float): The duration of the phase.
            label    (str)  : The lable identifying the phase.
        """
        self.start = start
        self.end = start + duration
        self.duration = duration
        self.label = label

    def __repr__(self) -> str:
        """
        Transforms the Phase into a string.

        Returns:
            str: the Phase to string.
        """
        return "<%.2f,%.2f,%s>" % (self.start, self.end, self.label)


class Entity(object):
    """
    Represents either a Client or a Service.

    Parameters:
        name       (str)         : The name of the entity.
        boot_del   (float)       : The boot delay.
        init_del   (float)       : The initial wait phase delay.
        rep_del    (float)       : The repetition phase delay.
        rep_max    (int)         : The maximum number of messages sent in the repetition phase.
        t_init     (float)       : The sum of boot and initial delays.
        phases     (List[Phase]) : The list of phases.
        rep_times  (List[float]) : The instants when messages are sents in the Repetition Phase.
    """
    name: str
    boot_del: float
    init_del: float
    rep_del: float
    rep_max: int
    t_init: float
    phases: List[Phase]
    rep_times: List[float]

    def __init__(self, name: str, boot_del: float, init_del: float, rep_del: float, rep_max: int):
        """
        The constructor for SOME/IP entities.

        Args:
            name     (str)   : The name of the entity.
            boot_del (float) : The boot delay.
            init_del (float) : The initial wait phase delay.
            rep_del  (float) : The repetition phase delay.
            rep_max  (int)   : The maximum number of messages sent in the repetition phase.
        """
        self.name = name
        self.boot_del = boot_del
        self.init_del = init_del
        self.rep_del = rep_del
        self.rep_max = rep_max
        self.t_init = self.boot_del + self.init_del
        # Generate the phases.
        # [0] Boot Phase
        self.phases = []
        self.phases.append(Phase(0, boot_del, "Boot"))
        # [1] Initial Wait Phase
        self.phases.append(Phase(self.phases[-1].end, init_del, "Initial"))
        # [2] Repetition Phase
        self.phases.append(Phase(self.phases[-1].end, sum(math.pow(2, i) * rep_del for i in range(0, rep_max)), "Repetition"))
        # [3] Main Phase
        self.phases.append(Phase(self.phases[-1].end, 1, "Main"))
        # Compute the time instants when the repetition messages are sent.
        self.rep_times = []
        # Actually, this is the one sent at the end of the Initial Wait Phase.
        self.rep_times.append(self.boot_del + self.init_del)
        # Then, the other are sent.
        for i in range(0, self.rep_max):
            self.rep_times.append(self.rep_times[-1] + pow(2, i) * self.rep_del)

    def __repr__(self) -> str:
        """
        Transforms the entity into a string.

        Returns:
            str: the entity to string.
        """
        return self.name


class Client(Entity):
    """
    Represents a client.

    Parameters:
        find_mode  (bool)        : If the client is activelly sending find messages.

    Parameters (inherited):
        name       (str)         : The name of the entity.
        boot_del   (float)       : The boot delay.
        init_del   (float)       : The initial wait phase delay.
        rep_del    (float)       : The repetition phase delay.
        rep_max    (int)         : The maximum number of messages sent in the repetition phase.
        t_init     (float)       : The sum of boot and initial delays.
        phases     (List[Phase]) : The list of phases.
        rep_times  (List[float]) : The instants when messages are sents in the Repetition Phase.
    """
    find_mode: bool

    def __init__(self, name: str, boot_del: float, init_del: float, rep_del: float, rep_max: int, find_mode: bool):
        """
        The constructor for SOME/IP clients.

        Args:
            boot_del  (float) : The boot delay.
            init_del  (float) : The initial wait phase delay.
            rep_del   (float) : The repetition phase delay.
            rep_max   (int)   : The maximum number of messages sent in the repetition phase.
            find_mode (bool)  : If the client is activelly sending find messages.
        """
        Entity.__init__(self, name, boot_del, init_del, rep_del, rep_max)
        # The client is actively searching for a service.
        self.find_mode = find_mode


class Service(Entity):
    """
    Represents a service.

    Parameters:
        cyc_del    (float)       : The delay between offer messages in the Main Phase.
        ans_del    (float)       : The answer delay.
        offer_mode (bool)        : If the service is activelly sending offer messages.

    Parameters (inherited):
        name       (str)         : The name of the entity.
        boot_del   (float)       : The boot delay.
        init_del   (float)       : The initial wait phase delay.
        rep_del    (float)       : The repetition phase delay.
        rep_max    (int)         : The maximum number of messages sent in the repetition phase.
        t_init     (float)       : The sum of boot and initial delays.
        phases     (List[Phase]) : The list of phases.
        rep_times  (List[float]) : The instants when messages are sents in the Repetition Phase.
    """
    cyc_del: float
    ans_del: float
    offer_mode: bool

    def __init__(self, name: str, boot_del: float, init_del: float, rep_del: float, rep_max: int, cyc_del: float, ans_del: float, offer_mode: bool):
        """
        The constructor for SOME/IP services.

        Args:
            boot_del   (float)  : The boot delay.
            init_del   (float)  : The initial wait phase delay.
            rep_del    (float)  : The repetition phase delay.
            rep_max    (int)    : The maximum number of messages sent in the repetition phase.
            cyc_del    (float)  : The period with which a service send offer message in the main phase.
            ans_del    (float)  : The delay between when a find message is received and the answer is sent back.
            offer_mode (bool)   : If the service is activelly sending offer messages.
        """
        Entity.__init__(self, name, boot_del, init_del, rep_del, rep_max)

        # Service specific variables.
        self.cyc_del = cyc_del
        self.ans_del = ans_del
        self.offer_mode = offer_mode


class Relation:
    """Keeps track of which service serve which client.

    Parameters:
        client  (Client)    : The client which requires a given service.
        service (Service)   : The specific service the client requests.
        t_c     (float)     : The communication delay specific of a client/service pair.
    """
    client: Client
    service: Service
    t_c: float

    def __init__(self, client: Client, service: Service, t_c: float) -> None:
        self.client = client
        self.service = service
        self.t_c = t_c

    def __repr__(self) -> str:
        """
        Transforms the relation into a string.

        Returns:
            str: the relation to string.
        """
        return "<%s,%s,%.2f>" % (str(self.client), str(self.service), self.t_c)


class EntitiesEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class EntitiesDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        if 'offer_mode' in d:
            return Service(d['name'], d['boot_del'], d['init_del'], d['rep_del'], d['rep_max'], d['cyc_del'], d['ans_del'], d['offer_mode'])
        elif 'find_mode' in d:
            return Client(d['name'], d['boot_del'], d['init_del'], d['rep_del'], d['rep_max'], d['find_mode'])
        elif ('client' in d) and ('service' in d) and ('t_c' in d):
            return Relation(EntitiesDecoder().decode(d['client']), EntitiesDecoder().decode(d['service']), d['t_c'])
        return d


def get_time_max(entities: List[Entity]) -> float:
    """
    Returns the larger phase ending time of all the entities.

    Args:
        entities (List[Entity]) : The list of entities.
    Returns:
        float: the maximum lenght of all phases.
    """
    return max([entity.phases[-1].end for entity in entities])


def adjust_phases(entities: List[Entity]):
    """
    Sets the same end of the Main Phase for all the enties.

    Args:
        entities (List[Entity]) : The list of entities.
    """
    # Compute the max.
    phase_max = get_time_max(entities)
    # Adjust the phases.
    for entity in entities:
        entity.phases[-1].end = phase_max

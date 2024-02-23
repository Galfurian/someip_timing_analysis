from typing import List
from typing import Any
from dataclasses import dataclass

import json


@dataclass
class Endpoint:
    """Endpoint details.

    Attributes
    ----------
    address : str
        Endpoint address.

    port: str
        Endpoint port.
    """
    address: str
    port: str

    @staticmethod
    def from_dict(obj: Any) -> 'Endpoint':
        _address = str(obj.get("address", "0.0.0.0"))
        _port = str(obj.get("port", "0"))
        return Endpoint(_address, _port)


@dataclass
class File:
    """File description.

    Attributes
    ----------
    enable: str
        Specifies whether a log file should be created (valid values: _true,
        false_).

    path: str
        The absolute path of the log file.
    """
    enable: str
    path: str

    @staticmethod
    def from_dict(obj: Any) -> 'File':
        _enable = str(obj.get("enable", "true"))
        _path = str(obj.get("path", ""))
        return File(_enable, _path)


@dataclass
class Logging:
    """Logging configuration.

    level: str
        Specifies the log level (valid values: _trace_, _debug_, _info_,
        _warning_, _error_, _fatal_).

    console: str
        Specifies whether logging via console is enabled (valid values: _true,
        false_).

    file: File
        Configure file logging.

    dlt: dlt
        Specifies whether Diagnostic Log and Trace (DLT) is enabled (valid
        values: _true, false_).
    """
    level: str
    console: str
    file: File
    dlt: str

    @staticmethod
    def from_dict(obj: Any) -> 'Logging':
        _level = str(obj.get("level", "info"))
        _console = str(obj.get("console", "true"))
        _file = File.from_dict(obj.get("file", {}))
        _dlt = str(obj.get("dlt", "true"))
        return Logging(_level, _console, _file, _dlt)


class Plugin:
    """Plugin details.

    Attributes
    ---------- 
    name : str
        The name of the plug-in.

    type : str
        The plug-in type (valid values: _application_plugin_). An application
        plug-in extends the functionality on application level. It gets informed
        by vsomeip over the basic application states (INIT/START/STOP) and can,
        based on these notifications, access the standard "application"-API via
        the runtime.
    """
    name: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Plugin':
        _name = str(obj.get("name", ""))
        _type = str(obj.get("type", ""))
        return Plugin(_name, _type)


@dataclass
class Application:
    """Application of the host system.

    Attributes
    ----------
    name : str
        The name of the application.

    id : str
        The id of the application. Usually its high byte is equal to the
        diagnosis address. In this case the low byte must be different from
        zero. Thus, if the diagnosis address is 0x63, valid values range from
        0x6301 until 0x63FF. It is also possible to use id values with a high
        byte different from the diagnosis address. 

    max_dispatchers : int
        The maximum number of threads that shall be used to execute the
        application callbacks. Default is 10.

    max_dispatch_time : int
        The maximum time in ms that an application callback may consume before
        the callback is considered to be blocked (and an additional thread is
        used to execute pending callbacks if max_dispatchers is configured
        greater than 0). The default value if not specified is 100ms.

    threads : int
        The number of internal threads to process messages and events within an
        application. Valid values are 1-255. Default is 2.

    io_thread_nice : int
        The nice level for internal threads processing messages and events.
        POSIX/Linux only. For actual values refer to nice() documentation.

    request_debounce_time : int
        Specifies a debounce-time interval in ms in which request-service
        messages are sent to the routing manager. If an application requests
        many services in short same time the load of sent messages to the
        routing manager and furthermore the replies from the routing manager
        (which contains the routing info for the requested service if available)
        can be heavily reduced. The default value if not specified is 10ms.

    plugins : List[Plugin]
        Contains the plug-ins that should be loaded to extend the functionality
        of vsomeip.
    """
    name: str
    id: int
    max_dispatchers: int
    max_dispatch_time: int
    threads: int
    io_thread_nice: int
    request_debounce_time: int
    plugins: List[Plugin]

    @staticmethod
    def from_dict(obj: Any) -> 'Application':
        _name = str(obj.get("name", ""))
        _id = str(obj.get("id", -1))
        _max_dispatchers = int(obj.get("max_dispatchers", 10))
        _max_dispatch_time = int(obj.get("max_dispatchers", 100))
        _threads = int(obj.get("threads", 2))
        _io_thread_nice = int(obj.get("io_thread_nice", 0))
        _request_debounce_time = int(obj.get("request_debounce_time", 10))
        _plugins = [Plugin.from_dict(y) for y in obj.get("plugins", [])]
        return Application(_name, _id, _max_dispatchers, _max_dispatch_time, _threads, _io_thread_nice, _request_debounce_time, _plugins)


@dataclass
class Eventgroup:
    """Eventgroup configuration.

    Attributes
    ----------
    eventgroup: str
        The id of the event group.

    events: List[str]
        Contains the ids of the appropriate events.

    multicast: Endpoint
        Specifies the multicast that is used to publish the eventgroup.

    threshold: int
        Specifies when to use multicast and when to use unicast to send a
        notification event. Must be set to a non-negative number. If it is set
        to zero, all events of the eventgroup will be sent by unicast.
        Otherwise, the events will be sent by unicast as long as the number of
        subscribers is lower than the threshold and by multicast if the number
        of subscribers is greater or equal. This means, a threshold of 1 will
        lead to all events being sent by multicast. The default value is _0_.  
    """
    eventgroup: str
    events: List[str]
    multicast: Endpoint
    threshold: int

    @staticmethod
    def from_dict(obj: Any) -> 'Eventgroup':
        _eventgroup = str(obj.get("eventgroup", ""))
        _events = [str(y) for y in obj.get("events", [])]
        _multicast = Endpoint.from_dict(obj.get("multicast", {}))
        _threshold = int(obj.get("threshold", "0"))
        return Eventgroup(_eventgroup, _events, _multicast, _threshold)


@dataclass
class Client:
    """A service user.

    Attributes
    ----------
    service : str
    instance : str
        Together they specify the service instance the port configuration shall
        be applied to.

    reliable: List[int]
        The list of client ports to be used for reliable (TCP) communication to
        the given service instance. 

    unreliable: List[int]
        The list of client ports to be used for unreliable (UDP) communication
        to the given service instance. 
    """
    service: str
    instance: str
    reliable: List[int]
    unreliable: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Client':
        _service = str(obj.get("service", "0x0000"))
        _instance = str(obj.get("instance", "0x0000"))
        _reliable = [int(y) for y in obj.get("unreliable", [])]
        _unreliable = [int(y) for y in obj.get("unreliable", [])]
        return Client(_service, _instance, _reliable, _unreliable)


@dataclass
class Reliable:
    """Specifies a reliable communication.

    Attributes
    ----------
    port: str
        The port of the TCP endpoint.

    enable_magic_cookies: str
        Specifies whether magic cookies are enabled (valid values: _true_, _false_).
    """
    port: str
    enable_magic_cookies: str

    @staticmethod
    def from_dict(obj: Any) -> 'Reliable':
        _port = str(obj.get("port", "0"))
        _enable_magic_cookies = str(obj.get("enable-magic-cookies", "true"))
        return Reliable(_port, _enable_magic_cookies)


@dataclass
class Event:
    """An event.

    Attributes
    ----------
    event: str
        The id of the event.

    is_field: str
        Specifies whether the event is of type field. NOTE: A field is a
        combination of getter, setter and notification event. It contains at
        least a getter, a setter, or a notifier. The notifier sends an event
        message that transports the current value of a field on change.

    update_cycle: int
        Specifies whether the communication is reliable respectively whether the
        event is sent with the TCP protocol (valid values: _true_,_false_). If
        the value is _false_ the UDP protocol will be used.
    """
    event: str
    is_field: str
    update_cycle: int

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        _event = str(obj.get("event", ""))
        _is_field = str(obj.get("is_field", "true"))
        _update_cycle = int(obj.get("update-cycle", "0"))
        return Event(_event, _is_field, _update_cycle)


@dataclass
class Service:
    """Details of a service provider.

    Attributes
    ----------
    service : str
        The id of the service.

    instance : str
        The id of the service instance.

    protocol : str (optional)
        The protocol that is used to implement the service instance. The default
        setting is _someip_. If a different setting is provided, vsomeip does
        not open the specified port (server side) or does not connect to the
        specified port (client side). Thus, this option can be used to let the
        service discovery announce a service that is externally implemented. 

    unicast : str (optional)
        The unicast that hosts the service instance. NOTE: The unicast address
        is needed if external service instances shall be used, but service
        discovery is disabled. In this case, the provided unicast address is
        used to access the service instance. 

    reliable : Reliable
        Specifies that the communication with the service is reliable
        respectively the TCP protocol is used for communication.

    unreliable : int
        Specifies that the communication with the service is unreliable
        respectively the UDP protocol is used for communication (valid values:
        the _port_ of the UDP endpoint).

    events: List[Event]
        Contains the events of the service.

    eventgroups: List[Eventgroup]
        Events can be grouped together into on event group. For a client it is
        thus possible to subscribe for an event group and to receive the
        appropriate events within the group.

    """
    service: str
    instance: str
    protocol: str
    unicast: str
    reliable: Reliable
    unreliable: str
    events: List[Event]
    eventgroups: List[Eventgroup]
    multicast: Endpoint

    @staticmethod
    def from_dict(obj: Any) -> 'Service':
        _service = str(obj.get("service", "0x0000"))
        _instance = str(obj.get("instance", "0x0000"))
        _protocol = str(obj.get("protocol", "tcp"))
        _unicast = str(obj.get("unicast", "0.0.0.1"))
        _reliable = Reliable.from_dict(obj.get("reliable", {}))
        _unreliable = str(obj.get("unreliable", "0x0000"))
        _events = [Event.from_dict(y) for y in obj.get("events", [])]
        _eventgroups = [Eventgroup.from_dict(y) for y in obj.get("eventgroups", [])]
        _multicast = Endpoint.from_dict(obj.get("multicast", {}))
        return Service(_service, _instance, _protocol, _unicast, _reliable, _unreliable, _events, _eventgroups, _multicast)


@dataclass
class ServiceDiscovery:
    """Contains settings related to the Service Discovery of the host application.

    Attributes
    ----------
    enable: str
        Specifies whether the Service Discovery is enabled (valid values:
        _true_, _false_). The default value is _true_.

    multicast: str
        The multicast address which the messages of the Service Discovery will
        be sent to. The default value is _224.0.0.1_.

    port: str
        The port of the Service Discovery. The default setting is _30490_.

    protocol: str
        The protocol that is used for sending the Service Discovery messages (valid
        values: _tcp_, _udp_). The default setting is _udp_.

    initial_delay_min: str
        Minimum delay before first offer message.

    initial_delay_max: str
        Maximum delay before first offer message.

    repetitions_base_delay: str
        Base delay sending offer messages within the repetition phase.

    repetitions_max: str
        Maximum number of repetitions for provided services within the
        repetition phase.

    ttl: str
        Lifetime of entries for provided services as well as consumed services
        and eventgroups.

    cyclic_offer_delay: str
        Cycle of the OfferService messages in the main phase.

    request_response_delay: str
        Minimum delay of a unicast message to a multicast message for provided
        services and eventgroups.

    offer_debounce_time: str
        Time which the stack collects new service offers before they enter the
        repetition phase. This can be used to reduce the number of sent messages
        during startup. The default setting is _500ms_.
    """
    enable: str
    multicast: str
    port: str
    protocol: str
    initial_delay_min: str
    initial_delay_max: str
    repetitions_base_delay: str
    repetitions_max: str
    ttl: str
    cyclic_offer_delay: str
    request_response_delay: str
    offer_debounce_time: str

    @staticmethod
    def from_dict(obj: Any) -> 'ServiceDiscovery':
        _enable = str(obj.get("enable", "true"))
        _multicast = str(obj.get("multicast", "224.0.0.1"))
        _port = str(obj.get("port", "30490"))
        _protocol = str(obj.get("protocol", "udp"))
        _initial_delay_min = str(obj.get("initial_delay_min", "0"))
        _initial_delay_max = str(obj.get("initial_delay_max", "0"))
        _repetitions_base_delay = str(obj.get("repetitions_base_delay", "0"))
        _repetitions_max = str(obj.get("repetitions_max", "0"))
        _ttl = str(obj.get("ttl", "3"))
        _cyclic_offer_delay = str(obj.get("cyclic_offer_delay", "0"))
        _request_response_delay = str(obj.get("request_response_delay", "0"))
        _offer_debounce_time = str(obj.get("offer_debounce_time", "500"))
        return ServiceDiscovery(_enable, _multicast, _port, _protocol, _initial_delay_min, _initial_delay_max, _repetitions_base_delay, _repetitions_max, _ttl, _cyclic_offer_delay, _request_response_delay, _offer_debounce_time)


@dataclass
class Configuration:
    """SOME/IP Configuration.

    Attributes
    ----------
    unicast: str
        The IP address of the host system.

    logging: Logging
        Logging configuration.

    applications: List[Application]
        Contains the applications of the host system that use this config file.

    clients: List[Client]
        The client-side ports that shall be used to connect to a specific
        service. For each service, an array of ports to be used for reliable /
        unreliable communication can be specified. vsomeip will take the first
        free port of the list. If no free port can be found, the connection will
        fail. If vsomeip is asked to connect to a service instance without
        specified port(s), the port will be selected by the system. This implies
        that the user has to ensure that the ports configured here do not
        overlap with the ports automatically selected by the IP stack.

    services: List[Service]
        Contains the services of the service provider.

    routing: str
        Specifies the properties of the routing. Either a string that specifies
        the application that hosts the routing component or a structure that
        specifies all properties of the routing. If the routing is not
        specified, the first started application will host the routing
        component.

    service_discovery: ServiceDiscovery
        Contains settings related to the Service Discovery of the host
        application.

    """
    unicast: str
    logging: Logging
    applications: List[Application]
    clients: List[Client]
    services: List[Service]
    routing: str
    service_discovery: ServiceDiscovery

    @staticmethod
    def from_dict(obj: Any) -> 'Configuration':
        _unicast = str(obj.get("unicast", "0.0.0.1"))
        _logging = Logging.from_dict(obj.get("logging", {}))
        _applications = [Application.from_dict(y) for y in obj.get("applications", {})]
        _clients = [Client.from_dict(y) for y in obj.get("clients", [])]
        _services = [Service.from_dict(y) for y in obj.get("services", [])]
        _routing = str(obj.get("routing", ""))
        _service_discovery = ServiceDiscovery.from_dict(obj.get("service-discovery", {}))
        return Configuration(_unicast, _logging, _applications, _clients, _services, _routing, _service_discovery)

# -----------------------------
# Swarm Simulator
# -----------------------------

from agent import Agent

class ProtocolTypes:
    FLOODING = "flooding"
    GOSSIP = "gossip"
    ADAPTIVE = "adaptive"

class SwarmSimulator:
    """
    Discrete event simulator for swarm communication.

    Every robot in the swarm plays two roles:

    1. Information Producer
       Robots occasionally generate new packets
       representing sensor measurements, navigation
       updates or discovered events.

    2. Router
       Robots forward packets received from neighbouring
       robots so information can propagate throughout
       the swarm.

    The simulator advances one discrete communication
    step at a time rather than using real wall clock
    time. This makes experiments deterministic and
    reproducible.
    """
    def __init__(self, num_agents=50, steps=200, protocol=ProtocolTypes.ADAPTIVE):
        self.num_agents = num_agents
        self.steps = steps
        self.agents = []
        self.history = []
        self.comm_range = 25
        self.messages = []
        self.message_id = 0
        self.protocol = protocol
        self.current_step = 0
        # Virtual propagation speed.
        # Used to convert communication distance into
        # transmission delay measured in simulation steps.
        #
        # Example:
        # Distance = 25 units
        # Speed = 10 units/step
        #
        # Packet arrives after ceil(25/10)=3 steps.
        self.propagation_speed = 10.0

        # metrics
        self.sent_packets = 0
        self.received_packets = 0
        self.total_transmissions = 0
        self.total_latency = 0
        self.init_agents()

    def init_agents(self):
        for i in range(self.num_agents):
            a = Agent(
                agent_id=i,
                x=random.uniform(0, 100),
                y=random.uniform(0, 100),
                speed=random.uniform(0.5, 2.0)
            )
            self.agents.append(a)

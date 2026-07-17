"""
=====================================================================
Adaptive Swarm Communication Simulator
=====================================================================

Author:
    Muhammad Rashid Ali Khan

Description
-----------
This project simulates communication within a decentralized swarm of
mobile robots operating in a wireless ad hoc network.

Unlike traditional computer networks where devices communicate through
fixed infrastructure, every robot in the swarm performs two roles
simultaneously:

    1. Information Producer
       Generates new packets representing sensor observations,
       navigation updates, obstacle detections, battery status,
       or other information that should be shared.

    2. Router
       Receives packets from neighbouring robots and decides whether
       those packets should be forwarded farther into the swarm.

The simulator compares several communication strategies to study how
efficiently information spreads as swarm size increases.

The implemented routing protocols are:

    • Flooding
    • Gossip Routing
    • Density Adaptive Routing

The objective is to evaluate the tradeoff between

    • Delivery Ratio
    • Communication Latency
    • Network Overhead

=====================================================================
Simulation Philosophy
=====================================================================

This is a discrete event simulator.

The simulator DOES NOT use real wall clock time.

Instead, time advances in fixed simulation steps.

Every iteration represents one communication cycle for the entire swarm.

Simulation Step

    Step k

        ↓

    Move Robots

        ↓

    Process Arriving Packets

        ↓

    Generate New Messages

        ↓

    Route / Forward Messages

        ↓

    Schedule Future Deliveries

        ↓

    Advance to Step k + 1

Using discrete simulation time makes experiments deterministic,
repeatable and independent of computer performance.

=====================================================================
Communication Model
=====================================================================

Communication is based on information dissemination rather than
point to point messaging.

Example

Robot A discovers an obstacle.

Instead of sending the information to one destination, Robot A
broadcasts the packet to every neighbouring robot.

Those neighbours may rebroadcast the packet to their neighbours,
allowing information to spread across the entire swarm.

This communication model is commonly used in

    • Robot swarms
    • Wireless Sensor Networks
    • Mobile Ad Hoc Networks (MANETs)

=====================================================================
Packet Lifecycle
=====================================================================

Every packet follows the same sequence.

    Robot generates information

            ↓

    Packet created

            ↓

    Nearby neighbours receive packet

            ↓

    Each neighbour decides whether to forward

            ↓

    Packet scheduled to arrive after propagation delay

            ↓

    Receiving robot processes packet

            ↓

    Packet forwarded again (optional)

            ↓

    TTL reaches zero

            ↓

    Packet discarded

=====================================================================
Duplicate Prevention
=====================================================================

Broadcast communication naturally creates duplicate packets.

Example

            B
           / \
    A ----     ---- D
           \ /
            C

Robot D may receive the same packet from both B and C.

To prevent endless rebroadcasting, every robot stores the IDs of
previously processed packets.

If the same packet arrives again, it is discarded.

=====================================================================
Time To Live (TTL)
=====================================================================

Every packet carries a Time To Live (TTL) value.

Every forwarding operation decreases the TTL.

Example

    TTL = 5

        ↓

    4

        ↓

    3

        ↓

    2

        ↓

    1

        ↓

    0

Once TTL reaches zero the packet is discarded.

This prevents packets from circulating forever.

=====================================================================
Wireless Channel Assumptions
=====================================================================

The current simulator models several simplified wireless effects.

    • Finite communication range

    • Distance dependent packet loss

    • Finite receiver buffer

    • Propagation delay proportional to distance

Future versions may also include

    • CSMA/CA

    • Binary exponential backoff

    • RTS / CTS

    • TDMA scheduling

    • Multi channel communication

=====================================================================
Performance Metrics
=====================================================================

The simulator measures

Delivery Ratio

    Successfully delivered packets
    ------------------------------
      Generated packets

Average Latency

    Average number of simulation steps required for a packet
    to reach receiving robots.

Transmission Count

    Total forwarding operations performed by the swarm.

These metrics allow communication protocols to be compared as the
number of robots increases.

=====================================================================
Limitations
=====================================================================

This simulator is intended for communication algorithm evaluation,
not physical layer accuracy.

Many real world effects are intentionally simplified, including

    • Radio propagation
    • MAC protocol behaviour
    • Wireless interference
    • Hardware timing

The design prioritizes clarity, extensibility and algorithm
comparison over exact network emulation.

=====================================================================
"""


import random
import math
import matplotlib.pyplot as plt
import time


# -----------------------------
# Agent
# -----------------------------
class Agent:
    def __init__(self, agent_id, x, y, speed=1.0):
        self.id = agent_id
        self.x = x
        self.y = y
        self.speed = speed

        self.tx = random.uniform(0, 100)
        self.ty = random.uniform(0, 100)

        self.inbox = []
        self.buffer_limit = 10
        # Prevent forwarding duplicate packets.
        #
        # Broadcast protocols naturally create multiple copies
        # of the same packet.
        #
        # Once a robot has processed a packet ID once,
        # every future copy is discarded.
        #
        # This prevents infinite rebroadcast loops.
        self.seen_messages = set()

    def distance_to_target(self):
        return math.sqrt((self.tx - self.x) ** 2 + (self.ty - self.y) ** 2)

    def set_new_target(self):
        self.tx = random.uniform(0, 100)
        self.ty = random.uniform(0, 100)

    def move(self):
        dx = self.tx - self.x
        dy = self.ty - self.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < 1:
            self.set_new_target()
            return

        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed

class ProtocolTypes:
    FLOODING = "flooding"
    GOSSIP = "gossip"
    ADAPTIVE = "adaptive"

# -----------------------------
# Swarm Simulator
# -----------------------------
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

def step(self):

    # Move every robot toward its current destination.
    # Robot movement changes the communication topology,
    # meaning neighbours may appear or disappear every step.
    for a in self.agents:
        a.move()

    # Simulate one complete communication cycle.
    self.communication_step()

    # Advance simulation clock.
    self.current_step += 1

    def run(self):
        for _ in range(self.steps):
            self.step()

    def plot(self):
        # final positions
        x = [a.x for a in self.agents]
        y = [a.y for a in self.agents]

        plt.figure()
        plt.scatter(x, y)
        plt.title("Swarm Final Positions (Day 1)")
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.show()

    def animate(self):
        plt.ion()
        fig, ax = plt.subplots()

        for _ in range(self.steps):
            ax.clear()

            self.step()
            # draw links
            for a in self.agents:
                neighbors = self.get_neighbors(a)
                for n in neighbors:
                    ax.plot([a.x, n.x], [a.y, n.y], linewidth=0.5)

            # draw nodes
            x = [a.x for a in self.agents]
            y = [a.y for a in self.agents]

            ax.scatter(x, y)

            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.set_title("Swarm Communication Links")
            avg_latency = 0

            if self.received_packets > 0:
                avg_latency = (
                    self.total_latency /
                    self.received_packets
                )

            ax.set_title(
                f"Protocol: {self.protocol} | "
                f"Sent: {self.sent_packets} | "
                f"Received: {self.received_packets} | "
                f"Latency: {avg_latency:.3f}s"
            )

            plt.pause(0.05)

        plt.ioff()
        plt.show()

    def get_neighbors(self, agent):
        """
        Discover all robots inside wireless communication range.
        The neighbour list represents every robot that can
        directly exchange packets with this robot during the
        current simulation step.
        """
        neighbors = []

        for other in self.agents:
            if other.id == agent.id:
                continue

            dist = math.sqrt((agent.x - other.x)**2 + (agent.y - other.y)**2)

            if dist <= self.comm_range:
                neighbors.append(other)

        return neighbors
    
    def create_message(self, sender_id):
        return {
            "id": self.message_id,
            "sender": sender_id,
            "ttl": 5
        }
    
    def communication_step(self):
        """
        Executes one communication cycle.

        Every simulation step performs two independent tasks.

        1. Process packets that have arrived this step.
        These packets may be forwarded to neighbouring robots.

        2. Generate new packets.
        Every robot has a small probability of creating
        brand new information (sensor update, obstacle,
        position estimate, etc.).

        Therefore each robot acts simultaneously as

            • a packet producer
            • a packet forwarder

        exactly as in many distributed swarm systems.
        """

        # process existing delayed packets
        for a in self.agents:
            self.process_inbox(a)

        # message generation
        for agent in self.agents:

            if random.random() < 0.03:

                msg = {
                    "id": self.message_id,
                    "sender": agent.id,
                    "ttl": 5,
                    "created_step": self.current_step
                }

                self.message_id += 1
                self.sent_packets += 1

                neighbors = self.get_neighbors(agent)

                for n in neighbors:
                    self.try_forward(agent, n, msg)

    def forward_message(self, sender, receiver, msg):
        """
        Attempts to transmit one packet from sender to receiver.

        Successful delivery depends on

        • wireless distance
        • packet loss model
        • receiver buffer capacity

        If transmission succeeds, the packet is scheduled to
        arrive several simulation steps later according to
        its propagation delay.
        """
        dx = sender.x - receiver.x
        dy = sender.y - receiver.y
        dist = math.sqrt(dx * dx + dy * dy)

        # LOSS MODEL
        if not self.transmission_success(dist):
            return

        # BUFFER CHECK
        if len(receiver.inbox) >= receiver.buffer_limit:
            return

        delayed_msg = self.copy_message(msg)

        delay_steps = max(
            1,
            math.ceil(dist / self.propagation_speed)
        )

        delayed_msg["arrival_step"] = (
            self.current_step + delay_steps
        )
        receiver.inbox.append(delayed_msg)

    def process_inbox(self, agent):
        """
        Deliver every packet whose arrival time has been reached.

        Packets remain inside the receiver's inbox until their
        scheduled arrival step.

        Once delivered, the robot decides whether the packet
        should be forwarded according to the selected routing
        protocol.
        """
        current_step = self.current_step

        ready_messages = []

        for msg in agent.inbox:
            if msg["arrival_step"] <= current_step:
                ready_messages.append(msg)

        for msg in ready_messages:
            agent.inbox.remove(msg)

            # duplicate prevention
            if msg["id"] in agent.seen_messages:
                continue

            agent.seen_messages.add(msg["id"])

            self.received_packets += 1

            latency = current_step - msg["created_step"]
            self.total_latency += latency

            # protocol forwarding
            self.route_message(agent, msg)

    def route_message(self, agent, msg):
        """
        Routing decision.

        The simulator models information dissemination rather
        than point to point communication.

        Each received packet represents information that may
        still need to reach robots farther away.

        Therefore a robot decides whether to rebroadcast the
        packet to all neighbouring robots.

        Forwarding stops when

        • TTL reaches zero
        • protocol decides not to forward
        """
        if msg["ttl"] <= 0:
            return

        neighbors = self.get_neighbors(agent)

        for neighbor in neighbors:

            # prevent bounce back
            if neighbor.id == msg["sender"]:
                continue

            forward = False

            # --------------------------------
            # FLOODING:
            #
            # Forward every received packet to every neighbour.
            #
            # Advantages
            # ----------
            # Maximum coverage.
            #
            # Disadvantages
            # -------------
            # Heavy network traffic.
            # Broadcast storm in large swarms.
            #  
            # --------------------------------
            if self.protocol == "flooding":
                forward = True

            # --------------------------------
            # GOSSIP
            # 
            # Advantages
            # ----------
            # Forward only with a fixed probability.
            #
            # Disadvantages
            # -------------
            # Reduces communication overhead but may leave
            # parts of the swarm uninformed.
            #
            # --------------------------------
            elif self.protocol == "gossip":
                if random.random() < 0.4:
                    forward = True

            # --------------------------------
            # ADAPTIVE
            # Density adaptive routing.
            #
            # Robots in sparse regions forward more often.
            #
            # Robots surrounded by many neighbours forward
            # less frequently because nearby robots are
            # already likely to retransmit the packet.
            #
            # Goal:
            # Reduce redundant transmissions while maintaining
            # good network coverage.
            #
            # --------------------------------
            elif self.protocol == "adaptive":

                density = len(neighbors)

                forwarding_probability = min(
                    1.0,
                    5 / (density + 1)
                )

                if random.random() < forwarding_probability:
                    forward = True

            if forward:
                new_msg = self.copy_message(msg)
                new_msg["ttl"] -= 1

                self.try_forward(agent, neighbor, new_msg)

    
    def try_forward(self, sender, receiver, msg):

        if msg["ttl"] <= 0:
            return

        self.total_transmissions += 1

        self.forward_message(sender, receiver, msg)

    def copy_message(self, msg):
        return {
            "id": msg["id"],
            "sender": msg["sender"],
            "ttl": msg["ttl"],
            "created_step": msg["created_step"]
        }
    
    def transmission_success(self, distance):
        """
        Simple wireless channel model.

        Packet loss increases with transmission distance.

        Long links are less reliable than short links,
        approximating the behaviour of real wireless
        communication systems.
        """
        # distance based loss + noise
        base_loss = distance / self.comm_range
        random_noise = random.uniform(0, 0.3)

        probability = min(1.0, base_loss + random_noise)

        return random.random() > probability
    
    def get_metrics(self):

        delivery_ratio = 0
        avg_latency = 0

        if self.sent_packets > 0:
            delivery_ratio = (
                self.received_packets /
                self.sent_packets
            )

        if self.received_packets > 0:
            avg_latency = (
                self.total_latency /
                self.received_packets
            )

        return {
            "protocol": self.protocol,
            "delivery_ratio": delivery_ratio,
            "latency": avg_latency,
            "transmissions": self.total_transmissions
        }
    
    def reset_metrics(self):

        self.sent_packets = 0
        self.received_packets = 0
        self.total_transmissions = 0
        self.total_latency = 0
        self.message_id = 0

        for a in self.agents:
            a.inbox.clear()
            a.seen_messages.clear()

    def simulate(self):

        for _ in range(self.steps):

            for a in self.agents:
                a.move()

            self.communication_step()

        return self.get_metrics()


def run_experiment():

    protocols = [
        "flooding",
        "gossip",
        "adaptive"
    ]

    swarm_sizes = [
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100
    ]

    num_trials = 20

    results = []

    for protocol in protocols:

        for size in swarm_sizes:

            print(
                f"\nRunning {protocol}"
                f" with {size} agents"
            )

            delivery_sum = 0
            latency_sum = 0
            transmission_sum = 0

            for trial in range(num_trials):

                print(
                    f" Trial "
                    f"{trial + 1}/{num_trials}"
                )

                sim = SwarmSimulator(
                    num_agents=size,
                    steps=1000,
                    protocol=protocol
                )

                metrics = sim.simulate()

                delivery_sum += (
                    metrics["delivery_ratio"]
                )

                latency_sum += (
                    metrics["latency"]
                )

                transmission_sum += (
                    metrics["transmissions"]
                )

            avg_metrics = {
                "protocol": protocol,
                "agents": size,
                "delivery_ratio":
                    delivery_sum / num_trials,
                "latency":
                    latency_sum / num_trials,
                "transmissions":
                    transmission_sum / num_trials
            }

            results.append(avg_metrics)

    return results

def plot_results(results):

    protocols = [
        "flooding",
        "gossip",
        "adaptive"
    ]

    metrics = [
        "delivery_ratio",
        "latency",
        "transmissions"
    ]

    for metric in metrics:

        plt.figure()

        for protocol in protocols:

            subset = [
                r for r in results
                if r["protocol"] == protocol
            ]

            x = [r["agents"] for r in subset]
            y = [r[metric] for r in subset]

            plt.plot(
                x,
                y,
                marker="o",
                label=protocol
            )

        plt.xlabel("Number of Agents")
        plt.ylabel(metric)
        plt.title(
            f"{metric} vs Swarm Size"
        )
        plt.legend()
        plt.grid(True)


# -----------------------------
# Run
# -----------------------------

def simulate_and_animate():
    sim = SwarmSimulator(num_agents=50, steps=200, protocol=ProtocolTypes.GOSSIP)
    sim.animate()

def plot_experiment():
    results = run_experiment()
    for r in results:
        print(r)
    plot_results(results)
    plt.show()

if __name__ == "__main__":

    plot_experiment()
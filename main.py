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
        for a in self.agents:
            a.move()

        self.communication_step()

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
        if msg["ttl"] <= 0:
            return

        neighbors = self.get_neighbors(agent)

        for neighbor in neighbors:

            # prevent bounce back
            if neighbor.id == msg["sender"]:
                continue

            forward = False

            # --------------------------------
            # FLOODING
            # --------------------------------
            if self.protocol == "flooding":
                forward = True

            # --------------------------------
            # GOSSIP
            # --------------------------------
            elif self.protocol == "gossip":
                if random.random() < 0.4:
                    forward = True

            # --------------------------------
            # ADAPTIVE (your contribution)
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
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



# -----------------------------
# Swarm Simulator
# -----------------------------
class SwarmSimulator:
    def __init__(self, num_agents=50, steps=200):
        self.num_agents = num_agents
        self.steps = steps
        self.agents = []
        self.history = []
        self.comm_range = 15
        self.messages = []
        self.message_id = 0
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

            # move agents
            for a in self.agents:
                a.move()

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
        new_messages = []

        # each agent generates a message sometimes
        for agent in self.agents:
            if random.random() < 0.05:
                msg = self.create_message(agent.id)
                self.message_id += 1
                new_messages.append((agent.id, msg))

        # propagate messages
        for sender_id, msg in new_messages:
            sender = self.agents[sender_id]
            neighbors = self.get_neighbors(sender)

            for n in neighbors:
                self.forward_message(n, msg)

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

        # DELAY SIMULATION (simple queue)
        delayed_msg = self.copy_message(msg)
        delayed_msg["arrival_time"] = time.time() + dist * 0.01

        receiver.inbox.append(delayed_msg)

    def process_inbox(self, agent):
        current_time = time.time()

        ready = []

        for msg in agent.inbox:
            if "arrival_time" in msg and msg["arrival_time"] <= current_time:
                ready.append(msg)

        for msg in ready:
            agent.inbox.remove(msg)
    
    def communication_step(self):
        # process delayed messages first
        for a in self.agents:
            self.process_inbox(a)

        # generate new messages
        for agent in self.agents:
            if random.random() < 0.05:
                msg = {
                    "id": self.message_id,
                    "sender": agent.id,
                    "ttl": 5
                }
                self.message_id += 1

                neighbors = self.get_neighbors(agent)

                for n in neighbors:
                    self.try_forward(agent, n, msg)
    
    def try_forward(self, sender, receiver, msg):
        if msg["ttl"] <= 0:
            return

        msg2 = self.copy_message(msg)
        msg2["ttl"] -= 1

        self.forward_message(sender, receiver, msg2)

    def copy_message(self, msg):
        return {
            "id": msg["id"],
            "sender": msg["sender"],
            "ttl": msg["ttl"]
        }
    
    def transmission_success(self, distance):
        # distance based loss + noise
        base_loss = distance / self.comm_range
        random_noise = random.uniform(0, 0.3)

        probability = min(1.0, base_loss + random_noise)

        return random.random() > probability

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    sim = SwarmSimulator(num_agents=50, steps=200)
    sim.animate()
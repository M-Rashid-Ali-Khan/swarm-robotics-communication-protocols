import random
import math
import matplotlib.pyplot as plt


# -----------------------------
# Agent
# -----------------------------
class Agent:
    def __init__(self, agent_id, x, y, speed=1.0):
        self.id = agent_id
        self.x = x
        self.y = y
        self.speed = speed

        # target for random waypoint
        self.tx = random.uniform(0, 100)
        self.ty = random.uniform(0, 100)

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

    def forward_message(self, agent, msg):
        if not hasattr(agent, "inbox"):
            agent.inbox = []

        # avoid duplicates
        if msg["id"] in [m["id"] for m in agent.inbox]:
            return

        agent.inbox.append(msg)

        # simple TTL decay
        msg = msg.copy()
        msg["ttl"] -= 1

        if msg["ttl"] > 0:
            neighbors = self.get_neighbors(agent)
            for n in neighbors:
                if n.id != agent.id:
                    self.forward_message(n, msg)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    sim = SwarmSimulator(num_agents=50, steps=200)
    sim.animate()
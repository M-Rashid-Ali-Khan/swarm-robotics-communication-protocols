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

        # store snapshot
        snapshot = [(a.x, a.y) for a in self.agents]
        self.history.append(snapshot)

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

            for a in self.agents:
                a.move()

            x = [a.x for a in self.agents]
            y = [a.y for a in self.agents]

            ax.scatter(x, y)

            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.set_title("Swarm Movement (Live)")

            plt.pause(0.05)

        plt.ioff()
        plt.show()


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    sim = SwarmSimulator(num_agents=50, steps=200)
    sim.animate()
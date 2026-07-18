# -----------------------------
# Agent
# -----------------------------

import math
import random

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

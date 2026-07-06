# Adaptive Swarm Communication Simulator

A Python-based simulator for studying communication protocols in large-scale mobile robot swarms.

The simulator models a wireless ad hoc network of autonomous agents that move through a 2D environment while exchanging messages using different routing strategies.

The primary objective is to investigate the tradeoff between communication reliability, latency, and network overhead as swarm size increases.

---

## Motivation

Future robotic swarms used for:

* Space exploration
* Environmental monitoring
* Disaster response
* Search and rescue

require reliable communication without centralized infrastructure.

Naive communication protocols such as Flooding become inefficient as the number of robots grows because every node forwards nearly every packet, causing congestion and excessive bandwidth usage.

This project compares three routing strategies under realistic wireless constraints:

* Flooding
* Gossip Routing
* Density Adaptive Routing

---

# Simulation Overview

Each simulation consists of a swarm of mobile agents.

Every agent:

* Moves toward a random destination.
* Detects neighbouring agents within communication range.
* Randomly generates messages.
* Receives and forwards messages.
* Maintains an inbox that simulates network buffering.

The simulator runs in discrete communication steps.

Each step contains:

1. Agent movement
2. Message generation
3. Wireless transmission
4. Packet forwarding
5. Metrics collection

---

# Simulation Environment

World size

100 × 100 units

Number of agents

10–100

Communication range

25 units

Simulation duration

1000 communication steps

Trials per experiment

20

---

# Routing Protocols

## Flooding

Every node forwards every received packet.

Advantages

* Highest redundancy
* Highest probability of delivery

Disadvantages

* Broadcast storm
* Heavy congestion
* Large transmission overhead

---

## Gossip Routing

Each node forwards with a fixed probability.

Advantages

* Reduced network traffic
* Lower congestion

Disadvantages

* Some packets never reach the destination
* Increased latency

---

## Density Adaptive Routing

Forwarding probability depends on local neighbourhood density.

Sparse areas

High forwarding probability.

Dense areas

Low forwarding probability.

Goal

Reduce unnecessary retransmissions while maintaining delivery performance.

---

# Wireless Network Model

The simulator models several real-world networking effects.

## Distance based packet loss

Signal quality decreases with transmission distance.

Longer links have a higher probability of failure.

---

## Communication delay

Packets require time to travel between sender and receiver.

Propagation delay is proportional to distance.

---

## Receiver buffer

Each agent has a finite inbox.

When congestion increases, packet drop probability also increases.

---

## Collision model

Dense neighbourhoods increase the probability that simultaneous transmissions collide.

Collision probability increases with local node density.

---

## Channel congestion

All transmissions share a common wireless medium.

As channel utilisation increases:

* throughput decreases
* packet failures increase

---

## CSMA inspired backoff

If the communication channel is busy:

1. The sender waits.
2. A random backoff is selected.
3. Transmission is retried later.

This approximates Carrier Sense Multiple Access (CSMA) behaviour used in IEEE 802.11 wireless networks.

---

# Message Lifecycle

Message created

↓

Neighbours discovered

↓

Routing protocol decides forwarding

↓

Channel availability checked

↓

Distance loss evaluated

↓

Collision model evaluated

↓

Buffer availability checked

↓

Packet delivered

↓

Receiver forwards packet

↓

TTL reaches zero

↓

Packet discarded

---

# Performance Metrics

The simulator records:

## Delivery Ratio

Delivered packets / Generated packets

Measures communication reliability.

---

## Average Latency

Average end-to-end packet delay.

Measures communication speed.

---

## Transmission Count

Total packet transmissions.

Measures network overhead.

---

# Experiment Design

For every routing protocol:

For swarm sizes

10

20

30

...

100

Twenty independent simulations are executed.

Results are averaged to reduce randomness.

The simulator produces comparison plots for:

* Delivery Ratio vs Swarm Size
* Average Latency vs Swarm Size
* Transmission Count vs Swarm Size

---

# Example Results

Typical behaviour:

Flooding

* Highest delivery ratio
* Highest transmission overhead
* Suffers under heavy congestion

Gossip

* Lowest communication overhead
* Moderate delivery ratio

Adaptive

* Similar delivery to flooding
* Lower transmission overhead
* Better scalability

---

# Project Structure

Agent

Represents an autonomous robot.

Responsible for:

* movement
* inbox
* packet reception

SwarmSimulator

Responsible for:

* communication
* routing
* wireless modelling
* experiments
* visualization

---

# Future Improvements

Possible extensions include:

* Binary exponential backoff
* RTS/CTS handshake
* Multi-channel communication
* Energy-aware routing
* ROS2 integration
* NS-3 networking backend
* Reinforcement learning based routing
* 3D swarm environments

---

# Technologies

* Python
* Matplotlib
* Random
* Object Oriented Programming

---

# Author

Muhammad Rashid Ali Khan

Mechatronics Engineer

Embedded Systems | Robotics | Distributed Systems
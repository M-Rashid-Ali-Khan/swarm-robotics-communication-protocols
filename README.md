# Swarm Communication Simulator

A Python based simulation of message dissemination in a mobile swarm network. The simulator models autonomous agents that move in a 2D environment and exchange messages using different communication protocols. It compares the performance of Flooding, Gossip, and an Adaptive forwarding strategy under varying swarm sizes.

## Features

* Mobile agents with random waypoint movement
* Distance based communication range
* Packet propagation delay
* Distance dependent packet loss model
* Limited receiver buffer
* Duplicate message suppression
* Message Time To Live (TTL)
* Multiple forwarding protocols:
  * Flooding
  * Gossip
  * Adaptive probabilistic forwarding
* Performance evaluation across different swarm sizes
* Animated network visualization
* Experimental plotting for protocol comparison

## Communication Protocols

### Flooding

Every received message is forwarded to all neighboring agents until its TTL expires.

**Advantages**
* Highest message dissemination
* Simple implementation

**Disadvantages**
* High transmission overhead
* Significant redundancy

### Gossip

Each neighbor receives a forwarded message with a fixed probability (40%).

**Advantages**
* Lower network traffic
* Reduced redundancy

**Disadvantages**
* Lower delivery ratio than flooding

### Adaptive

Forwarding probability depends on local network density.

```
forwarding_probability = min(1.0, 5 / (density + 1))
```

Dense neighborhoods result in fewer retransmissions, while sparse areas forward more aggressively.

## Simulation Model

Each agent:

* Moves toward a randomly selected destination
* Chooses a new destination upon arrival
* Generates messages randomly
* Maintains:
  * Inbox
  * Seen message history
  * Limited receive buffer

Communication includes:

* Neighbor discovery
* Propagation delay based on distance
* Packet loss based on transmission distance
* TTL based forwarding

## Metrics

The simulator measures:

* Delivery Ratio
* Average Latency
* Total Transmissions

These metrics are averaged over multiple trials for different swarm sizes.

## Experiment Configuration

Default experiment:

* Swarm sizes: 10 to 100 agents
* Simulation steps: 1000
* Trials per configuration: 20
* Protocols:
  * Flooding
  * Gossip
  * Adaptive

## Requirements

Python 3.x

Install dependencies:

```bash
pip install matplotlib
```

## Running

Run the experiment:

```bash
python main.py
```

This executes all experiments, prints averaged results, and displays comparison graphs.

## Visualization

To view the live animation instead of the experiment, replace the main section with:

```python
if __name__ == "__main__":
    simulate_and_animate()
```

The animation displays:

* Moving agents
* Communication links
* Active protocol
* Packets sent
* Packets received
* Average latency

## Project Structure

```
Agent
│
├── Movement
├── Inbox
├── Buffer
└── Message History

SwarmSimulator
│
├── Agent Movement
├── Neighbor Discovery
├── Packet Forwarding
├── Delay Model
├── Packet Loss
├── Metrics
├── Animation
└── Experiments
```

## Output

The experiment produces three comparison plots:

* Delivery Ratio vs Swarm Size
* Average Latency vs Swarm Size
* Total Transmissions vs Swarm Size

These plots can be used to compare the efficiency and scalability of each communication protocol.

## Future Improvements

* Energy consumption model
* Dynamic communication ranges
* Obstacles and terrain
* Additional routing protocols
* Parallel experiment execution
* Network partition analysis
* Mobility models beyond random waypoint

## License

This project is intended for educational and research purposes.
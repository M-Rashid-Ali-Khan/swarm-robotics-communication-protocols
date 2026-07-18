# Experiment: Communication Protocol Evaluation in Swarm Robotics

## Objective

Evaluate the performance of three communication protocols across different swarm sizes by comparing message delivery, latency, and communication overhead.

## Protocols Evaluated

- Flooding
- Gossip
- Adaptive

## Swarm Sizes

The following swarm sizes are evaluated:

- 10 agents
- 20 agents
- 30 agents
- 40 agents
- 50 agents
- 60 agents
- 70 agents
- 80 agents
- 90 agents
- 100 agents

## Simulation Configuration

| Parameter | Value |
|-----------|-------|
| Simulation steps | 1000 |
| Trials per configuration | 20 |
| Total protocols | 3 |
| Total swarm sizes | 10 |
| Total experiment configurations | 30 |
| Total simulations | 600 |

## Experimental Procedure

For each communication protocol:

1. Iterate through each swarm size.
2. Run the simulator for 20 independent trials.
3. Each simulation executes for 1000 time steps.
4. Record the following metrics after each trial:
   - Delivery Ratio
   - Latency
   - Number of Transmissions
5. Compute the average of each metric across the 20 trials.
6. Store the averaged results for later analysis.

## Metrics Collected

### Delivery Ratio

The proportion of successfully delivered messages relative to the total messages generated.

Higher values indicate better reliability.

### Latency

The average time required for messages to reach their destination.

Lower values indicate faster communication.

### Transmissions

The total number of message transmissions performed during the simulation.

Lower values indicate lower communication overhead and better network efficiency.

## Independent Variables

- Communication Protocol
- Swarm Size

## Dependent Variables

- Average Delivery Ratio
- Average Latency
- Average Number of Transmissions

## Output

Each experiment configuration produces one averaged result containing:

- Protocol
- Number of Agents
- Average Delivery Ratio
- Average Latency
- Average Transmissions

The complete experiment generates 30 averaged data points, one for each combination of protocol and swarm size.

## Reference Implementation

```
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
```
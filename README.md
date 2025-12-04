## Description

This code is designed to optimize the robot picking sequence in a bipartite setting. The objective of the optimization is to minimize the total travel time required for the robot to complete its picking tasks from a set of Gravity Racks and placing tasks to a set of Kit Holders.

In the real-world application, we work with a detailed mapping between containers, Gravity Rack positions and Kit Holders. Each KH slot requires specific component types, and each GR pocket provides specific components. On top of this mapping we apply an exact–linear approach: an exact optimization method to compute the optimal picking sequence, and a linear baseline to approximate it. Comparing these two allows us to study the trade-off between optimality and computation time in realistic MODAPTO kitting scenarios.

In parallel, we also include complete-graph benchmark cases, where all nodes represent generic positions and components are treated in a uniform way (e.g. all of the same type). On these abstract instances we experiment with Nearest Neighbor, 2-opt, Q-Learning and the Exact method, not to model a specific factory layout, but to compare algorithms themselves under controlled conditions. By looking at objective values and execution times across both the real-world BTSP cases and the complete-graph benchmarks, we can better understand the strengths and limitations of each method and when each one is most appropriate.

## How to use optEngine
This service comes along with [optEngine](https://github.com/Modapto/optEngine/tree/main), i.e., a data-agnostic API responsible to dispatch the required data to this optimization service.
Documentation of optEngine can be found [here](https://optengine.adopt.eltrun.gr:10100/api/v1/swagger-ui/index.html?configUrl=/api/v1/api-docs/swagger-config).

Use the following curl commands in this sequence: 

1. curl -k -X POST https://optengine.adopt.eltrun.gr:10100/api/v1/opt/job -H "Authorization:USE_AUTHORIZATION_KEY" -H "Content-Type: application/json" -d "@PATH_TO_crfIn.json"
2. keep the returned uuid
3. curl -k "https://optengine.adopt.eltrun.gr:10100/api/v1/opt/job/result?uuid=THE_RETURNED_UUID" -H "Authorization:USE_AUTHORIZATION_KEY"

### How to use Optimization / Simulation

- **Optimization (real-world mapping)**  
  This mode uses the real Gravity Rack / Kit Holder mapping. Each component type appears in specific containers and positions, and each KH requires a specific bill-of-materials. Methods such as `exact`, `linear` and `exact-linear` use these mappings and the distance matrix to compute feasible pick-and-place sequences.

- **Complete-graph optimization (algorithm benchmarks)**  
  In this mode, the problem is defined on a complete distance matrix without detailed component mapping. Methods such as `nearest_complete`, `2opt_complete`, `exact_complete`, `qlearning_complete` and `all_complete` operate on this abstract graph to compare algorithms independently of a specific industrial configuration.

- **Simulation**  
  The simulation mode (`method = "simulation"`) runs multiple configurations of the Gravity Rack layout and evaluates the resulting picking sequences. It is designed to work together with external services (e.g. optEngine and a production simulator) and to support co-simulation scenarios where the layout is changed and evaluated iteratively.

### Input JSON (high-level overview)

All use cases follow the same basic envelope:

- Top level: an object that may contain a `uuid` and a `data` field.
- The `data` field contains the configuration and a `method` field that controls which mode is used.

Some typical fields inside `data` are:

- For **real-world optimization** (`method = "exact"`, `"linear"`, `"exact-linear"`):  
  A `templates` block with `containers_opt`, `kit_holders_opt`, `kh_sequences_opt`, `distance_matrix_opt`, plus a specific `gr_sequence` describing the current Gravity Rack layout, and the chosen `method`. These describe which containers exist, what they contain, how they are placed on the Gravity Rack, which Kit Holders are active, and which distances are used.

- For **complete-graph benchmarks**:  
  `distance_matrix_opt` (full graph distances), with `method` set to one of the `*_complete` variants (`"nearest_complete"`, `"2opt_complete"`, `"exact_complete"`, `"qlearning_complete"`, `"all_complete"`). Here the focus is on comparing Nearest Neighbor, 2-opt, Q-Learning and Exact on a generic complete graph.

- For **simulation / co-simulation** (`method = "simulation"`):  
  A `templates` block with `containers_sim`, `kit_holders_sim`, `kh_sequences_sim`, `distance_matrix_sim`,  
  together with a baseline `gr_sequence` and `num_random_gr_configs` specifying how many random GR configurations to test. The service uses these templates to build concrete instances, randomize Gravity Rack layouts and evaluate the resulting sequences.

### Repository Files 
This repository contains the code and example artefacts for the single-gripper robot picking sequence optimization.  
The main logic is implemented in Python modules (optimization, simulation, graph creation, heuristics, exact solver, etc.), while the files below are ready-made inputs/outputs you can inspect or reuse:

- `input_data.json`  
  Plain, decoded example input for a single-gripper optimization or simulation run.

- `encoded_input.json`  
  Same logical content as `input_data.json`, but wrapped in the encoded format used by optEngine / the message bus:  
  a top-level `uuid` plus a `data.base64` field that carries the payload as a Base64-encoded blob.

- `opt_execution_output.json`  
  Human-readable (decoded) result of an optimization run (e.g. `exact`, `linear`, or `exact-linear`).  
  Contains the total cost, detailed `time_details` (with `from`, `to`, and `component_*` info), and data such as `solutionTime` and `totalTime`.

- `sim_execution_output.json`  
  Human-readable (decoded) result of a **simulation** run.  
  Includes baseline costs, the baseline `gr_sequence`, and the best GR configuration found across multiple random trials.

- `encoded_opt_output.json`  
  Encoded version of the optimization result (similar content to `opt_execution_output.json`), with the full result stored under `data.base64`.  
  This is what is pushed back to optEngine / the message bus.

- `encoded_sim_output.json`  
  Encoded version of the simulation result (similar structure to `encoded_opt_output.json`, but for simulation).

- `q_values.csv`  
  Exported Q-learning Q-table from complete-graph experiments in the single-gripper case.  

These files are examples generated from specific industrial scenarios and are meant as references for:

- understanding the expected input format, and  
- validating the structure of your own outputs when integrating with optEngine or when running locally.


### Data and examples

Reference JSON examples and industrial input data (distance matrices, container and KH templates) for the real-world MODAPTO application can be obtained from the following Zenodo record:

[Dataset for Pick and Place Operations (Bipartite Travelling Salesman Problem - BTSP)
](https://zenodo.org/records/17640037)

You can connect these JSONs directly into this service (either via optEngine or via local execution) to reproduce the optimization and simulation scenarios.


## Authors
The persons who contributed to this project are Konstantinos Giannakos, Dimitrios Tsakoumis, Gregory Koronakos, Stathis Plitsos and Pavlos Eirinakis.

## Acknowledgement
This research work has been conducted within the framework of the MODAPTO project (MODULAR MANUFACTURING AND DISTRIBUTED CONTROL VIA INTEROPERABLE DIGITAL TWINS), which has received funding from the European Union’s Horizon Europe research and innovation program under grant agreement No 101091996.
<https://modapto.eu/>

## License
robot-picking-seq-opt (c) by the University of Piraeus, Greece.

robot-picking-seq-opt is licensed under a
Creative Commons Attribution-NonCommercial-NoDerivs 3.0 Unported License.

You should have received a copy of the license along with this
work.  If not, see <http://creativecommons.org/licenses/by-nc-nd/3.0/>.

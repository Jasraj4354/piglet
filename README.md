![banner](./banner.png)

# Piglet

Piglet is a library of search algorithms that you can not only readily use, but incorporate into your application.

## Requirements

python >= 3.8

pyyaml == 6.0.2

## Install

1. Clone the repo to your machine
2. Run:

```
$ python setup.py install
```

## Usage

### Commandline Interface

```
$ piglet.py --help
```

run a scenario:

```
$ python piglet.py -p ./example/example_n_puzzle_scenario.scen -f graph -s uniform
```

### Generating search traces

Use search traces to analyse and debug algorithms in [Posthoc](https://posthoc.pathfinding.ai). Add the `--log trace` argument to make Piglet output search traces.

```bash
python piglet.py -p ./example/arena2.min.scen -f graph -s a-star --log trace
```

### Piglet Library

Piglet provides a variety of flexible search algorithms. These algorithms are
able to help you to build your application.

#### Example

To use an algorithm you need a domain instance, an expander instance and a search instance.

```python
import os,sys
from lib_piglet.domains import gridmap
from lib_piglet.expanders.grid_expander import grid_expander
from lib_piglet.search.tree_search import tree_search
from lib_piglet.utils.data_structure import bin_heap,stack,queue

mapfile = "./example/gridmap/empty-16-16.map"

# create an instance of gridmap domain
gm = gridmap.gridmap(mapfile)

# create an instance of grid_expander and pass the girdmap instance to the expander.
expander = grid_expander(gm)

# create an instance of tree_search, and pass an open list (we use a binary heap here)
# and the expander to it.
search = tree_search(bin_heap(), expander)

# start search by proving a start state and goal state. For gridmap a state is a (x,y) tuple
solution = search.get_path((1,2),(10,2))

# print solution
print(solution)

```

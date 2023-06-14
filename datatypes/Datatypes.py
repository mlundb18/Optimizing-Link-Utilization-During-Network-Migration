from dataclasses import dataclass
from typing import List
import networkx as nx


@dataclass
class Flow:
    initial_path: list
    final_path: list
    demand: int

@dataclass
class TrafficSystem:
    flows: list
    topology: nx.Graph


@dataclass
class UpdateSequence:  #this is wip no hate
    split_ratio: List[float]


path0 = [1,2,3]
path1 = [3,2,1]


flow = Flow(path0, path1, 0)

T = TrafficSystem({0:flow}, nx.Graph())
def main():
    print(T.flows[0].initial_path)

if __name__ == "__main__":
    main()
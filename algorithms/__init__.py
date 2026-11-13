from algorithms.maxflow.dinic import Dinic
from algorithms.maxflow.ford_fulkerson import FordFulkerson
from algorithms.maxflow.push_relabel import PushRelabel
from algorithms.registry import AlgorithmRegistry

AlgorithmRegistry.register("ford_fulkerson", FordFulkerson)
AlgorithmRegistry.register("dinic", Dinic)
AlgorithmRegistry.register("push_relabel", PushRelabel)

AlgorithmRegistry.register_alias("max_flow", "ford_fulkerson")
AlgorithmRegistry.register_alias("dinic_flow", "dinic")
AlgorithmRegistry.register_alias("push_relabel_flow", "push_relabel")
from algorithms.maxflow.ford_fulkerson import FordFulkerson
from algorithms.registry import AlgorithmRegistry

AlgorithmRegistry.register("ford_fulkerson", FordFulkerson)
AlgorithmRegistry.register_alias("max_flow", "ford_fulkerson")
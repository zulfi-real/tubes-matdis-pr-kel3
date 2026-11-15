from collections import deque
import networkx as nx
from core.base_algorithm import BaseGraphAlgorithm
from core.graph_model import SpatialGraphModel


class Dinic(BaseGraphAlgorithm):
    """Algoritma Advanced Maximum Flow (Dinic's Algorithm dengan Level Graph & Blocking Flow)."""

    def __init__(self, model: SpatialGraphModel):
        super().__init__(model)
        self.residual = nx.DiGraph()
        self.level = {}

    def _bfs(self, source, sink) -> bool:
        self.level = {node: -1 for node in self.residual.nodes()}
        self.level[source] = 0
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in self.residual.neighbors(u):
                capacity = self.residual[u][v].get("capacity", 0.0)
                if self.level[v] < 0 and capacity > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[sink] >= 0

    def _dfs(self, u, sink, pushed, ptr) -> float:
        if pushed == 0:
            return 0.0
        if u == sink:
            return pushed

        neighbors = list(self.residual.neighbors(u))
        while ptr[u] < len(neighbors):
            v = neighbors[ptr[u]]
            if self.level[u] + 1 == self.level[v]:
                capacity = self.residual[u][v].get("capacity", 0.0)
                if capacity > 0:
                    tr = min(pushed, capacity)
                    flow_pushed = self._dfs(v, sink, tr, ptr)
                    if flow_pushed > 0:
                        self.residual[u][v]["capacity"] -= flow_pushed
                        self.residual[v][u]["capacity"] += flow_pushed
                        return flow_pushed
            ptr[u] += 1
        return 0.0

    def run(self, source_node: int, sink_node: int) -> tuple:
        self.residual.clear()
        self.residual.add_nodes_from(self.graph.nodes())

        for u, v, data in self.graph.edges(data=True):
            cap = float(data.get("capacity", data.get("weight", 1.0)))
            self.residual.add_edge(u, v, capacity=cap)
            if not self.residual.has_edge(v, u):
                self.residual.add_edge(v, u, capacity=0.0)

        max_flow = 0.0

        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={"source": source_node, "sink": sink_node, "max_flow": 0.0},
        )

        while self._bfs(source_node, sink_node):
            ptr = {node: 0 for node in self.residual.nodes()}
            while True:
                push = self._dfs(source_node, sink_node, float("inf"), ptr)
                if push == 0:
                    break
                max_flow += push
                self.log_step(
                    event_type="BLOCKING_FLOW_AUGMENTED",
                    state_mutations={"flow_added": push, "current_max_flow": max_flow},
                )

        return [], float(max_flow)

    def handle_dynamic_event(self, event_data: dict) -> tuple:
        
        edge = event_data.get("edge")
        new_capacity = event_data.get("new_weight", event_data.get("new_capacity", 0.0))
        start_node = event_data.get("start")
        goal_node = event_data.get("goal")

        if edge and self.graph.has_edge(edge[0], edge[1]):
            self.graph[edge[0]][edge[1]]["capacity"] = float(new_capacity)

        new_flow = self.run(start_node, goal_node)[1]
        return [], float(new_flow)
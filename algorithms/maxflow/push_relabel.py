from collections import deque
import networkx as nx
from core.base_algorithm import BaseGraphAlgorithm
from core.graph_model import SpatialGraphModel


class PushRelabel(BaseGraphAlgorithm):
    """Algoritma Advanced Maximum Flow (Push-Relabel / Preflow-Push Variant)."""

    def __init__(self, model: SpatialGraphModel):
        super().__init__(model)
        self.residual = nx.DiGraph()
        self.height = {}
        self.excess = {}

    def run(self, source_node: int, sink_node: int) -> tuple:
        self.residual.clear()
        self.residual.add_nodes_from(self.graph.nodes())

        for u, v, data in self.graph.edges(data=True):
            cap = float(data.get("capacity", data.get("weight", 1.0)))
            self.residual.add_edge(u, v, capacity=cap)
            if not self.residual.has_edge(v, u):
                self.residual.add_edge(v, u, capacity=0.0)

        nodes = list(self.residual.nodes())
        n = len(nodes)

        self.height = {node: 0 for node in nodes}
        self.excess = {node: 0.0 for node in nodes}

        self.height[source_node] = n

        self.log_step(
            event_type="INITIALIZATION",
            state_mutations={"source": source_node, "sink": sink_node, "max_flow": 0.0},
        )

        for v in list(self.residual.neighbors(source_node)):
            cap = self.residual[source_node][v]["capacity"]
            if cap > 0:
                self.residual[source_node][v]["capacity"] = 0.0
                self.residual[v][source_node]["capacity"] += cap
                self.excess[v] += cap
                self.excess[source_node] -= cap

        active = deque([v for v in nodes if v != source_node and v != sink_node and self.excess[v] > 0])

        def push(u, v):
            send = min(self.excess[u], self.residual[u][v]["capacity"])
            self.residual[u][v]["capacity"] -= send
            self.residual[v][u]["capacity"] += send
            self.excess[u] -= send
            self.excess[v] += send
            if v != source_node and v != sink_node and v not in active and self.excess[v] > 0:
                active.append(v)

        def relabel(u):
            min_height = float("inf")
            for v in self.residual.neighbors(u):
                if self.residual[u][v]["capacity"] > 0:
                    min_height = min(min_height, self.height[v])
            if min_height < float("inf"):
                self.height[u] = min_height + 1

        while active:
            u = active.popleft()
            old_excess = self.excess[u]
            
            # Coba dorong aliran (push) ke tetangga yang lebih rendah
            pushed = False
            for v in list(self.residual.neighbors(u)):
                if self.excess[u] > 0 and self.residual[u][v]["capacity"] > 0 and self.height[u] == self.height[v] + 1:
                    push(u, v)
                    if self.excess[u] == 0:
                        pushed = True
                        break

            if self.excess[u] > 0:
                # Jika tidak bisa push, lakukan relabel
                relabel(u)
                active.append(u)

            if self.excess[u] != old_excess:
                self.log_step(
                    event_type="PUSH_RELABEL_STEP",
                    state_mutations={"active_node": u, "excess": self.excess[u]},
                )

        max_flow = self.excess[sink_node]

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
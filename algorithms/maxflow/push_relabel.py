"""Max flow dengan algoritma Push-Relabel (Preflow-Push), murni Python."""
from __future__ import annotations

import os
import sys
from collections import deque
from typing import Dict, List, Optional, Set

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from algorithms.maxflow.maxflow_core import (
    EPS,
    Edge,
    LogFn,
    MaxFlowResult,
    _build,
    _finish,
    _log_done,
    _name,
    _num,
)


def push_relabel(
    edges: List[Edge],
    s: int,
    t: int,
    labels: Optional[dict] = None,
    log: LogFn = None,
    unit: str = "truk/hari",
) -> MaxFlowResult:
    cap, orig = _build(edges)
    steps: List[dict] = []

    if s == t:
        res = _finish(cap, orig, s, steps)
        _log_done(log, labels, res, unit)
        return res

    nodes: Set[int] = {s, t}
    for u, v in orig:
        nodes.add(u)
        nodes.add(v)

    n = len(nodes)
    height: Dict[int, int] = {u: 0 for u in nodes}
    excess: Dict[int, float] = {u: 0.0 for u in nodes}
    height[s] = n

    if log:
        log(
            "INITIALIZE",
            f"Set aliran awal dari {_name(labels, s)} ke {_name(labels, t)} = 0, "
            f"tinggi sumber = {n}. Jumlah sisi = {len(orig)}.",
            source=s,
            sink=t,
            height=n,
        )

    active: deque[int] = deque()
    in_queue: Set[int] = set()

    for v, c in list(cap[s].items()):
        if c > EPS and v != s:
            cap[s][v] -= c
            cap[v][s] += c
            excess[v] += c
            excess[s] -= c
            steps.append({"action": "PREFLOW", "u": s, "v": v, "delta": c})
            if log:
                log(
                    "PREFLOW",
                    f"Preflow awal {_name(labels, s)} -> {_name(labels, v)} "
                    f"sebesar {_num(c)} {unit}.",
                    u=s,
                    v=v,
                    delta=c,
                )
            if v != s and v != t and v not in in_queue:
                active.append(v)
                in_queue.add(v)

    while active:
        u = active.popleft()
        in_queue.discard(u)

        while excess[u] > EPS:
            pushed = False
            for v, r_cap in list(cap[u].items()):
                if v == u:
                    continue
                if r_cap > EPS and height[u] == height[v] + 1:
                    delta = min(excess[u], r_cap)
                    cap[u][v] -= delta
                    cap[v][u] += delta
                    excess[u] -= delta
                    excess[v] += delta
                    pushed = True
                    steps.append({"action": "PUSH", "u": u, "v": v, "delta": delta})

                    if log:
                        log(
                            "PUSH",
                            f"Push {_num(delta)} {unit} dari {_name(labels, u)} ke {_name(labels, v)} "
                            f"(sisa excess {_name(labels, u)} = {_num(excess[u])}).",
                            u=u,
                            v=v,
                            delta=delta,
                            excess=excess[u],
                        )

                    if v != s and v != t and v not in in_queue and excess[v] > EPS:
                        active.append(v)
                        in_queue.add(v)

                    if excess[u] <= EPS:
                        break

            if excess[u] > EPS and not pushed:
                min_h = min(
                    (height[v] for v, r_cap in cap[u].items() if v != u and r_cap > EPS),
                    default=None,
                )
                if min_h is None:
                    break
                old_h = height[u]
                height[u] = min_h + 1
                steps.append(
                    {
                        "action": "RELABEL",
                        "u": u,
                        "old_height": old_h,
                        "new_height": height[u],
                    }
                )
                if log:
                    log(
                        "RELABEL",
                        f"Relabel {_name(labels, u)}: tinggi naik dari {old_h} menjadi {height[u]}.",
                        u=u,
                        old_height=old_h,
                        new_height=height[u],
                    )

    res = _finish(cap, orig, s, steps)
    _log_done(log, labels, res, unit)
    return res


try:
    from algorithms.maxflow._flow_adapter import FlowAdapter
    from algorithms.registry import AlgorithmRegistry

    class PushRelabelMaxFlow(FlowAdapter):
        def _solve(self, edges, s, t, labels, log):
            return push_relabel(edges, s, t, labels, log)

    AlgorithmRegistry.register("push_relabel", PushRelabelMaxFlow)
except ImportError:
    pass


if __name__ == "__main__":
    labels = {
        0: "Suplai_Truk",
        1: "Gerbang_Kawasan",
        2: "Jl_Yos_Sudarso",
        3: "Jl_Cilincing",
        4: "Gerbang_NPCT1",
    }
    edges = [
        (0, 1, 4000),
        (1, 2, 1500),
        (1, 3, 1000),
        (2, 4, 1500),
        (3, 4, 1000),
    ]

    def print_log(action, narrative, **data):
        print(f"[{action}] {narrative}")

    hasil = push_relabel(edges, s=0, t=4, labels=labels, log=print_log)
    print("\n--- RINGKASAN ---")
    print("Aliran Maksimum :", hasil.value, "truk/hari")
    print("Sisi Min-Cut    :", hasil.cut_edges)

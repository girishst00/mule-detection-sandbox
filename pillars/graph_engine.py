import networkx as nx
from typing import Dict, List

class GraphIntelligenceEngine:
    """
    Pillar 2: Constructs transaction and entity graphs to uncover 
    fan-in (funnel accounts), fan-out, and structural centrality shifts.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def ingest_edges(self, edges: List[Dict]):
        """Edges format: [{'source': 'acc_A', 'target': 'acc_B', 'amount': 15000}]"""
        for edge in edges:
            self.graph.add_edge(
                edge["source"], 
                edge["target"], 
                weight=edge.get("amount", 1.0)
            )

    def analyze_node_topology(self, account_id: str) -> Dict:
        if account_id not in self.graph:
            return {"structural_risk": 0.0, "topology_notes": ["Account not found in active graph network."]}

        # In-degree vs Out-degree (Fan-in / Fan-out analysis)
        in_deg = self.graph.in_degree(account_id)
        out_deg = self.graph.out_degree(account_id)
        
        # Centrality Metrics
        pagerank = nx.pagerank(self.graph, alpha=0.85).get(account_id, 0.0)
        
        structural_risk = 0.0
        notes = []

        # Funnel / Collection account pattern (Fan-in)
        if in_deg >= 10 and out_deg <= 2:
            structural_risk += 0.6
            notes.append(f"Fan-in funnel topology detected: {in_deg} inbound senders to {out_deg} outflow.")
        
        # Dispersion pipeline pattern (Fan-out)
        elif out_deg >= 10 and in_deg <= 2:
            structural_risk += 0.6
            notes.append(f"Fan-out dispersion topology detected: {out_deg} outflow recipients from {in_deg} inflow.")

        if pagerank > 0.05:
            structural_risk += 0.3
            notes.append(f"Elevated PageRank centrality score: {pagerank:.4f}")

        return {
            "account_id": account_id,
            "structural_risk_score": min(structural_risk, 1.0),
            "in_degree": in_deg,
            "out_degree": out_deg,
            "pagerank": pagerank,
            "topology_notes": notes
        }
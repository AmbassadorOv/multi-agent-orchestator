from logic_engine.connectivity import build_base_connectivity

def test_connectivity_has_22_nodes_and_edges():
    g = build_base_connectivity()
    assert g.as_dict()["node_count"] == 22
    assert g.as_dict()["edge_count"] > 0

def test_propagation_moves_activation():
    g = build_base_connectivity()
    assert g.propagate({"א": 1.0}, relation="adjacency")["ב"] == 1.0

def test_source_claims_are_tagged():
    g = build_base_connectivity()
    assert all(e.status == "SOURCE_CLAIM" for e in g.edges("numeric_equivalence"))

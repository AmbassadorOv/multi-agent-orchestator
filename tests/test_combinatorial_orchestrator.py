from logic_engine import CombinationEngine, HEBREW_22, NeuralLogicOrchestrator, OrchestrationRequest, THOUGHT_MODES_28

def test_alphabet_has_22_base_letters():
    assert len(HEBREW_22) == 22
    assert len({n.symbol for n in HEBREW_22}) == 22

def test_combination_and_permutation_counts():
    engine=CombinationEngine([n.symbol for n in HEBREW_22])
    assert engine.combination_count(2)==231
    assert engine.permutation_count(2)==462

def test_28_modes_are_stable():
    assert len(THOUGHT_MODES_28)==28
    assert THOUGHT_MODES_28[0].mode_id=="TM-01"
    assert THOUGHT_MODES_28[-1].mode_id=="TM-28"

def test_orchestrator_builds_traceable_form_object():
    result=NeuralLogicOrchestrator().prepare(
        OrchestrationRequest("בדיקת צירוף",("א","ב","ג"),"TM-13",2,max_preview=4)
    )
    assert result.normalized_letters==("א","ב","ג")
    assert result.combinatorics["combination_count"]==3
    assert result.combinatorics["permutation_count"]==6
    assert len(result.combinatorics["combination_preview"])==3
    assert result.trace[-1]["status"]=="READY_FOR_NEURAL_LAYER"

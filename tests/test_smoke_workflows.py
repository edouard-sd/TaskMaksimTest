from scripts.smoke_test_workflows import build_persona_task, load_benchmarks, load_concept, recommend_rsp


def test_sample_inputs_support_smoke_workflow():
    concept = load_concept()
    benchmarks = load_benchmarks()
    rsp = recommend_rsp(concept, benchmarks)
    persona_task = build_persona_task()

    assert concept.name == "Protein Coffee"
    assert len(benchmarks) == 2
    assert rsp.currency == "USD"
    assert rsp.low_range <= rsp.recommended_rsp <= rsp.high_range
    assert persona_task.task_type == "website_review"

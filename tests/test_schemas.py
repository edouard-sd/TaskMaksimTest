from nestle_automation_schemas import (
    BenchmarkProduct,
    Concept,
    PersonaProfile,
    PersonaTask,
    PriceObservation,
    RSPRecommendation,
)


def test_rsp_recommendation_normalizes_currency():
    recommendation = RSPRecommendation(
        concept_id="concept-1",
        market="UK",
        currency="gbp",
        recommended_rsp=2.49,
        low_range=2.29,
        high_range=2.79,
        confidence="medium",
        rationale="Anchored to similar peer products with a modest benefit premium.",
    )

    assert recommendation.currency == "GBP"


def test_benchmark_product_accepts_price_observations():
    product = BenchmarkProduct(
        product_id="peer-1",
        name="Peer Bar",
        brand="Example",
        category="snacks",
        market="UK",
        prices=[
            PriceObservation(
                source_name="Retailer",
                price=1.25,
                currency="gbp",
                pack_size=40,
                pack_unit="g",
            )
        ],
    )

    assert product.prices[0].currency == "GBP"


def test_persona_task_embeds_profile():
    persona = PersonaProfile(
        persona_id="persona-1",
        name="Busy parent",
        market="US",
        goals=["Find convenient family snacks"],
    )
    task = PersonaTask(
        task_id="task-1",
        persona=persona,
        task_type="website_review",
        objective="Evaluate whether the product page is easy to understand.",
        target_url="https://example.com",
    )

    assert task.persona.persona_id == "persona-1"


def test_concept_minimum_contract():
    concept = Concept(
        concept_id="concept-1",
        name="Protein Coffee",
        category="beverages",
        market="US",
        description="A chilled coffee with added protein.",
        target_audience="Busy professionals",
    )

    assert concept.benefits == []

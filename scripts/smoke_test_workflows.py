"""Smoke-test the initial Nestle automation schemas with sample workflow inputs.

This script does not call external AI, retailer, or video APIs. It verifies that
local contracts can load realistic inputs and create representative downstream
objects for the three scoped workflows.
"""

from __future__ import annotations

import json
from pathlib import Path

from nestle_automation_schemas import (
    BenchmarkProduct,
    BrandGuidelines,
    Concept,
    ConceptVideoBrief,
    PersonaProfile,
    PersonaTask,
    PriceObservation,
    RSPRecommendation,
)

ROOT = Path(__file__).resolve().parents[1]


def load_concept() -> Concept:
    data = json.loads((ROOT / "examples" / "sample_concept.json").read_text())
    guidelines = BrandGuidelines(**data.pop("brand_guidelines"))
    return Concept(**data, brand_guidelines=guidelines)


def load_benchmarks() -> list[BenchmarkProduct]:
    raw_products = json.loads((ROOT / "examples" / "sample_benchmark.json").read_text())
    products: list[BenchmarkProduct] = []
    for raw_product in raw_products:
        prices = [PriceObservation(**price) for price in raw_product.pop("prices")]
        products.append(BenchmarkProduct(**raw_product, prices=prices))
    return products


def recommend_rsp(concept: Concept, products: list[BenchmarkProduct]) -> RSPRecommendation:
    weighted_prices = []
    for product in products:
        if not product.prices or product.similarity_score is None:
            continue
        weighted_prices.append((product.prices[0].price, product.similarity_score))

    total_weight = sum(weight for _, weight in weighted_prices)
    weighted_anchor = sum(price * weight for price, weight in weighted_prices) / total_weight
    recommendation = round(weighted_anchor + 0.20, 2)

    return RSPRecommendation(
        concept_id=concept.concept_id,
        market=concept.market,
        currency="usd",
        recommended_rsp=recommendation,
        low_range=round(recommendation - 0.30, 2),
        high_range=round(recommendation + 0.30, 2),
        confidence="medium",
        rationale="Smoke-test recommendation anchored to similarity-weighted peer prices plus a small benefit premium.",
        assumptions=["Sample retailer data only", "No promotional adjustment applied"],
        benchmark_product_ids=[product.product_id for product in products],
    )


def build_persona_task() -> PersonaTask:
    persona = PersonaProfile(
        persona_id="persona-busy-professional-us",
        name="Busy US professional",
        market="US",
        goals=["Find convenient products that fit a hectic morning routine"],
        shopping_behaviors=["Compares benefits quickly", "Looks for clear pack claims"],
        digital_fluency="high",
        decision_heuristics=["Prioritizes convenience", "Avoids confusing claims"],
    )
    return PersonaTask(
        task_id="task-review-product-page",
        persona=persona,
        task_type="website_review",
        objective="Review a product page from the persona's perspective and flag unclear value propositions.",
        target_url="https://example.com/product-page",
        success_criteria=["Identifies main benefit", "Notes trust concerns", "Suggests improvements"],
    )


def main() -> None:
    concept = load_concept()
    video_brief = ConceptVideoBrief(
        concept=concept,
        objective="Introduce the concept for internal stakeholder review",
        duration_seconds=20,
        aspect_ratio="16:9",
        call_to_action="Learn more in concept testing",
    )
    benchmarks = load_benchmarks()
    rsp = recommend_rsp(concept, benchmarks)
    persona_task = build_persona_task()

    print("OK: concept loaded ->", concept.name)
    print("OK: video brief created ->", f"{video_brief.duration_seconds}s", video_brief.aspect_ratio)
    print("OK: benchmarks loaded ->", len(benchmarks), "peer products")
    print("OK: RSP recommendation ->", rsp.currency, rsp.recommended_rsp, f"({rsp.low_range}-{rsp.high_range})")
    print("OK: persona task created ->", persona_task.persona.name, persona_task.task_type)


if __name__ == "__main__":
    main()

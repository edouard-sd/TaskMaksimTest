"""Versioned data contracts for automation workflows.

These dataclasses define provider-neutral inputs and outputs for concept videos,
benchmarking and RSP recommendations, and synthetic persona-agent tasks. They
use only the Python standard library so the contracts can be imported in early
prototypes before a full service framework is installed.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal


class AssetType(str, Enum):
    """Supported concept asset types."""

    PRODUCT_IMAGE = "product_image"
    PACKSHOT = "packshot"
    LOGO = "logo"
    LIFESTYLE_IMAGE = "lifestyle_image"
    GUIDELINE = "guideline"


@dataclass(slots=True)
class ConceptAsset:
    """Reusable reference to a generated or approved concept asset."""

    asset_id: str
    asset_type: AssetType
    uri: str
    description: str | None = None
    rights_notes: str | None = None


@dataclass(slots=True)
class BrandGuidelines:
    """Brand and market rules used by generation and QA steps."""

    brand_name: str
    market: str
    tone_of_voice: list[str] = field(default_factory=list)
    required_disclaimers: list[str] = field(default_factory=list)
    forbidden_claims: list[str] = field(default_factory=list)
    color_palette: list[str] = field(default_factory=list)
    logo_usage_rules: list[str] = field(default_factory=list)
    source_uris: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Concept:
    """Normalized product concept input shared by all workflows."""

    concept_id: str
    name: str
    category: str
    market: str
    description: str
    target_audience: str
    benefits: list[str] = field(default_factory=list)
    reasons_to_believe: list[str] = field(default_factory=list)
    assets: list[ConceptAsset] = field(default_factory=list)
    brand_guidelines: BrandGuidelines | None = None


@dataclass(slots=True)
class ConceptVideoBrief:
    """Provider-neutral brief for automated marketing video generation."""

    concept: Concept
    objective: str
    duration_seconds: int
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:5"] = "16:9"
    channel: str = "internal_review"
    call_to_action: str | None = None
    creative_mandatories: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not 5 <= self.duration_seconds <= 60:
            raise ValueError("duration_seconds must be between 5 and 60")


@dataclass(slots=True)
class PriceObservation:
    """Single price evidence point for a peer product."""

    source_name: str
    price: float
    currency: str
    pack_size: float
    pack_unit: str
    observed_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    promotion_notes: str | None = None
    source_url: str | None = None

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("price must be positive")
        if self.pack_size <= 0:
            raise ValueError("pack_size must be positive")
        self.currency = self.currency.upper()
        if len(self.currency) != 3:
            raise ValueError("currency must be an ISO 4217 code")


@dataclass(slots=True)
class BenchmarkProduct:
    """Comparable product used for benchmark and RSP analysis."""

    product_id: str
    name: str
    brand: str
    category: str
    market: str
    claims: list[str] = field(default_factory=list)
    format: str | None = None
    target_audience: str | None = None
    similarity_score: float | None = None
    similarity_rationale: list[str] = field(default_factory=list)
    prices: list[PriceObservation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.similarity_score is not None and not 0 <= self.similarity_score <= 1:
            raise ValueError("similarity_score must be between 0 and 1")


@dataclass(slots=True)
class RSPRecommendation:
    """Audit-friendly retail selling price recommendation."""

    concept_id: str
    market: str
    currency: str
    recommended_rsp: float
    low_range: float
    high_range: float
    confidence: Literal["low", "medium", "high"]
    rationale: str
    assumptions: list[str] = field(default_factory=list)
    benchmark_product_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.currency = self.currency.upper()
        if len(self.currency) != 3:
            raise ValueError("currency must be an ISO 4217 code")
        if min(self.recommended_rsp, self.low_range, self.high_range) <= 0:
            raise ValueError("RSP values must be positive")
        if not self.low_range <= self.recommended_rsp <= self.high_range:
            raise ValueError("recommended_rsp must be within low_range and high_range")


@dataclass(slots=True)
class PersonaProfile:
    """Executable synthetic persona profile for agent workflows."""

    persona_id: str
    name: str
    market: str
    demographics: dict[str, Any] = field(default_factory=dict)
    goals: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    shopping_behaviors: list[str] = field(default_factory=list)
    digital_fluency: Literal["low", "medium", "high"] = "medium"
    accessibility_needs: list[str] = field(default_factory=list)
    decision_heuristics: list[str] = field(default_factory=list)
    source_research_refs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PersonaTask:
    """Task assigned to a persona agent."""

    task_id: str
    persona: PersonaProfile
    task_type: Literal["website_review", "app_test", "gameplay", "portal_evaluation"]
    objective: str
    target_url: str | None = None
    success_criteria: list[str] = field(default_factory=list)
    max_steps: int = 30

    def __post_init__(self) -> None:
        if not 1 <= self.max_steps <= 500:
            raise ValueError("max_steps must be between 1 and 500")

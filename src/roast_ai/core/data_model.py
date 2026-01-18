from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EarlyGameStats:
    """Calculates metrics for the critical first 3 minutes."""
    cs_at_3: int
    xp_at_3: int
    deaths_at_3: int
    gold_diff_at_3: int

@dataclass
class AwarenessStats:
    """The 'Surgical' Map Awareness Pillar."""
    deaths_near_vision: int
    vision_timer: float
    objective_rotation_delay: float

@dataclass
class PerformancePillars:
    """The three 'Objective Truth' categories."""
    efficiency: float  # Gold per minute
    teamwork: float    # Kill participation %
    safety: float      # Vision score per minute

@dataclass
class MatchTruth:
    """The complete analysis package for the AI."""
    is_leaver: bool
    is_weakest_link: bool
    lobby_avg_mmr: str
    pillars: PerformancePillars
    early_game: EarlyGameStats
    awareness: AwarenessStats
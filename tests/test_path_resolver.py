"""Tests for centralized default path resolution."""

from __future__ import annotations

from pathlib import Path

from quizz.config import AppSettings
from quizz.services.path_resolver import DefaultPathResolver


def test_default_player_answers_path_uses_slug(tmp_path: Path) -> None:
    """Player default answers path should be name-based and filesystem-safe."""

    resolver = DefaultPathResolver(AppSettings(data_dir=tmp_path))

    result = resolver.default_player_answers_path("Alice Smith")

    assert result == tmp_path / "alice-smith_answers.yaml"


def test_default_impersonation_path_uses_both_names(tmp_path: Path) -> None:
    """Impersonation path should include both impersonator and impersonatee names."""

    resolver = DefaultPathResolver(AppSettings(data_dir=tmp_path))

    result = resolver.default_impersonator_answers_path("Alice Smith", "Bob")

    assert result == tmp_path / "alice-smith_as_bob_answers.yaml"

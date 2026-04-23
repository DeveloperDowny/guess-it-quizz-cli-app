"""Default file path generation for CLI flags."""

from __future__ import annotations

import re
from pathlib import Path

from quizz.config import AppSettings


class DefaultPathResolver:
    """Resolve shared default paths for player and judge apps."""

    def __init__(self, settings: AppSettings) -> None:
        """Initialize the resolver.

        Args:
            settings: Application settings object.
        """

        self._settings = settings

    def default_player_answers_path(self, player_name: str) -> Path:
        """Return default path for a player's own answers.

        Args:
            player_name: Player identifier.

        Returns:
            Path: Default answers path.
        """

        slug = self._slugify(player_name)
        return self._settings.data_dir / f"{slug}_answers.yaml"

    def default_impersonator_answers_path(
        self,
        impersonator_name: str,
        impersonatee_name: str,
    ) -> Path:
        """Return default path for an impersonation answer sheet.

        Args:
            impersonator_name: The player answering as someone else.
            impersonatee_name: The player being impersonated.

        Returns:
            Path: Default impersonation answers path.
        """

        impersonator_slug = self._slugify(impersonator_name)
        impersonatee_slug = self._slugify(impersonatee_name)
        return self._settings.data_dir / f"{impersonator_slug}_as_{impersonatee_slug}_answers.yaml"

    @staticmethod
    def _slugify(name: str) -> str:
        """Convert a user-supplied name to filesystem-safe slug."""

        candidate = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
        return candidate or "player"

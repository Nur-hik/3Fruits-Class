"""Logika bebas-hardware yang dapat diuji untuk pipeline AIoT."""

from dataclasses import dataclass
from typing import Mapping, Optional


def command_for_prediction(
    label: str,
    confidence: float,
    threshold: float,
    command_by_class: Mapping[str, str],
    off_command: str = "0",
) -> str:
    """Ubah hasil model menjadi perintah relay yang aman.

    Prediksi di bawah ambang batas atau kelas yang tidak dipetakan selalu
    menghasilkan perintah OFF.
    """
    if confidence < threshold:
        return off_command
    return command_by_class.get(label.lower(), off_command)


@dataclass
class CommandStabilizer:
    """Terima perubahan state hanya setelah muncul pada N frame berurutan."""

    min_consecutive_frames: int = 3
    stable_command: Optional[str] = None
    _candidate: Optional[str] = None
    _candidate_count: int = 0

    def __post_init__(self) -> None:
        if self.min_consecutive_frames < 1:
            raise ValueError("min_consecutive_frames harus minimal 1")

    def update(self, command: str) -> Optional[str]:
        """Kembalikan perintah baru hanya saat state stabil benar-benar berubah."""
        if command == self._candidate:
            self._candidate_count += 1
        else:
            self._candidate = command
            self._candidate_count = 1

        if (
            self._candidate_count >= self.min_consecutive_frames
            and command != self.stable_command
        ):
            self.stable_command = command
            return command
        return None

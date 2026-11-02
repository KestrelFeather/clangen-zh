"""Keep full-suite runs isolated from player saves and explicit about locale."""
import os
from pathlib import Path
import random

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault(
    "CLANGEN_ZH_DATA_DIR",
    str(
        Path(__file__).resolve().parents[1]
        / ".localization-work"
        / f"suite-data-{os.getpid()}"
    ),
)
(Path(os.environ["CLANGEN_ZH_DATA_DIR"]) / "saves").mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser):
    parser.addoption("--game-locale", choices=("zh", "en"), default="zh")


def pytest_configure(config):
    random.seed(42)


@pytest.fixture(autouse=True)
def game_locale(request):
    import i18n

    previous = i18n.config.get("locale")
    i18n.set("locale", request.config.getoption("--game-locale"))
    yield
    i18n.set("locale", previous)

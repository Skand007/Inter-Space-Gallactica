import os
import json
import pygame
from settings import ASSETS_DIR, SCORES_PATH


def asset_path(filename: str) -> str:
    return os.path.join(ASSETS_DIR, filename)


def load_image(name: str, size=None, rotate=None):
    img = pygame.image.load(asset_path(name)).convert_alpha()
    if size is not None:
        img = pygame.transform.scale(img, size)
    if rotate is not None:
        img = pygame.transform.rotate(img, rotate)
    return img


def load_sound(name: str):
    return pygame.mixer.Sound(asset_path(name))


def ensure_scores_file():
    if not os.path.exists(SCORES_PATH):
        with open(SCORES_PATH, "w") as f:
            json.dump({}, f)


def load_scores():
    ensure_scores_file()
    try:
        with open(SCORES_PATH, "r") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        return {}


def save_scores(scores: dict):
    with open(SCORES_PATH, "w") as f:
        json.dump(scores, f, indent=2)

import time

import logging
import os
from pathlib import Path
from typing import TypeVar

import numpy as np
import pytest
from PIL import Image, ImageChops

logging.basicConfig(level=logging.INFO, format=r"[%(levelname)s] %(message)s")

BASELINE_IMG_DIR = Path(__file__).resolve().parent / "baseline"
CURRENT_IMG_DIR = Path(__file__).resolve().parent / "current"

if not CURRENT_IMG_DIR.exists():
    CURRENT_IMG_DIR.mkdir()
    logging.info(f"Made {CURRENT_IMG_DIR}")


WebElement = TypeVar("WebElement")


def _are_images_the_same(base: Image, other: Image, threshold: float = 0.0) -> bool:
    image_ops_diff = ImageChops.difference(base, other).getdata()
    pixel_diff = np.array(image_ops_diff).sum()
    return pixel_diff <= threshold


class _MatchingElement:
    def __init__(self, element: WebElement, name: str):
        self._element = element
        self._name = name
        self._baseline_path = BASELINE_IMG_DIR / f'{name}.png'
        self._current_path = CURRENT_IMG_DIR / f'{name}.png'

    def take_baseline_image(self):
        self._element.screenshot(str(self._baseline_path))
        logging.info(f"Captured image to {self._baseline_path}")

    def take_current_image(self):
        self._element.screenshot(str(self._current_path))

    def has_baseline(self):
        return self._baseline_path.exists()

    def match_baseline(self):
        base = Image.open(self._baseline_path)
        current = Image.open(self._current_path)
        return _are_images_the_same(base, current)


def web_element_image_regression(
    element: WebElement, name: str, wait_time: float = 5, timeout: float = 5
):
    """
    It will capture an image of the element when the environment variable UPDATE_BASELINE=1,
    otherwise it will check whether the element matches the latest image
    """
    matching_element = _MatchingElement(element, name)
    if int(os.environ.get("UPDATE_BASELINE", 0)) == 1:
        time.sleep(wait_time)
        matching_element.take_baseline_image()
    else:
        if not matching_element.has_baseline():
            logging.error(
                f"Please use UPDATE_BASELINE=1 to update the baseline image of {name} first"
            )
            pytest.fail()

        start_time = time.time()
        elapsed_time = 0

        matching_element.take_current_image()
        while not matching_element.match_baseline() and elapsed_time < timeout:
            time.sleep(0.1)
            matching_element.take_current_image()
            elapsed_time = time.time() - start_time

        assert (
            matching_element.match_baseline()
        ), f'[Visual Regression "{name}"] Images are not the same.'

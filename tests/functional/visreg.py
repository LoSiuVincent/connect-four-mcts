import inspect
import logging
import os
import time
from pathlib import Path
from typing import TypeVar

import numpy as np
import pytest
from PIL import Image, ImageChops

logging.basicConfig(level=logging.INFO, format=r'[%(levelname)s] %(message)s')

BASELINE_IMG_DIR = Path(__file__).resolve().parent / 'baseline'
CURRENT_IMG_DIR = Path(__file__).resolve().parent / 'current'

if not CURRENT_IMG_DIR.exists():
    CURRENT_IMG_DIR.mkdir()
    logging.info(f'Made {CURRENT_IMG_DIR}')


WebElement = TypeVar('WebElement')


def _get_caller_name():
    caller_frame = inspect.stack()[2]
    function_name = caller_frame.function
    return function_name


def _get_average_pixel_diff(base: Image, other: Image) -> float:
    image_ops_diff = ImageChops.difference(base, other).getdata()
    pixel_diff = np.array(image_ops_diff).sum()
    num_pixels = base.size[0] * base.size[1] * len(base.getbands())
    return pixel_diff / num_pixels


def _are_images_the_same(base: Image, other: Image, threshold: float = 0.1) -> bool:
    average_pixel_diff = _get_average_pixel_diff(base, other)
    return average_pixel_diff <= threshold


class _MatchingElement:
    def __init__(self, element: WebElement, name: str, caller: str):
        self._element = element
        self._baseline_path = BASELINE_IMG_DIR / caller / f'{name}.png'
        self._current_path = CURRENT_IMG_DIR / caller / f'{name}.png'

    def take_baseline_image(self):
        if not self._baseline_path.parent.exists():
            self._baseline_path.parent.mkdir()
        self._element.screenshot(str(self._baseline_path))
        logging.info(f'Captured image to {self._baseline_path}')

    def take_current_image(self):
        if not self._current_path.parent.exists():
            self._current_path.parent.mkdir()
        self._element.screenshot(str(self._current_path))
        logging.info(f'Captured image to {self._current_path}')

    def has_baseline(self):
        return self._baseline_path.exists()

    def match_baseline(self):
        base = Image.open(self._baseline_path)
        current = Image.open(self._current_path)
        return _are_images_the_same(base, current)

    def get_pixel_diff(self) -> float:
        base = Image.open(self._baseline_path)
        current = Image.open(self._current_path)
        return _get_average_pixel_diff(base, current)


def web_element_regression(
    element: WebElement, name: str, wait_time_before_capture: float = 0, timeout: float = 3
):
    """When the environment variable UPDATE_BASELINE=1, it will Capture an image of the element.

    Otherwise it will check whether the element matches the latest image

    Args:
        element: the webelement for the regression
        name: the image name for the regression
        wait_time: The waiting time before capturing the image (only effect when UPDATE_BASELINE=1). Defaults to 0.
        timeout: maximum wait time to match the baseline. Defaults to 3.
    """
    matching_element = _MatchingElement(element, name, _get_caller_name())
    if int(os.environ.get('UPDATE_BASELINE', 0)) == 1:
        time.sleep(wait_time_before_capture)
        matching_element.take_baseline_image()
    else:
        if not matching_element.has_baseline():
            logging.error(
                f'Please use UPDATE_BASELINE=1 to update the baseline image of {name} first'
            )
            pytest.fail()

        start_time = time.time()
        elapsed_time = 0

        matching_element.take_current_image()
        while not matching_element.match_baseline() and elapsed_time < timeout:
            pixel_diff = matching_element.get_pixel_diff()
            logging.info(f'Image not the same, average pixel diff: {pixel_diff}')

            time.sleep(0.1)
            matching_element.take_current_image()
            elapsed_time = time.time() - start_time

        is_match_baseline = matching_element.match_baseline()
        if not is_match_baseline:
            pixel_diff = matching_element.get_pixel_diff()
            pytest.fail(
                f'[Visual Regression "{name}"] Images are not the same, average pixel diff: {pixel_diff}'
            )

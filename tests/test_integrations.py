import time

import pytest
from selenium.webdriver.common.by import By

from tests.visreg import web_element_image_regression


@pytest.mark.visual
def test_coins_show_up_when_the_game_drops_the_coins(browser):
    canvas = browser.find_element(By.TAG_NAME, "canvas")
    time.sleep(1)

    browser.execute_script("game.dropCoin(0);")
    time.sleep(2)
    web_element_image_regression(canvas, "first_coin")

    browser.execute_script("game.dropCoin(3);")
    time.sleep(2)
    web_element_image_regression(canvas, "second_coin")

    browser.execute_script("game.dropCoin(0);")
    time.sleep(2)
    web_element_image_regression(canvas, "third_coin")

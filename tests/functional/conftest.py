import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BROWSER_WIDTH = 1000
BROWSER_HEIGHT = 1200


class ConnectFourTestDriver(webdriver.Firefox):
    def find_canvas(self):
        return self.find_element(By.TAG_NAME, 'canvas')

    def find_state_text(self):
        return self.find_element(By.ID, 'id-game-state-text')

    def get_cell_length(self):
        return self.execute_script('return view.getCellLength();')

    def wait_until_text_appear(self, text: str, timeout=5):
        WebDriverWait(self, timeout, poll_frequency=0.1).until(
            EC.text_to_be_present_in_element((By.ID, 'id-game-state-text'), text)
        )

    def wait_until_text_disappear(self, text: str, timeout=5):
        WebDriverWait(self, timeout, poll_frequency=0.1).until_not(
            EC.text_to_be_present_in_element((By.ID, 'id-game-state-text'), text)
        )

    def wait_until_player_turn_start(self, timeout=5):
        self.wait_until_text_appear('Your turn', timeout)

    def wait_until_player_turn_done(self, timeout=5):
        self.wait_until_text_disappear('Your turn', timeout)

    def wait_until_computer_turn_done(self, timeout=5):
        self.wait_until_text_disappear('Thinking ...', timeout)

    def click_column(self, column_index, wait_before_player_turn_start=True):
        if wait_before_player_turn_start:
            self.wait_until_player_turn_start()

        canvas = self.find_canvas()
        cell_width = self.get_cell_length()
        click_x = column_index * cell_width + 0.5 * cell_width - canvas.size['width'] / 2
        click_y = 100 - canvas.size['height'] / 2

        action = webdriver.common.action_chains.ActionChains(self)
        action.move_to_element_with_offset(canvas, click_x, click_y)
        action.click()
        action.perform()


@pytest.fixture
def browser():
    driver = ConnectFourTestDriver()
    driver.get('http://localhost:8000/test')
    driver.set_window_size(BROWSER_WIDTH, BROWSER_HEIGHT)
    yield driver
    driver.quit()

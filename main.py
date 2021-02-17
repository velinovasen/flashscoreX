from bs4 import BeautifulSoup
from time import sleep, perf_counter
import re

# from webdriver_manager.firefox import GeckoDriverManager
import csv
from selenium.webdriver import FirefoxOptions, Firefox, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities as DC
from selenium.webdriver.support.wait import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions, Chrome, ActionChains


class GameCollector:
    GAME_DIV_XPATH = '/html/body/div[5]/div[1]/div/div[1]/div[2]/div[5]/div[2]/div[2]/div/div/div'
    HEADER_WAIT_XPATH = '/html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div[2]/div/div/div[1]'
    COOKIE_BUTTON_XPATH = '/html/body/div[10]/div[3]/div/div/div[2]/div/button[1]'
    GAME_WAIT_XPATH = '/html/body/iframe    '
    TEAMS_A_LINKS_CLASS = 'participant-imglink'
    ODDS_CLASS = 'odds value'
    HOME_ODD_CLASS, DRAW_ODD_CLASS, AWAY_ODD_CLASS = 'kx o_1', 'kx o_0', 'kx o_2'

    def main(self):
        driver = self.driver_chrome()

        driver.get('https://www.flashscore.com/')

        all_games = self.gather_games(driver)

        self.scan_each_game(driver, all_games)

    def scan_each_game(self, driver, all_games):
        for game in all_games:
            # print(game.split('g_1_')[1])
            BASE_URL = f"https://www.flashscore.com/match/{game.split('g_1_')[1]}/#match-summary"
            driver.get(BASE_URL)
            sleep(3)
            # WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, self.GAME_WAIT_XPATH)))

            teams_token = driver.find_elements_by_class_name(self.TEAMS_A_LINKS_CLASS)

            home_team, away_team = teams_token[1].text, teams_token[3].text

            try:
                odds_token = driver.find_element_by_id('tab-prematch-odds').text
                print(odds_token)

            except Exception:
                home_odd, draw_odd, away_odd = '-', '-', '-'

            print(home_team, away_team)


    def gather_games(self, driver):
        # sleep(3)
        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, self.COOKIE_BUTTON_XPATH)))
        driver.find_element_by_xpath(self.COOKIE_BUTTON_XPATH).click()
        sleep(1)
        all_divs_token = driver.find_elements_by_xpath(self.GAME_DIV_XPATH)
        print(len(all_divs_token))
        all_games = []

        for div in all_divs_token:
            div_stings = div.get_attribute('outerHTML')

            if 'Click for match detail!' in div_stings:
                print(div.get_attribute('id'))
                all_games.append(div.get_attribute('id'))

        return all_games

    def driver_chrome(self):
        """
        Open and set the settings for the browser
        :param link:
        :param token:
        :return driver:
        """
        CHROME_PATH = '/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/home/velinov/Desktop/scrp-drivers/chromedriver'

        chrome_options = ChromeOptions()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.headless = False  # IF YOU WANT TO SEE THE BROWSER -> FALSE

        capa = DC.CHROME
        capa["pageLoadStrategy"] = "normal"

        driver = Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH, desired_capabilities=capa)
        driver.maximize_window()
        return driver


if __name__ == '__main__':
    scanner = GameCollector()
    scanner.main()

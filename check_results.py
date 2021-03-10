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


class CheckResults:

    def main(self):
        driver = self.driver_chrome()

        games_id = self.get_games()

        self.get_results(driver, games_id)

    def get_results(self, driver, games_id):
        for game_id in games_id:
            clean_id = game_id.split('_')[-1]
            driver.get(f'https://www.flashscore.com/match/{clean_id}/#match-summary')
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.ID, 'event_detail_current_result')))
            score_raw = driver.find_element_by_id('event_detail_current_result').text
            home_team, away_team = score_raw.split('-')[0].strip(), score_raw.split('-')[1].strip()
            print(f"home team {home_team} - {away_team} away team")

    def get_games(self):
        games = []
        with open('valuebets07.03.2021.txt') as file:
            for game in file.readlines():
                game_id = game.split(' ')[0]
                games.append(game_id)
        return games

    @staticmethod
    def driver_chrome():
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
    script = CheckResults()
    script.main()

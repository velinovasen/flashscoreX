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
    COUNTRY_TOURNAMENT_DIV_XPATH = '/html/body/div[2]/div[1]/div[2]/div[1]/span[2]'
    H2H_ID = 'a-match-head-2-head'
    HOME_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div[12]/div[2]/div[4]/div[1]/table/tbody/tr'
    AWAY_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div[12]/div[2]/div[4]/div[2]/table/tbody/tr'
    H2H_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div[12]/div[2]/div[4]/div[3]/table/tbody/tr'
    HOME_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[1]/table/tbody/tr'
    AWAY_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[2]/table/tbody/tr'
    H2H_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[3]/table/tbody/tr'

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

            date_time_token = driver.find_element_by_id('utime').text.split(' ')
            date, time = date_time_token[0], date_time_token[1]

            county_league_token = driver.find_element_by_xpath(self.COUNTRY_TOURNAMENT_DIV_XPATH).text.split(': ')
            country, league = county_league_token

            try:
                odds_token = driver.find_element_by_id('tab-prematch-odds').text.split('\n')

                home_odd, draw_odd, away_odd = odds_token[1], odds_token[3], odds_token[5]

            except Exception:
                home_odd, draw_odd, away_odd = '-', '-', '-'

            self.get_h2h(driver)

            print(country, league, date, time, home_team, away_team, home_odd, draw_odd, away_odd)

    def get_h2h(self, driver):
        try:
            driver.find_element_by_id(self.H2H_ID).click()
            sleep(1)
        except Exception:
            print('No h2h button')

        try:
            home_team_games = driver.find_elements_by_xpath(self.HOME_GAMES_XPATH)
            if len(home_team_games) >= 5:
                home_team_games = home_team_games[:-1]
            away_team_games = driver.find_elements_by_xpath(self.AWAY_GAMES_XPATH)
            if len(away_team_games) >= 5:
                away_team_games = away_team_games[:-1]
            h2h_games = driver.find_elements_by_xpath(self.H2H_GAMES_XPATH)
            if len(h2h_games) >= 5:
                h2h_games = h2h_games[:-1]

            if len(home_team_games) == 0:
                home_team_games = driver.find_elements_by_xpath(self.HOME_GAMES_XPATH_2)
                if len(home_team_games) >= 5:
                    home_team_games = home_team_games[:-1]
                away_team_games = driver.find_elements_by_xpath(self.AWAY_GAMES_XPATH_2)
                if len(away_team_games) >= 5:
                    away_team_games = away_team_games[:-1]
                h2h_games = driver.find_elements_by_xpath(self.H2H_GAMES_XPATH_2)
                if len(h2h_games) >= 5:
                    h2h_games = h2h_games[:-1]
            print(len(home_team_games), len(away_team_games), len(h2h_games))

        except Exception:
            print('Click more button error')


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
    scanner = GameCollector()
    scanner.main()

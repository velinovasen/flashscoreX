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

        games_data = self.get_games()

        self.get_results(driver, games_data)

    def get_results(self, driver, games):
        for game in games:
            clean_id = game[0].split('_')[-1]
            driver.get(f'https://www.flashscore.com/match/{clean_id}/#match-summary')
            WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.ID, 'event_detail_current_result')))
            score_raw = driver.find_element_by_id('event_detail_current_result').text
            try:
                home_team, away_team = int(score_raw.split('-')[0].strip()), int(score_raw.split('-')[1].strip())
            except:
                try:
                    home_team = int(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/span[3]/span[1]').text)
                    away_team = int(driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div[2]/div[1]/div[2]/div[1]/span[3]/span[2]/span[2]').text)
                except:
                    continue
            sign = ''
            if home_team == away_team:
                sign = 'X'
            elif home_team > away_team:
                sign = '1'
            elif home_team < away_team:
                sign = '2'

            odds_raw = str(game).split(' -> Value:')[0].split(' ')
            favourite = 'X'
            home_odds, draw_odds, away_odds = float(odds_raw[-3]), float(odds_raw[-2]), float(odds_raw[-1])
            if home_odds <= 1.80:
                favourite = '1'
            if away_odds <= 1.80:
                favourite = '2'

            final_result = 'loss'
            with open('results12.03.2021.txt', 'a') as file:
                if sign == 'X':
                    final_result = f'profit :+: {(draw_odds * 10) - 10}'
                    file.write(f"{game[1]} Score: {home_team} {away_team} Odd: {draw_odds} Favourite: {favourite} final: {final_result}")
                elif sign == '1' and abs(home_team - away_team) == 1 and favourite == '1':
                    final_result = f'profit :+: handicap -1'
                    file.write(f"{game} Score: {home_team} {away_team} Odd: {home_odds} Favourite: {favourite} final: {final_result}")
                elif sign == '2' and abs(home_team - away_team) == 1 and favourite == '2':
                    final_result = f'profit :+: handicap -1'
                    file.write(f"{game} Score: {home_team} {away_team} Odd: {away_odds} Favourite: {favourite} final: {final_result}")
                else:
                    final_result = f'loss :+: 10'
                    file.write(f"{game} Score: {home_team} {away_team} Odd: {draw_odds} Favourite: {favourite} final: {final_result}")

                file.close()

            print(f"{game} {home_team} {away_team} {draw_odds} {favourite} {final_result}")

    def get_games(self):
        games = []
        with open('valuebets12.03.2021.txt') as file:
            for game in file.readlines():
                game_id = game.split(' ')[0]
                games.append([game_id, game])
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

import datetime

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


# all_games = ['g_1_OzaZBCdm', 'g_1_4CPdbgSm', 'g_1_QwxUj2dh', 'g_1_YRFhXtQE', 'g_1_g_1_IqeVeTDH',
#              'g_1_bVESOjSp','g_1_jPPhVhkH', 'g_1_K8if632r', 'g_1_vglJ2naP', 'g_1_x480LCM3',
#              'g_1_EHZ0UYta', 'g_1_Msw9SCBB', 'g_1_rcRHQjtO', 'g_1_IkthWfCn', 'g_1_fXULPAeU',
#              'g_1_h8Y4Thd5', 'g_1_WhpdVERh', 'g_1_nwrvqrcM', 'g_1_YoILfVf4', 'g_1_AaB2mq9r',
#              'g_1_jNCQgkAA', 'g_1_feJHeBub', 'g_1_4zQ5n3Ol', 'g_1_UHFbDvwd', 'g_1_thJ2Cbh2',
#              'g_1_Y9AyL2U2', 'g_1_COVIousG', 'g_1_8h0voSiO', 'g_1_Sn2Jmggn', 'g_1_zuOG3gTO',
#              'g_1_0S0zn8xI', 'g_1_ncGb9cam', 'g_1_xdSgjJyM', 'g_1_GnRckwiS', 'g_1_MT3Qpcaq',
#              'g_1_2q5ZEPPH', 'g_1_A98sD3fU', 'g_1_A98sD3fU', 'g_1_WI9wEquO', 'g_1_ngMMVCxd',
#              'g_1_SMI4AiQh', 'g_1_MqI89Bua']
#
# with open('checked_games2021-03-06.txt', 'a') as file:
#     [file.write(game + '\n') for game in all_games]
# file.close()

class GameCollector:
    GAME_DIV_XPATH = '/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div[2]/section/div/div/div'
    HEADER_WAIT_XPATH = '/html/body/div[5]/div[1]/div/div[1]/div[2]/div[4]/div[2]/div[2]/div/div/div[1]'
    COOKIE_BUTTON_XPATH = '//*[@id="onetrust-accept-btn-handler"]'
    GAME_WAIT_XPATH = '/html/body/iframe    '
    TEAMS_A_LINKS_CLASS = 'participant-imglink'
    ODDS_CLASS = 'odds value'
    COUNTRY_TOURNAMENT_DIV_XPATH = '/html/body/div[2]/div[1]/div[2]/div[1]/span[2]'
    H2H_ID = 'a-match-head-2-head'
    HOME_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[4]/div[1]/table/tbody/tr'
    AWAY_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[4]/div[2]/table/tbody/tr'
    H2H_GAMES_XPATH = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[4]/div[3]/table/tbody/tr'
    HOME_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[1]/table/tbody/tr'
    AWAY_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[2]/table/tbody/tr'
    H2H_GAMES_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[3]/table/tbody/tr'
    HOME_HOME_XPATH = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[5]/div[1]/table/tbody/tr'
    AWAY_AWAY_XPATH = '/html/body/div[2]/div[1]/div[4]/div/div[2]/div[6]/div[1]/table/tbody/tr'
    HOME_HOME_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[5]/div[1]/table/tbody/tr'
    AWAY_AWAY_XPATH_2 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[6]/div[1]/table/tbody/tr'

    def main(self):
        driver = self.driver_chrome()

        driver.get('https://www.flashscore.com/')

        # all_games = self.gather_games(driver)

        # all_games = ['g_1_OzaZBCdm', 'g_1_4CPdbgSm', 'g_1_QwxUj2dh', 'g_1_YRFhXtQE', 'g_1_g_1_IqeVeTDH',
        #              'g_1_bVESOjSp','g_1_jPPhVhkH', 'g_1_K8if632r', 'g_1_vglJ2naP', 'g_1_x480LCM3',
        #              'g_1_EHZ0UYta', 'g_1_Msw9SCBB', 'g_1_rcRHQjtO', 'g_1_IkthWfCn', 'g_1_fXULPAeU',
        #              'g_1_h8Y4Thd5', 'g_1_WhpdVERh', 'g_1_nwrvqrcM', 'g_1_YoILfVf4', 'g_1_AaB2mq9r',
        #              'g_1_jNCQgkAA', 'g_1_feJHeBub', 'g_1_4zQ5n3Ol', 'g_1_UHFbDvwd', 'g_1_thJ2Cbh2',
        #              'g_1_Y9AyL2U2', 'g_1_COVIousG', 'g_1_8h0voSiO', 'g_1_Sn2Jmggn', 'g_1_zuOG3gTO',
        #              'g_1_0S0zn8xI', 'g_1_ncGb9cam', 'g_1_xdSgjJyM', 'g_1_GnRckwiS', 'g_1_MT3Qpcaq',
        #              'g_1_2q5ZEPPH', 'g_1_A98sD3fU', 'g_1_A98sD3fU', 'g_1_WI9wEquO', 'g_1_ngMMVCxd',
        #              'g_1_SMI4AiQh', 'g_1_MqI89Bua']

        all_games = []
        with open('today_games.txt', 'r') as file:
            for line in file.readlines():
                all_games.append(line)

        self.scan_each_game(driver, all_games)

    def scan_each_game(self, driver, all_games):

        tokens_list = str(datetime.datetime.now()).split(' ')
        date_for_file = tokens_list[0]
        # print(date_for_file)
        # with open(f'checked_today{date_for_file}.txt', 'w') as file:
        #     file.write('')
        # file.close()
        checked_today = []
        with open(f'checked_today{date_for_file}.txt', 'r') as file:
            [checked_today.append(line.split('\n')[0]) for line in file.readlines()]
        print(checked_today)
        for game in all_games:
            if game in checked_today:
                print('CHECKED')
                continue
            try:
                # print(game.split('g_1_')[1])
                BASE_URL = f"https://www.flashscore.com/match/{game.split('g_1_')[1]}/#match-summary"
                driver.get(BASE_URL)
                with open(f'checked_today{date_for_file}.txt', 'a') as file:
                    file.write(f'{game}')
                file.close()
                sleep(3)
                try:
                    driver.find_element_by_id('onetrust-accept-btn-handler').click()
                except:
                    pass
                # WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, self.GAME_WAIT_XPATH)))

                teams_token = driver.find_elements_by_class_name(self.TEAMS_A_LINKS_CLASS)

                home_team, away_team = teams_token[1].text, teams_token[3].text

                date_time_token = driver.find_element_by_id('utime').text.split(' ')
                date, time = date_time_token[0], date_time_token[1]
                print(date, time)
                time += ':00'
                my_datetime = datetime.datetime.strptime(time, "%H:%M:%S")
                print(datetime.datetime.now())
                tokens_list = str(datetime.datetime.now()).split(' ')
                curr_time = datetime.datetime.strptime(tokens_list[1].split('.')[0], '%H:%M:%S')
                # if my_datetime < curr_time:
                #     print(f'Finished - {home_team} {away_team}')
                #     continue

                county_league_token = driver.find_element_by_xpath(self.COUNTRY_TOURNAMENT_DIV_XPATH).text.split(': ')
                country, league = county_league_token

                try:
                    odds_token = driver.find_element_by_id('tab-prematch-odds').text.split('\n')

                    home_odd, draw_odd, away_odd = odds_token[1], odds_token[3], odds_token[5]

                except Exception:
                    home_odd, draw_odd, away_odd = '-', '-', '-'
                    continue

                home_team_games, away_team_games, h2h_games, homehome_games, awayaway_games = self.get_h2h(driver)

                print(country, league, date, time, home_team, away_team, home_odd, draw_odd, away_odd)

                home_games_stats = self.get_stats(home_team_games, 'home_games')
                print(home_games_stats)
                away_games_stats = self.get_stats(away_team_games, 'away_games')
                print(away_games_stats)
                h2h_games_stats = self.get_stats(h2h_games, 'h2h_games')
                print(h2h_games_stats)
                homehome_games_stats = self.get_stats(homehome_games, 'homehome_games')
                print(homehome_games_stats)
                awayaway_games_stats = self.get_stats(awayaway_games, 'awayaway_games')
                print(awayaway_games_stats)
                total_games_checked = home_games_stats['total_games'] + away_games_stats['total_games'] + \
                                      h2h_games_stats['total_games'] + homehome_games_stats['total_games'] + \
                                      awayaway_games_stats['total_games']
                average_percent_draws = (home_games_stats['draws_percent'] + away_games_stats['draws_percent'] +
                                         h2h_games_stats['draws_percent'] + homehome_games_stats['draws_percent'] +
                                         awayaway_games_stats['draws_percent']) / 5
                try:
                    valuebet_percent = average_percent_draws - (1/float(draw_odd) * 100)
                except:
                    valuebet_percent = 0
                valuebet_abs = False
                if valuebet_percent > 0 and total_games_checked > 50:
                    valuebet_abs = True
                print(f'Average percent draws: {average_percent_draws:.2f}, current odds: {draw_odd}, Valuebet %: {valuebet_percent:.2f}')
                if valuebet_abs:
                    with open(f'valuebets{date}.txt', 'a') as file:
                        file.write(f'{game} {country} {league} {date} {time} {home_team} {away_team} {home_odd} {draw_odd} {away_odd} -> Value: {valuebet_percent:.2f}\n')
                    file.close()

                print(f'{country} {league} {date} {time} {home_team} {away_team} {home_odd} {draw_odd} {away_odd} -> Value: {valuebet_percent:.2f} %')
            except:
                pass

    def get_stats(self, games, trigger):
        stats = {'total_games': 0, 'draws': 0}
        for game in games:
            stats['total_games'] += 1
            if game[3] == 'Draw':
                stats['draws'] += 1
        try:
            stats['draws_percent'] = (stats['draws'] / stats['total_games']) * 100
        except:
            stats['draws_percent'] = 0
        return stats

    def get_h2h(self, driver):
        try:
            driver.find_element_by_id(self.H2H_ID).click()
            sleep(1)
            self.click_show_more_buttons(driver)
        except Exception:
            print('No h2h button')

        # try:
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
        # print(len(home_team_games), len(away_team_games), len(h2h_games))

        home_team_games, away_team_games, h2h_games = self.clean_h2h_data(driver, home_team_games, away_team_games,
                                                                          h2h_games)

        home_home_games, away_away_games = self.get_home_home_away_away(driver)

        # except Exception:
        #     print('Click more button error')

        try:
            driver.find_element_by_id('h2h-home').click()
            self.click_show_more_buttons(driver)
        except Exception:
            print('No h2h home button.')

        return home_team_games, away_team_games, h2h_games, home_home_games, away_away_games

    def get_home_home_away_away(self, driver):
        driver.find_element_by_id('h2h-home').click()
        sleep(1)
        self.click_show_more_buttons(driver)

        home_home_games = []
        away_away_games = []

        try:
            home_team_games = driver.find_elements_by_xpath(self.HOME_HOME_XPATH)
            if len(home_team_games) >= 5:
                home_team_games = home_team_games[:-1]

            if len(home_team_games) == 0:
                home_team_games = driver.find_elements_by_xpath(self.HOME_HOME_XPATH_2)
                if len(home_team_games) >= 5:
                    home_team_games = home_team_games[:-1]

            for home_game in home_team_games:
                # print(type(home_game))
                # print(home_game.get_attribute('outerHTML'))
                all_tds = home_game.find_elements_by_tag_name('td')
                # print(len(all_tds))

                date = all_tds[0].get_attribute('innerText')
                result = home_game.find_element_by_tag_name('a').get_attribute('title')
                score = all_tds[4].get_attribute('innerText')
                teams_token = home_game.find_elements_by_class_name('name')
                home_team = teams_token[0].get_attribute('innerText')
                away_team = teams_token[1].get_attribute('innerText')
                home_home_games.append([date, home_team, away_team, result, score])

                # print('||||||||||||||||')
                # print(len(date), len(home_team), len(away_team), len(result), len(score))
                # print(date, home_team, away_team, result, score)

        except Exception:
            print('home_home_games_problem')

        driver.find_element_by_id('h2h-away').click()
        sleep(1)
        self.click_show_more_buttons(driver)

        try:
            away_team_games = driver.find_elements_by_xpath(self.AWAY_AWAY_XPATH)
            if len(away_team_games) >= 5:
                away_team_games = away_team_games[:-1]

            if len(away_team_games) == 0:
                away_team_games = driver.find_elements_by_xpath(self.AWAY_AWAY_XPATH_2)
                if len(away_team_games) >= 5:
                    away_team_games = away_team_games[:-1]

            for away_game in away_team_games:
                # print(away_game.get_attribute('outerHTML'))
                all_tds = away_game.find_elements_by_tag_name('td')
                date = all_tds[0].get_attribute('innerText')
                result = away_game.find_element_by_tag_name('a').get_attribute('title')
                score = all_tds[4].get_attribute('innerText')
                teams_token = away_game.find_elements_by_class_name('name')
                home_team, away_team = teams_token[0].get_attribute('innerText'), teams_token[1].get_attribute('innerText')
                away_away_games.append([date, home_team, away_team, result, score])

                # print("-------------")
                # print(date, home_team, away_team, result, score)

            return home_home_games, away_away_games
        except Exception:
            print('problem_away_away_games')

    def clean_h2h_data(self, driver, home_team_games, away_team_games, h2h_games):
        all_home_finished_games = []
        all_away_finished_games = []
        h2h_finished_games = []
        try:
            for old_home_game in home_team_games:
                date = old_home_game.find_element_by_class_name('date').text
                result = old_home_game.find_element_by_tag_name('a').get_attribute('title')
                score = old_home_game.find_element_by_class_name('score').text
                teams_token = old_home_game.find_elements_by_class_name('name')
                home_team, away_team = teams_token[0].text, teams_token[1].text
                all_home_finished_games.append([date, home_team, away_team, result, score])

                # print(date, home_team, away_team, result, score)

            for old_away_game in away_team_games:
                date = old_away_game.find_element_by_class_name('date').text
                result = old_away_game.find_element_by_tag_name('a').get_attribute('title')
                score = old_away_game.find_element_by_class_name('score').text
                teams_token = old_away_game.find_elements_by_class_name('name')
                home_team, away_team = teams_token[0].text, teams_token[1].text
                all_away_finished_games.append([date, home_team, away_team, result, score])

                # print(date, home_team, away_team, result, score)
        except:
            pass
        try:
            for old_h2h_game in h2h_games:
                # LOSS ON RESULT IS NOT ACCURATE, I COUNT ONLY THE DRAWS !!! IT NOT ACCURATE ONLY ON THIS H2H GAMES
                date = old_h2h_game.find_element_by_class_name('date').text
                score = old_h2h_game.find_element_by_class_name('score').text
                teams_token = old_h2h_game.find_elements_by_class_name('name')
                home_team, away_team = teams_token[0].text, teams_token[1].text
                result = 'Loss'
                home_goals, away_goals = score.split(' : ')[0], score.split(' : ')[1]
                if home_goals == away_goals:
                    result = 'Draw'
                h2h_finished_games.append([date, home_team, away_team, result, score])

            # print(date, home_team, away_team, result, score)
        except Exception:
            print('h2h_h2h error')
        return all_home_finished_games, all_away_finished_games, h2h_finished_games

    def gather_games(self, driver):
        # sleep(3)
        try:
            WebDriverWait(driver, timeout=20).until(EC.visibility_of_element_located((By.XPATH, self.COOKIE_BUTTON_XPATH)))
            driver.find_element_by_xpath(self.COOKIE_BUTTON_XPATH).click()
        except:
            pass
        sleep(3)
        all_divs_token = driver.find_elements_by_xpath(self.GAME_DIV_XPATH)
        print(len(all_divs_token))
        # asd
        all_games = []

        for div in all_divs_token:
            div_strings = div.get_attribute('outerHTML')

            if 'Click for match detail!' in div_strings:
                # print(div.get_attribute('id'))
                all_games.append(div.get_attribute('id'))

        with open('today_games.txt', 'w') as txt_file:
            [txt_file.write(game + '\n') for game in all_games]
        txt_file.close()
        return all_games

    @staticmethod
    def click_show_more_buttons(driver):
        try:
            buttons = driver.find_elements_by_class_name('show_more')
            for button in buttons:
                if 'Show more matches' in button.text:
                    while True:
                        try:
                            button.click()
                        except Exception:
                            break
            buttons.click()
            sleep(1)
        except Exception:
            pass

    @staticmethod
    def driver_chrome():
        CHROME_PATH = '/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/home/velinov/Desktop/scrp-drivers/chromedriver'

        chrome_options = ChromeOptions()
        chrome_options.binary_location = CHROME_PATH
        chrome_options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE

        capa = DC.CHROME
        capa["pageLoadStrategy"] = "normal"

        driver = Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH, desired_capabilities=capa)
        driver.maximize_window()
        return driver


if __name__ == '__main__':
    scanner = GameCollector()
    scanner.main()

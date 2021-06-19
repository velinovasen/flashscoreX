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
    ODDS_XPATH = str("//div[{'contains(concat(" ",normalize-space(@class),' '),' oddsWrapper ')}']")
    COUNTRY_TOURNAMENT_DIV_XPATH = '/html/body/div[1]/div[3]/div/span[3]'
    COUNTRY_TOURNAMENT_DIV_XPATH_2 = '/html/body/div[2]/div[3]/div/span[3]'
    H2H_XPATH = '/html/body/div[1]/div[5]/div/a[3]'
    H2H_XPATH_2 = '/html/body/div[1]/div[6]/div/a[3]'
    HOME_GAMES_XPATH = '/html/body/div[1]/div[8]/div[1]/div[2]/div'
    HOME_GAMES_XPATH_2 = '/html/body/div[2]/div[8]/div[1]/div[2]/div'
    AWAY_GAMES_XPATH = '/html/body/div[1]/div[8]/div[2]/div[2]/div'
    H2H_GAMES_XPATH = '/html/body/div[1]/div[8]/div[3]/div[2]/div'
    HOME_GAMES_XPATH_3 = '/html/body/div[2]/div[1]/div[4]/div[11]/div[2]/div[4]/div[1]/table/tbody/tr'
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

        all_games = ['g_1_8MZOBNVL', 'g_1_GMP2SN8h', 'g_1_KCFSWvfH', 'g_1_dzACfQFJ', 'g_1_vsbvWLUs', 'g_1_pld9xCMD']
        #
        # all_games = []
        # with open('today_games.txt', 'r') as file:
        #     for line in file.readlines():
        #         all_games.append(line)

        self.scan_each_game(driver, all_games)

    def scan_each_game(self, driver, all_games):

        tokens_list = str(datetime.datetime.now()).split(' ')
        date_for_file = tokens_list[0]
        # print(date_for_file)
        # with open(f'checked_today{date_for_file}.txt', 'w') as file:
        #     file.write('')
        # file.close()
        checked_today = []
        with open(f'checked_today2021-06-18.txt', 'r') as file:
            [checked_today.append(line.split('\n')[0]) for line in file.readlines()]
        print(checked_today)
        for game in all_games:
            print(f'84 -> {game}')
            if game in checked_today:
                print('CHECKED')
                continue
            # try:
            # print(game.split('g_1_')[1])
            BASE_URL = f"https://www.flashscore.com/match/{game.split('g_1_')[1]}/#match-summary"
            driver.get(BASE_URL)
            with open(f'checked_today{date_for_file}.txt', 'a') as file:
                file.write(f"{game} + '\n'")
            file.close()
            sleep(3)
            try:
                driver.find_element_by_id('onetrust-accept-btn-handler').click()
            except:
                pass
            # WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, self.GAME_WAIT_XPATH)))
            try:
                home_team = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[4]').text
                away_team = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[4]/div[4]').text
            except:
                home_team = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div[4]/div[2]').text
                away_team = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[4]/div[4]/div[1]').text

            print('---------------------------------------------')
            print(f'110 -> {home_team} vs {away_team}')

            try:
                print('PROBVA ZA DATATA')
                date_time_token = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]').text.split(' ')
            except:
                print('EXCEPTVA DATATA')
                date_time_token = driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[1]').text.split(' ')
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

            try:
                county_league_token = driver.find_element_by_xpath(self.COUNTRY_TOURNAMENT_DIV_XPATH).text.split(': ')
            except:
                county_league_token = driver.find_element_by_xpath(self.COUNTRY_TOURNAMENT_DIV_XPATH_2).text.split(': ')
            country, league = county_league_token


            print(f'137 -> {country}: {league}')

            try:
                odds_token = driver.find_element_by_xpath(self.ODDS_XPATH).text.split('\n')

                print(f'142 -> {odds_token}')

                home_odd, draw_odd, away_odd = odds_token[1], odds_token[3], odds_token[5]

            except Exception:
                try:
                    odds_token = driver.find_element_by_xpath('/html/body/div[1]/div[9]/div/div/div').text.split(
                        '\n')

                    print(f'151 -> {odds_token}')

                    home_odd, draw_odd, away_odd = odds_token[1], odds_token[3], odds_token[5]
                except:
                    try:
                        odds_token = driver.find_element_by_xpath('/html/body/div[2]/div[15]/div/div/div').text.split('\n')
                        print(f'151 -> {odds_token}')

                        home_odd, draw_odd, away_odd = odds_token[1], odds_token[3], odds_token[5]
                    except:
                        print(f'155 -> No odds -> skipping')
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
            average_percent_draws = ((home_games_stats['draws'] + away_games_stats['draws'] +
                                     h2h_games_stats['draws'] + homehome_games_stats['draws'] +
                                     awayaway_games_stats['draws']) / total_games_checked) * 100
            try:
                valuebet_percent = average_percent_draws - (1/float(draw_odd) * 100)
            except:
                valuebet_percent = 0
            valuebet_abs = False
            if valuebet_percent > 0 and total_games_checked > 50:
                valuebet_abs = True
            print(f'Average percent draws: {average_percent_draws:.2f}, current odds: {draw_odd}, Valuebet %: {valuebet_percent:.2f}')
            if valuebet_abs:
                with open(f'valuebets06.18.2021.txt', 'a') as file:
                    file.write(f'{game} {country} {league} {date} {time} {home_team} {away_team} {home_odd} {draw_odd} {away_odd} -> Value: {valuebet_percent:.2f}\n')
                file.close()

            print(f'{country} {league} {date} {time} {home_team} {away_team} {home_odd} {draw_odd} {away_odd} -> Value: {valuebet_percent:.2f} %')
            # except:
            #     print('184 -> CHUPI SE MAMKA MU')
            #     pass

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
        print('215 -> VLEZNAHME V get_h2h')
        try:
            driver.find_element_by_link_text('H2H').click()
            sleep(3)
            print('220 -> KLIKA NA H2H')
            self.click_show_more_buttons(driver)
        except Exception:
            try:
                driver.find_element_by_xpath(self.H2H_XPATH_2).click()
                sleep(1)
                self.click_show_more_buttons(driver)
            except:
                print('No h2h button')

        WebDriverWait(driver, timeout=10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[15]')))

        home_team_games = self.get_home_away_h2h_games(driver, 'home')

        away_team_games = self.get_home_away_h2h_games(driver, 'away')

        h2h_games = self.get_home_away_h2h_games(driver, 'h2h')

        print(len(home_team_games), len(away_team_games), len(h2h_games))

        home_team_games, away_team_games, h2h_games = self.clean_h2h_data(driver, home_team_games, away_team_games,
                                                                          h2h_games)

        home_home_games, away_away_games = self.get_home_home_away_away(driver)

        try:
            driver.find_element_by_link_text(' - Home').click()
            self.click_show_more_buttons(driver)
        except Exception:
            print(f'272 -> No h2h home button.')

        return home_team_games, away_team_games, h2h_games, home_home_games, away_away_games

    def get_home_away_h2h_games(self, driver, option):
        '''
        :param driver:
        :param option: a string, home team games, away team games or h2h games
        :return: a list with web elements containing the games
        '''
        main_h2h_div = driver.find_element_by_id('detail')
        raw_tokens = main_h2h_div.find_elements_by_tag_name('div')
        div_raw_big = ''
        for raw_div in raw_tokens:
            if 'h2h' in raw_div.get_attribute('class'):
                div_raw_big = raw_div
                break

        all_divs_section_tokens = []
        for tok in div_raw_big.find_elements_by_tag_name('div'):
            if 'section' in tok.get_attribute('class'):
                all_divs_section_tokens.append(tok)

        if option == 'home':
            div_class_section_home = all_divs_section_tokens[0]
            div_class_rows_home = div_class_section_home.find_elements_by_tag_name('div')[1]
            home_team_games = div_class_rows_home.find_elements_by_tag_name('div')
            home_team_games = home_team_games[0::2]
            return home_team_games

        if option == 'away':
            div_class_section_away = all_divs_section_tokens[1]
            div_class_rows_away = div_class_section_away.find_elements_by_tag_name('div')[1]
            away_team_games = div_class_rows_away.find_elements_by_tag_name('div')
            away_team_games = away_team_games[0::2]
            return away_team_games

        if option == 'h2h':
            div_class_section_h2h = all_divs_section_tokens[2]
            div_class_rows_h2h = div_class_section_h2h.find_elements_by_tag_name('div')[1]
            h2h_games = div_class_rows_h2h.find_elements_by_tag_name('div')
            h2h_games = h2h_games[0::2]
            return h2h_games

        if option == 'homehome':
            div_class_section_homehome = all_divs_section_tokens[0]
            div_class_rows_homehome = div_class_section_homehome.find_elements_by_tag_name('div')[1]
            homehome_games = div_class_rows_homehome.find_elements_by_tag_name('div')
            homehome_games = homehome_games[0::2]
            return homehome_games

        if option == 'homeh2h':
            div_class_section_homeh2h = all_divs_section_tokens[1]
            div_class_rows_homeh2h = div_class_section_homeh2h.find_elements_by_tag_name('div')[1]
            homeh2h_games = div_class_rows_homeh2h.find_elements_by_tag_name('div')
            homeh2h_games = homeh2h_games[0::2]
            return homeh2h_games

    def get_home_home_away_away(self, driver):
        main_div = driver.find_element_by_class_name('subTabs')
        # print(main_div.text)
        home_home_div = main_div.find_elements_by_tag_name('a')[1]
        ActionChains(driver).move_to_element(home_home_div).click().perform()
        sleep(1)
        self.click_show_more_buttons(driver)

        home_home_games = []
        away_away_games = []

        # try:
            # home_team_games = driver.find_elements_by_xpath(self.HOME_HOME_XPATH)
        main_h2h_div = driver.find_element_by_id('detail')
        # print('------------------')
        # print(f"291 -> {main_h2h_div.get_attribute('outerHTML')}")
        # print('------------------')
        raw_tokens = main_h2h_div.find_elements_by_tag_name('div')
        div_raw_big = ''
        for raw_div in raw_tokens:
            if 'h2h' in raw_div.get_attribute('class'):
                div_raw_big = raw_div
                break

        print(f"300 -> {div_raw_big.get_attribute('outerHTML')}")

        self.click_show_more_buttons(driver)

        homehome_games = self.get_home_away_h2h_games(driver, 'homehome')
        ## TO FINISH !!!

        clean_homehome_games = self.clean_homehome_games(homehome_games)

        # except Exception:
        #     print('home_home_games_problem')

        away_away_div = main_div.find_elements_by_tag_name('a')[2]
        away_away_div.click()
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

    def clean_homehome_games(self, homehome_games):
        all_ready_games = []
        for homegame in homehome_games:
            date_token, competition_token, home_team_token, away_team_token, score_token, result_token = '', '', '', '', '', ''
            all_spans = homegame.find_elements_by_tag_name('span')
            for span in all_spans:
                if 'date' in span.get_attribute('class'):
                    date_token = span
                elif 'event' in span.get_attribute('class'):
                    competition_token = span
                elif 'home' in span.get_attribute('class'):
                    home_team_token = span
                elif 'away' in span.get_attribute('class'):
                    away_team_token = span
                elif 'result' in span.get_attribute('class'):
                    score_token = span
                elif 'icon' in span.get_attribute('class'):
                    result_token = span
            try:
                date = date_token.get_attribute('innerText')
            except:
                date = ''
                # print(homegame.get_attribute('outerHTML'))
            competition_token = competition_token.get_attribute('innerText')
            home_team = home_team_token.get_attribute('innerText')
            away_team = away_team_token.get_attribute('innerText')
            score = score_token.get_attribute('innerText')
            result = result_token.get_attribute('innerText')
            print(date, competition_token, home_team, away_team, score, result)
            all_ready_games.append([date, competition_token, home_team, away_team, score, result])
        return all_ready_games

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
            sleep(3)
            WebDriverWait(driver, timeout=15).until(EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div[2]/div[3]')))
            # driver.find_element_by_xpath(
            #     '/html/body/div[6]/div[1]/div/div[1]/div[2]/div[5]/div[2]/div[1]/div[2]/div[3]').click()
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
        while True:
            try:
                # print('444 -> VLIZA V BUTONA')
                main_h2h_div = driver.find_element_by_id('detail')
                raw_tokens = main_h2h_div.find_elements_by_tag_name('div')
                div_raw_big = ''
                for raw_div in raw_tokens:
                    if 'h2h' in raw_div.get_attribute('class'):
                        div_raw_big = raw_div
                        break
                all_divs = div_raw_big.find_elements_by_tag_name('div')
                button = ''
                for div in all_divs:
                    if 'showMore' in div.get_attribute('class'):
                        button = div
                        break
                button.click()
                # print('454 -> KLIKNA')
            except:
                break

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

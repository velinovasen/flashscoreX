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
        '''
        Main controller. We can choose how to pass the input games, as we also can choose to gather them.
        :return:
        '''
        driver = self.driver_chrome()

        driver.get('https://www.flashscore.com/')

        # all_games = self.gather_games(driver)

        all_games = ['g_1_t8sIvBLj', 'g_1_27DKJH59', 'g_1_f3ea75lf']
        #
        # all_games = []
        # with open('today_games.txt', 'r') as file:
        #     for line in file.readlines():
        #         all_games.append(line)

        self.scan_each_game(driver, all_games)

    def scan_each_game(self, driver, all_games):
        '''
        The main controller function for each game. Here we handle the behaviour for each separate game.
        :param driver: Selenium webdriver
        :param all_games:
        :return:
        '''

        tokens_list = str(datetime.datetime.now()).split(' ')
        date_for_file = tokens_list[0]

        checked_today = []
        with open(f'checked_today2021-06-18.txt', 'r') as file:
            [checked_today.append(line.split('\n')[0]) for line in file.readlines()]
        print(checked_today)

        # Entering the main loop for all games we have as an input.
        for game in all_games:
            print(f'84 -> {game}')
            if game in checked_today:
                print('CHECKED')
                continue

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

            odds_token = self.extract_odds(driver)
            if odds_token == 'No odds.':
                print('139 -> No odds, skipping this game.')
                continue
            else:
                home_odd, draw_odd, away_odd = odds_token

            # Getting the results for both teams.
            home_team_games, away_team_games, h2h_games, homehome_games, home_h2h_games, awayaway_games = self.get_results(driver)

            print(country, league, date, time, home_team, away_team, home_odd, draw_odd, away_odd)

            # Making the calculations from past results.
            home_games_stats = self.get_stats(home_team_games, 'home_games')
            print(f'Home team games -> {home_games_stats}')
            away_games_stats = self.get_stats(away_team_games, 'away_games')
            print(f'Away team games -> {away_games_stats}')
            h2h_games_stats = self.get_stats(h2h_games, 'h2h_games')
            print(f'H2H games -> {h2h_games_stats}')
            homehome_games_stats = self.get_stats(homehome_games, 'homehome_games')
            print(f'Home_Home games ->{homehome_games_stats}')
            home_h2h_games_stats = self.get_stats(home_h2h_games, 'home_h2h_games')
            print(f'Home H2H games -> {home_h2h_games_stats}')
            awayaway_games_stats = self.get_stats(awayaway_games, 'awayaway_games')
            print(f'Away_Away games -> {awayaway_games_stats}')
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

    def get_results(self, driver):
        '''
        Getting the games data and preparing it for calculations.
        :param driver: Selenium webdriver
        :return: Six lists with webelements(football games)
        '''
        print('215 -> VLEZNAHME V get_h2h')
        try:
            driver.find_element_by_link_text('H2H').click()
            sleep(3)
            print('220 -> KLIKA NA H2H')
        except Exception:
            try:
                driver.find_element_by_xpath(self.H2H_XPATH_2).click()
                sleep(1)
            except:
                print('No h2h button')

        self.click_show_more_buttons(driver)

        home_team_games = self.get_home_away_h2h_games(driver, 'home')

        away_team_games = self.get_home_away_h2h_games(driver, 'away')

        h2h_games = self.get_home_away_h2h_games(driver, 'h2h')

        home_home_games = self.get_home_away_h2h_games(driver, 'homehome')

        home_h2h_games = self.get_home_away_h2h_games(driver, 'homeh2h')

        away_away_games = self.get_home_away_h2h_games(driver, 'awayaway')

        print(len(home_team_games), len(away_team_games), len(h2h_games), len(home_home_games), len(home_h2h_games) len(away_away_games))

        return home_team_games, away_team_games, h2h_games, home_home_games, home_h2h_games, away_away_games

    def get_home_away_h2h_games(self, driver, option):
        '''
        :param driver:
        :param option: a string, home team games, away team games or h2h games
        :return: a list with web elements containing the games
        '''
        if option == 'homehome':
            self.click_homehome_awayaway_button(driver, 'home')
        elif option == 'awayaway':
            self.click_homehome_awayaway_button(driver, 'away')

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

        if option == 'home' or option == 'homehome' or option == 'awayaway':
            div_class_section = all_divs_section_tokens[0]
            div_class_rows = div_class_section.find_elements_by_tag_name('div')[1]
            team_games = div_class_rows.find_elements_by_tag_name('div')
            team_games = team_games[0::2]
            team_games = self.clean_games(team_games)
            return team_games

        if option == 'away' or option == 'homeh2h':
            div_class_section = all_divs_section_tokens[1]
            div_class_rows = div_class_section.find_elements_by_tag_name('div')[1]
            team_games = div_class_rows.find_elements_by_tag_name('div')
            team_games = team_games[0::2]
            team_games = self.clean_games(team_games)
            return team_games

        if option == 'h2h':
            div_class_section_h2h = all_divs_section_tokens[2]
            div_class_rows_h2h = div_class_section_h2h.find_elements_by_tag_name('div')[1]
            h2h_games = div_class_rows_h2h.find_elements_by_tag_name('div')
            h2h_games = h2h_games[0::2]
            h2h_games = self.clean_games(h2h_games)
            return h2h_games

    def clean_games(self, all_games):
        '''
        Clean the data, make sure we have everything(result)
        :param all_games: list with all games(raw WebElement)
        :return: List with all games(webelements)
        '''
        all_ready_games = []
        for home_game in all_games:
            # print(home_game.get_attribute('outerHTML'))
            date_token, competition_token, home_team_token, away_team_token, score_token, result_token = '', '', '', '', '', ''
            all_spans = home_game.find_elements_by_tag_name('span')
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

            date = date_token.get_attribute('innerText')
            competition_token = competition_token.get_attribute('innerText')
            home_team = home_team_token.get_attribute('innerText')
            away_team = away_team_token.get_attribute('innerText')
            score = score_token.get_attribute('innerText')
            if result_token == '':
                result = 'L'
                home_goals, away_goals = score.split(' : ')[0], score.split(' : ')[1]
                if home_goals == away_goals:
                    result = 'D'
            else:
                result = result_token.get_attribute('innerText')
            # print(f'304 -> {date, competition_token, home_team, away_team, score, result}')
            all_ready_games.append([date, competition_token, home_team, away_team, score, result])
        return all_ready_games

    def extract_odds(self, driver):
        '''
        Extract the odds for each game, but if we don't have odds, we continue with next game.
        :param driver:
        :return: A list with the odds ['3.00', '3.00', '3.00'] or A string 'No odds'
        '''
        main_div = driver.find_element_by_id('detail')
        main_div_tokens = main_div.find_elements_by_tag_name('div')
        div_odds_wrapper = ''
        for div in main_div_tokens:
            if 'oddsWrapper' in div.get_attribute('class'):
                div_odds_wrapper = div
                break
        if div_odds_wrapper == '':
            return 'No odds.'

        all_div_tokens = div_odds_wrapper.find_elements_by_tag_name('div')
        all_odds_tokens = []
        for div in all_div_tokens:
            if 'cellWrapper' in div.get_attribute('class'):
                all_odds_tokens.append(div)

        home_odd = all_odds_tokens[0].get_attribute('innerText').split('\n')[1]
        draw_odd = all_odds_tokens[1].get_attribute('innerText').split('\n')[1]
        away_odd = all_odds_tokens[2].get_attribute('innerText').split('\n')[1]
        return home_odd, draw_odd, away_odd

    def get_stats(self, games, trigger):
        '''
        Count how many draws they have.
        :param games: ALl games that need to be calculated
        :param trigger: In case we want to add extra options for the calculations
        :return: A dictionary with total games, total draws and percent of draws
        '''
        stats = {'total_games': 0, 'draws': 0}
        for game in games:
            # print(game)
            stats['total_games'] += 1
            if game[5] == 'D':
                stats['draws'] += 1
        try:
            stats['draws_percent'] = (stats['draws'] / stats['total_games']) * 100
        except:
            stats['draws_percent'] = 0
            # print(stats)
        return stats

    def click_homehome_awayaway_button(self, driver, option):
        '''
        Click Home team games at home or Away team games away button.
        :param driver:
        :param option:
        :return:
        '''
        main_div = driver.find_element_by_class_name('subTabs')
        if option == 'home':
            div_to_click = main_div.find_elements_by_tag_name('a')[1]
        else:
            div_to_click = main_div.find_elements_by_tag_name('a')[2]
        ActionChains(driver).move_to_element(div_to_click).click().perform()
        sleep(1)
        self.click_show_more_buttons(driver)

    def gather_games(self, driver):
        '''
        Get all games for the specific day(funcitonality will be added to choose from the calendar)
        :param driver: Selenium webdriver
        :return: A file with all games for today(id's)
        '''
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
        '''
        Click show more button to reveal all past games.
        :param driver: Selenium webdriver
        '''
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
        '''
        Open the selenium chrome webdriver.
        :return: Selenium webdriver
        '''
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

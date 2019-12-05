import sys
import re
import pycountry
import random
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


class CsvWriter:
    filename = None

    def __init__(self, filename='results.csv'):
        self.filename = filename
        try:
            if sys.argv[2] == 'save':
                with open(self.filename, mode='w') as file:
                    file_writer = csv.writer(
                        file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(['ISO Code', 'Value'])
        except IndexError:
            pass

    def write_row(self, row):
        try:
            if sys.argv[2] == 'save':
                with open(self.filename, mode='a') as file:
                    file_writer = csv.writer(
                        file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(row)
        except IndexError:
            pass


class Scrapper:
    driver = webdriver.Chrome()

    def displayRandomCountries(self, number):
        selected_countries = []

        for i in range(number):
            selected_countries.append(list(pycountry.countries)[
                random.randint(-1, len(pycountry.countries) - 1)].alpha_3)
        for ISO in selected_countries:
            print(ISO)
            self.searchByIso(ISO)
            print('\n')

    def searchByIso(self, iso):
        self.driver.get("https://wits.worldbank.org/CountryProfile/en/Country/" +
                        iso + "/Year/2017/TradeFlow/Export/Partner/by-country/Product/Total")
        for i in range(4):
            html = self.driver.find_element_by_id(
                "row" + str(i) + "jqx-ProductGrid")
            if 'No data to display' in html.text:
                print('No data to display for this ISO')
                break
            else:
                rawValue = html.find_element_by_css_selector(
                    '.jqx-grid-cell.jqx-item.jqx-grid-cell-sort')
                value = rawValue.text.split(',')[0]
                country = html.find_element_by_tag_name(
                    "a").get_attribute("href")
                isoCode = re.match(
                    r'^https://wits.worldbank.org/CountryProfile/en/Country/' + iso + '/Year/2017/TradeFlow/Export/Partner/(.*)/Product/All-Groups$', country).group(1)
                print('> ' + isoCode + ' ' + value + 'B')
                csv_file.write_row([isoCode, value + 'B'])


page = Scrapper()

try:
    csv_file = CsvWriter(sys.argv[3])
except IndexError:
    csv_file = CsvWriter()

if (sys.argv[1] == 'all'):
    page.displayRandomCountries(5)
else:
    page.searchByIso(sys.argv[1])

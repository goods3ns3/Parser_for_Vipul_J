from requests_html import HTMLSession
from funcy import print_durations
from selenium import webdriver
import lxml.html
import csv
import os


options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
options.add_argument('accept=accept: ')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')
driver = webdriver.Chrome(
    executable_path=os.path.join('chromedriver', 'chromedriver.exe'),
    options=options
)
driver.set_window_size(1980, 2000)


def get_name_and_city_from_file():  # Open file with company names
    try:
        with open('Sample_Web_Scrapping.csv', 'r', newline='') as csv_read:
            reader = csv.DictReader(csv_read)
            company_name = []
            company_city = []
            for row in reader:
                company_name.append(row['CompanyName'])
                company_city.append(row['CompanyCity'])
            return company_name, company_city
    except Exception as e:
        print(e)
        print("Can't read the file. Try rename it like 'Sample_Web_Scrapping.csv'")


def create_name_for_search_links():  # Change names to insert into a link
    name_list = get_name_and_city_from_file()[0]
    name_list_for_search = []
    for name in name_list:
        if '&' in name:
            name = name.replace('&', '%26')
        if '\'' in name:
            name = name.replace('\'', '%27')
        if ';' in name:
            name = name.replace(';', '')
        if ' ' in name:
            name = name.replace(' ', '%20')
        if ',' in name:
            name = name.replace(',', '%2C')
        name_list_for_search.append(name)
    return name_list_for_search


def create_search_links():  # Create search links :)
    print('==========================')
    print('Creating links for search')
    print('==========================')
    name_list_for_search = create_name_for_search_links()
    links_list = []
    for i in range(len(name_list_for_search)):
        link = f'https://www.dnb.com/business-directory/company-search.html?term={name_list_for_search[i]}&page=1'
        links_list.append(link)
    return links_list


# def save_search_links():  # Save search links into a file (not necessary)
#     try:
#         links_list = create_search_links()
#         with open('search_links_list.csv', 'a', encoding='utf-8', newline='') as links_csv:
#             writer = csv.writer(links_csv)
#             for link in links_list:
#                 writer.writerow([link])
#     except Exception as e:
#         print(e)
#         print('File writing error')


# def save_links_list(company_link):  # Save links list into a file (not necessary)
#     try:
#         with open('links_list.csv', 'a', encoding='utf-8', newline='') as links_csv:
#             writer = csv.writer(links_csv)
#             writer.writerow([company_link])
#     except Exception as e:
#         print(e)
#         print('File writing error')


def save_result(row):
    with open('result.csv', 'a', encoding='utf-8', newline='') as links_csv:
        writer = csv.writer(links_csv, delimiter=';')
        writer.writerow(row)


def parse_company_page_requests(company_link): # Use requests-html and lxml (higher speed)
    session = HTMLSession()
    try:
        r = session.get(company_link)
        r.html.render(sleep=1, keep_page=True)
        tree = lxml.html.document_fromstring(r.text)
        try:
            title = (tree.xpath('//*[@id="content"]/div[2]/div/div[3]/div/div/div[1]/div/div/div/h2/text()')[0]).strip()
        except:
            title = ' '
        try:
            website = (tree.xpath('//*[@id="hero-company-link"]/text()')[0]).strip()
        except:
            website = ' '
        try:
            street_address_1 = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[1]/div/text()')[
                0]).strip()
        except:
            street_address_1 = ' '
        try:
            company_city = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[1]/text()')[
                0]).strip()
        except:
            company_city = ' '
        try:
            company_region = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[2]/text()')[
                0]).strip()
        except:
            company_region = ' '
        try:
            company_postal = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[3]/text()')[
                0]).strip()
        except:
            company_postal = ' '
        try:
            company_country = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[4]/text()')[
                0]).strip()
        except:
            company_country = ' '
        try:
            address = (street_address_1 + ',' + company_city + ',' + company_region + ',' + company_postal + ',' + company_country).strip()
        except:
            address = ' '
        try:
            phone = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[3]/div[2]/div/span/text()')[
                0]).strip()
        except:
            raise Exception
            # phone = ' '
        try:
            description = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div/div/span/text()')[
                0]).strip()
        except:
            description = ' '
        try:
            key_principal = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[5]/div[2]/div/div/span[1]/text()')[
                0]).strip()
        except:
            key_principal = ' '
        try:
            industry = (tree.xpath(
                '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[6]/div[2]/div/span[1]/a/text()')[
                0]).strip()
        except:
            industry = ' '

        save_result([title, website, address, phone, description, key_principal, industry])
    except Exception as e:
        print('phone number not found', e)


def company_search():  # Company search
    company_city = get_name_and_city_from_file()[1]
    company_search_links_list = create_search_links()
    len_of_list = len(company_search_links_list)
    for a in range(len_of_list):
        company_city_match = company_city[a].lower()
        try:
            driver.get(company_search_links_list[a])
            driver.implicitly_wait(10)
            print('Company №', a + 1, 'of', len_of_list)
            results_amount = len(driver.find_elements_by_class_name('search_result'))
            if results_amount == 1:
                city = driver.find_element_by_xpath('//*[@id="company_results"]/ul/li/div[4]/div/span[1]').text
                city = city.lower()
                if city == company_city_match:
                    company_link = driver.find_element_by_xpath(
                        '//*[@id="company_results"]/ul/li/div[1]/div[1]/a').get_attribute('href')
                    parse_company_page_requests(company_link)
            elif results_amount > 1:
                for i in range(1, results_amount):
                    if i == 11 or i == 22:
                        continue
                    else:
                        city = driver.find_element_by_xpath(
                            f'//*[@id="company_results"]/ul/li[{i}]/div[4]/div/span[1]').text
                        city = city.lower()
                        if city == company_city_match:
                            company_link = driver.find_element_by_xpath(
                                f'//*[@id="company_results"]/ul/li[{i}]/div[1]/div[1]/a').get_attribute('href')
                            parse_company_page_requests(company_link)
            else:
                raise Exception
        except Exception as e:
            print('company not found', e)
    driver.close()
    driver.quit()


# def read_links_list_from_file():  # Open file with company links (not necessary)
#     try:
#         with open('links_list.csv', 'r', newline='') as csv_read:
#             reader = csv.reader(csv_read)
#             company_links = []
#             for row in reader:
#                 company_links.append(row)
#             return company_links
#     except Exception as e:
#         print(e)
#         print("Can't read the file 'links_list.csv'")


# def parse_company_page_selenium(): # Use Selenium webdriver (lower speed) (not necessary)
#     links_list = read_links_list_from_file()
#     len_links_list = len(links_list)
#     for i in range(len_links_list):
#         print('Page №', i+1, 'of', len_links_list)
#         try:
#             driver.get(links_list[i][0])
#             driver.implicitly_wait(3)
#             try:
#                 title = driver.find_element_by_class_name('profile_header_title').text
#             except:
#                 title = ' '
#             try:
#                 website = driver.find_element_by_id('hero-company-link').get_attribute('href')
#             except:
#                 website = ' '
#             try:
#                 street_address_1 = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[1]/div').text
#             except:
#                 street_address_1 = ' '
#             try:
#                 company_city = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[1]').text
#             except:
#                 company_city = ' '
#             try:
#                 company_region = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[2]').text
#             except:
#                 company_region = ' '
#             try:
#                 company_postal = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[3]').text
#             except:
#                 company_postal = ' '
#             try:
#                 company_country = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div/span/div[2]/span[4]').text
#             except:
#                 company_country = ' '
#             try:
#                 address = street_address_1 + ',' + company_city + ',' + company_region + ',' + company_postal + ',' + company_country
#             except:
#                 address = ' '
#             try:
#                 phone = driver.find_element_by_class_name('profile-phone-element').text
#             except:
#                 phone = ' '
#             try:
#                 description = driver.find_element_by_xpath(
#                     '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[4]/div[2]/div/div/span').text
#             except:
#                 description = ' '
#             try:
#                 key_principal = driver.find_element_by_xpath(
#                     '//*[@id="content"]/div[2]/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div[5]/div[2]/div/div/span[1]').text
#             except:
#                 key_principal = ' '
#             try:
#                 industry = driver.find_element_by_class_name('profile-industry-item').text
#             except:
#                 industry = ' '
#
#             save_result([title, website, address, phone, description, key_principal, industry])
#         except Exception as e:
#             print(e)
#     driver.close()
#     driver.quit()


@print_durations()
def main():
    try:
        company_search()  # Run it to get a file with links to company pages
    except Exception as e:
        print('=====================')
        print(e)
        print('=====================')
        print('Something went wrong. Save the message above and contact your programmer.')
        print('=====================')
    finally:
        print('=====================')
        print('The program has completed its work.')
        print('You can check the file "result.csv"')
        print('=====================')


if __name__ == '__main__':
    main()

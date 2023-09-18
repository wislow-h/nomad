from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
domain = "https://kr.indeed.com"


def extract_indeed_jobs(search_keyword):
  browser = webdriver.Chrome(options=options)
  pages = get_page_count(search_keyword)
  job_list = []

  for page in range(pages):
    browser.get(f"{domain}/jobs?q={search_keyword}&start={page * 10}")

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    jobs = soup.find_all("div", class_="cardOutline", reculsive=False)

    for job in jobs:
      anchor = job.select_one("h2 a")
      job_title = anchor['aria-label']
      job_link = anchor['href']
      company_name = job.find("span",
                              class_="companyName").text.replace(",", " ")
      company_location = job.find("div",
                                  class_="companyLocation").text.replace(
                                    ",", " ")

      job_data_dic = {
        'company': company_name,
        'link': f"{domain}{job_link}",
        'region': company_location,
        'title': job_title.replace(",", " "),
      }

      job_list.append(job_data_dic)

  return job_list


def get_page_count(search_keyword):
  browser = webdriver.Chrome(options=options)
  browser.get(f"{domain}/jobs?q={search_keyword}")

  soup = BeautifulSoup(browser.page_source, 'html.parser')
  # nav[role='navigation'] always exists even if the page is a single page.
  pagination_button_area = soup.select_one("nav[role='navigation']")
  if pagination_button_area == None:
    return 1

  count = len(pagination_button_area.find_all("div"))

  if count >= 5:
    return 5
  else:
    return count - 1 if count > 1 else 1

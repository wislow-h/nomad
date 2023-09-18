from bs4 import BeautifulSoup

domain = "https://remoteok.com"


def extract_remoteok_jobs(browser, search_keyword):

  browser.get(f"{domain}/remote-{search_keyword}-jobs")

  soup = BeautifulSoup(browser.page_source, 'html.parser')
  job_post_list = soup.find_all('tr', class_='job')
  job_list = []

  if len(job_post_list) < 1:
    return job_list
  else:
    for job in job_post_list:
      anchor = job.find('a', attrs={'itemprop': 'url'})
      job_link = anchor['href']
      job_title = job.find('h2', attrs={'itemprop': 'title'})
      company = job.find('h3', attrs={'itemprop': 'name'})
      location_list = job.find_all('div', class_='location')
      company_location = ''
      pay_range = ''

      if location_list[-1].text.find('$') > -1:
        pay_range = location_list[-1].text
        location_list.pop(-1)

      for location in location_list:
        company_location = company_location + ' / ' + location.string if company_location != '' else location.string

      job_data_dic = {
        'title': job_title.text.strip().replace(",", " "),
        'company': company.text.strip().replace(",", " "),
        'link': f"{domain}{job_link}",
        'region': company_location.replace(",", " "),
        'payment': pay_range,
      }

      job_list.append(job_data_dic)

  return job_list

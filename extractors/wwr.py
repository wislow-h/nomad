from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(search_term):
  base_url = "https://weworkremotely.com/remote-jobs/search?utf8=✓&term="
  response = get(f"{base_url}{search_term}")
  real_job_list = []

  if response.status_code != 200:
    print("We have problem.")
  else:
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all("section", class_="jobs")
    if len(jobs) > 0:
      for job in jobs:
        job_li_list = job.find_all("li")

        for item in job_li_list:
          if len(item['class']) == 0 or (len(item['class']) > 0
                                         and item['class'][0] != 'view-all'):
            anchors = item.find_all("a")
            anchor = anchors[1]
            link = anchor['href']
            company, kind, region = anchor.find_all('span', class_='company')
            title = anchor.find('span', class_='title')

            job_data_dic = {
              'company': company.string.replace(",", " "),
              'link': f"https://weworkremotely.com/{link}",
              'region': region.string.replace(",", " "),
              'title': title.string.replace(",", " "),
            }

            real_job_list.append(job_data_dic)

    return real_job_list

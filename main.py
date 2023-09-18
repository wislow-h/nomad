from flask import Flask, render_template, request, redirect, send_file
from extractors.remoteok import extract_remoteok_jobs
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from file import save_file

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options)

app = Flask("Jean-Job-Scrapper")
db = {}


@app.route("/")
def home():
  return render_template('home.html')


@app.route("/search")
def search():
  search_keyword = request.args.get("keyword")

  if search_keyword == None or search_keyword == "":
    return redirect("/")

  if search_keyword in db:
    jobs = db[search_keyword]
  else:
    wwr_jobs = extract_wwr_jobs(search_keyword)
    remoteok_jobs = extract_remoteok_jobs(browser, search_keyword)
    jobs = wwr_jobs + remoteok_jobs
    db[search_keyword] = jobs

  return render_template('search.html', keyword=search_keyword, jobs=jobs)


@app.route("/export")
def export():
  search_keyword = request.args.get("keyword")

  if search_keyword == None or search_keyword == "":
    return redirect("/")

  if search_keyword not in db:
    return redirect(f"/search?keyword={search_keyword}")

  save_file(search_keyword, db[search_keyword])
  return send_file(f"{search_keyword}.csv", as_attachment=True)


@app.route("/bot")
def bot():
  return "this is a page for bots to check the server."


app.run("0.0.0.0")

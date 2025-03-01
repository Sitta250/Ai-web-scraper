from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_cd9e2c11-zone-ai_scraper:9nsszfq7rtjw'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
import time

def scrape_website(website):
  print("Launching chrome browser...")


  sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
  with Remote(sbr_connection, options=ChromeOptions()) as driver:
      print('Connected! Navigating...')
      driver.get(website)
      solve_res = driver.execute('executeCdpCommand', {
          'cmd': 'Captcha.waitForSolve',
          'params':{'detectTimeout': 10000},
      })
      print('Captcha solve status:', solve_res['value']['status'])
      print('Taking page screenshot to file page.png')
      driver.get_screenshot_as_file('./page.png')
      print('Navigated! Scraping page content...')
      html = driver.page_source
      return html

def exrtact_body_content(html_content):
   soup = BeautifulSoup(html_content, 'html.parser')
   body_content = soup.body
   if body_content:
      return str(body_content)
   return ''

def clean_body_content(body_content):
   soup = BeautifulSoup(body_content, 'html.parser')

   for script_or_style in soup(['script', 'style']):
      script_or_style.extract()

      cleaned_content = soup.get_text(separator='\n')
      cleaned_content = '\n'.join(line.strip() for line in cleaned_content.splitlines() if line.strip())

      return cleaned_content

def split_dom_content(dom_content, max_length=6000):
   return [
      #grabbing the first 6000 char to ensure this will not exceed the limit of llm. after each loop is completed the index is increased by the amount of the max_lenght, in this case, 6000. this is repeated until the len of dom_content is reached
      dom_content[i: i +max_length] for i in range(0, len(dom_content), max_length)
   ]


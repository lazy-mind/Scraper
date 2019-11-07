import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv

# helper function to visualize the progress
def showProgress(counter,msg):
	if parameters.number_of_profiles < 10:
		return counter+1
	if (counter % int(parameters.number_of_profiles/10) == 0):
		print("{}: {}%".format(msg,int(100*counter/parameters.number_of_profiles)))
	return counter+1

# general method to extract information from specific xpath location
def scrapeInfoFromXPath(sel, path):
	info = sel.xpath(path).extract_first()
	return info.strip() if info and info!="" else "*** NA ***"

# check login status
def checkLoginStatus(response):
	# reslove login issue
	if response == parameters.restricted_page:
		print("Please resolve your login problem with LinkedIn, and rerun the program")
		exit(0)
	elif response != parameters.success_page:
		user_response = int(input("Please finish the verification process to go on\nWhen finished, enter 1\nPress others to exit\n: "))
		if user_response != 1:
			exit(0)

# go to the login page, enter the credential, and click the login button
def login():
	global driver
	driver.get('https://www.linkedin.com/login')

	username = driver.find_element_by_id('username')
	username.send_keys(parameters.linkedin_username)

	password = driver.find_element_by_id('password')
	password.send_keys(parameters.linkedin_password)

	log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
	log_in_button.click()

	return driver.current_url

# open google and search, store all search result in a list, return the list with valid url
def searchOnGoogle():
	global driver
	linkedin_urls = []

	# open google and do a search
	driver.get('https:www.google.com')
	search_query = driver.find_element_by_name('q')
	search_query.send_keys(parameters.search_query)
	search_query.send_keys(Keys.RETURN)

	# capture the search result in a list
	while parameters.number_of_profiles > len(linkedin_urls):
		# find all valid elements
		linkedin_urls_elements = driver.find_elements_by_class_name('iUh30')

		# navigate to the parent nodes and extract the link
		for webElement in linkedin_urls_elements:
			parentElement = webElement.find_element_by_xpath("../..")
			linkedin_urls.append(parentElement.get_attribute("href"))
			showProgress(len(linkedin_urls), "Scraping Profile Links")

		# navigate to the next page
		next_page = driver.find_element_by_xpath('//*[@id="pnnext"]').get_attribute("href")
		if next_page and next_page!="":
			driver.get(next_page)
		else:
			break

	print("Number of profile links collected: {}\n".format(len(linkedin_urls)))
	return linkedin_urls

# go to linkedIn profile page, grab and record information
def scrapeFromLinkedIn(url): 
	driver.get(url)
	sel = Selector(text=driver.page_source) 

	name = scrapeInfoFromXPath(sel,'//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()')
	job_title = scrapeInfoFromXPath(sel,'//*[starts-with(@class, "mt1 t-18 t-black t-normal")]/text()')
	company = scrapeInfoFromXPath(sel,'//*[@data-control-name="position_see_more"]/span/text()')
	college = scrapeInfoFromXPath(sel,'//*[@data-control-name="education_see_more"]/span/text()')
	location = scrapeInfoFromXPath(sel,'//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()')

	global writer
	writer.writerow([name,job_title,company,college,location,url])

	if parameters.slow_mode==1:
		sleep(1)





# check whether username and password are provided
if parameters.linkedin_username == "" or parameters.linkedin_password == "":
	print("Please provide username and password in parameters.py file. Then rerun the program")
	exit(0)

# start the browser and login
driver = webdriver.Chrome(parameters.drive_path)
checkLoginStatus(login())

# start the csv writer
writer = csv.writer(open(parameters.file_name, 'w+'))
writer.writerow(['Name','Job Title','Company','College', 'Location','URL'])
counter = 1

# search google and scrape linkedin information
for url in searchOnGoogle()[0:parameters.number_of_profiles]:
	scrapeFromLinkedIn(url)
	counter = showProgress(counter,"Scraping Profile Information")
driver.quit()
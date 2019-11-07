#
#
# Specify the following parameter
#
#

# desirable profile
search_query = 'site:linkedin.com/in/ AND "Python developer" AND "London"'

# user credential: user name
linkedin_username = ''

# user credential: password
linkedin_password = ''

# how many profiles to scrape in one time
number_of_profiles = 100

# change to others if don't care about linkedin restriction
slow_mode = 0

# where the selenium driver located
drive_path = './chromedriver'

# the file name for output dataframe
file_name = 'results_file.csv'



#
#
# Don't change unless it is necessary
#
#

# check whether there is a restriction when logging in
restricted_page = "https://www.linkedin.com/checkpoint/lg/login-submit"

# check whether the user has successfully logged in
success_page = "https://www.linkedin.com/feed/"


import os
import pandas as pd
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def scrape():
    '''
    main scrape logics
    '''

    # open the driver, start the browser and login
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(parameters.drive_path, chrome_options=chrome_options)

    # login to the account
    pass

    # go though user pagges
    for identifier in parameters.user_identifier:
        print(identifier)

        # visit the user identifier
        driver.get(parameters.website_url + identifier)

        # find required post
        # class_name = "v1Nh3 kIKUG  _bz0w"
        post_list = driver.find_elements_by_xpath("//div[contains(@class,'v1Nh3')]//a")[:parameters.num_of_post]

        # get the post content
        for post in post_list:
            post_result = [identifier, parameters.website_url + identifier]
            post_result.extend(scrape_post(post))

            post_result = pd.DataFrame([post_result], columns=["user", "profile link", "post link", "post image", "post comment", "post date", "post like"])
            if not os.path.exists("instagram.csv"):
                post_result.to_csv("instagram.csv", index=False)
            else:
                with open('instagram.csv', 'a') as f:
                    post_result.to_csv(f, header=False, index=False)
            # sleep(1000)
    driver.quit()

def scrape_post(post):
    '''
    scrape the content of a single post
    '''

    # go to the webpage
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(parameters.drive_path, chrome_options=chrome_options)

    post_link = post.get_attribute("href")
    driver.get(post_link)

    # find the post main frame
    post_content = driver.find_elements_by_xpath("//div[contains(@class,'ltEKP')]")[0]

    post_image = ""
    try:
        post_image = post_content.find_elements_by_xpath("//img[contains(@class,'FFVAD')]")[0].get_attribute("src")
        # print(post_image)
    except Exception as e:
        pass

    post_main_comment = ""
    try:
        span_list = post_content.find_elements_by_xpath("//li[contains(@class,'PpGvg')]//span")
        if len(span_list)==1:
            post_main_comment = span_list[0].text
        else:
            post_main_comment = span_list[1].text
    except Exception as e:
        print(e)
        pass

    post_time = ""
    try:
        post_time = post_content.find_elements_by_xpath("//div[contains(@class,'NnvRN')]//time")[0].get_attribute("datetime")
        # print(post_time)
    except Exception as e:
        pass

    post_like = ""
    try:
        post_like = post_content.find_elements_by_xpath("//div[contains(@class,'Nm9Fw')]//span")[0].text
        # print(post_like)
    except Exception as e:
        pass

    driver.quit()
    return [post_link, post_image, post_main_comment, post_time, post_like]

scrape()

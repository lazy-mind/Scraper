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
        sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        sleep(3)

        # find required post
        # class_name = "v1Nh3 kIKUG  _bz0w"
        # sleep(10)
        post_list = []
        trail = 10
        while len(post_list)==0:
            sleep(1)
            post_list = driver.find_elements_by_xpath(".//article[contains(@class,'r-6416eg')]")[:parameters.num_of_post]
            trail -= 1
            if trail==0:
                break
        sleep(3)
        print(len(post_list))

        # get the post content
        for post in post_list:
            post_result = [identifier, parameters.website_url + identifier]
            post_result.extend(scrape_post(post))

            post_result = pd.DataFrame([post_result], columns=["user", "profile link", "post link", "post video", "post image", "post tweet", "post date", "post like"])
            if not os.path.exists("tweet.csv"):
                post_result.to_csv("tweet.csv", index=False)
            else:
                with open('tweet.csv', 'a') as f:
                    post_result.to_csv(f, header=False, index=False)
            # sleep(1000)
        # sleep(1000)

    driver.quit()

def scrape_post(post):
    '''
    scrape the content of a single post
    '''
    post_link = ""
    try:
        post_link = post.find_elements_by_xpath(".//a[contains(@class,'css-4rbku5 css-18t94o4 css-901oao r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')]")[0].get_attribute("href")
        # print(post_link)
    except Exception as e:
        pass

    post_video = ""
    try:
        upper_div = post.find_elements_by_xpath(".//div[contains(@class, 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o')]")[0]
        post_video = upper_div.find_elements_by_xpath(".//video")[0].get_attribute("src")
        # print(post_video)
    except Exception as e:
        pass

    post_img = ""
    try:
        upper_div = post.find_elements_by_xpath(".//div[contains(@class, 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-5f2r5o r-1mi0q7o')]")[0]
        post_img = upper_div.find_elements_by_xpath(".//img")[0].get_attribute("src")
        # print(post_img)
    except Exception as e:
        pass

    post_tweet = ""
    try:
        post_tweet = post.find_elements_by_xpath(".//div[contains(@class,'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')]")[0].text
        # print(post_tweet)
    except Exception as e:
        pass

    post_time = ""
    try:
        post_time = post.find_elements_by_xpath(".//a[contains(@class,'css-4rbku5 css-18t94o4 css-901oao r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0')]//time")[0].get_attribute("datetime")
        # print(post_time)
    except Exception as e:
        pass

    post_like = ""
    try:
        upper_div = post.find_elements_by_xpath(".//div[contains(@class, 'css-901oao r-1awozwy r-1re7ezh r-6koalj r-1qd0xha r-a023e6 r-16dba41 r-1h0z5md r-ad9z0x r-bcqeeo r-o7ynqc r-clp7b1 r-3s2u2q r-qvutc0')]")[2]
        post_like = upper_div.find_elements_by_xpath(".//span//span")[0].text
        # print(post_like)
    except Exception as e:
        pass

    return [post_link, post_video, post_img, post_tweet, post_time, post_like]

scrape()

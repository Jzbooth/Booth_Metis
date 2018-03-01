# -*- coding: utf-8 -*-
# Zillow scraper functions, these are sourced at the top of zillow_runfile.py

import re as re
import time
import zipcode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def zipcodes_list(st_items):
    # If st_items is a single zipcode string.
    if isinstance(st_items, str):
        zc_objects = zipcode.islike(st_items)
        output = [str(i).split(" ", 1)[1].split(">")[0] for i in zc_objects]
    # If st_items is a list of zipcode strings.
    elif isinstance(st_items, list):
        zc_objects = [n for i in st_items for n in zipcode.islike(str(i))]
        output = [str(i).split(" ", 1)[1].split(">")[0] for i in zc_objects]
    else:
        raise ValueError("arg 'st_items' must be of type str or list")
    return(output)

def init_driver(file_path):
    # Starting maximized fixes https://github.com/ChrisMuir/Zillow/issues/1
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=file_path, 
                              chrome_options=options)
    driver.wait = WebDriverWait(driver, 10)
    return(driver)

# Helper function for checking for the presence of a web element.
def _is_element_displayed(driver, elem_text, elem_type):
    if elem_type == "class":
        try:
            out = driver.find_element_by_class_name(elem_text).is_displayed()
        except (NoSuchElementException, TimeoutException):
            out = False
    elif elem_type == "css":
        try:
            out = driver.find_element_by_css_selector(elem_text).is_displayed()
        except (NoSuchElementException, TimeoutException):
            out = False
    else:
        raise ValueError("arg 'elem_type' must be either 'class' or 'css'")
    return(out)

# If captcha page is displayed, this function will run indefinitely until the 
# captcha page is no longer displayed (checks for it every 30 seconds).
# Purpose of the function is to "pause" execution of the scraper until the 
# user has manually completed the captcha requirements.
def _pause_for_captcha(driver):
    while True:
        time.sleep(30)
        if not _is_element_displayed(driver, "captcha-container", "class"):
            break

# Check to see if the page is currently stuck on a captcha page. If so, pause 
# the scraper until user has manually completed the captcha requirements.
def check_for_captcha(driver):
    if _is_element_displayed(driver, "captcha-container", "class"):
        print("\nCAPTCHA!\n"\
              "Manually complete the captcha requirements.\n"\
              "Once that's done, if the program was in the middle of scraping "\
              "(and is still running), it should resume scraping after ~30 seconds.")
        _pause_for_captcha(driver)

def navigate_to_website(driver, site):
    driver.get(site)
    # Check to make sure a captcha page is not displayed.
    check_for_captcha(driver)

def click_buy_button(driver):
    try:
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "nav-header")))
        button.click()
        time.sleep(10)
    except (TimeoutException, NoSuchElementException):
        raise ValueError("Clicking the 'Buy' button failed")
    # Check to make sure a captcha page is not displayed.
    check_for_captcha(driver)

def enter_search_term(driver, search_term):
    if not isinstance(search_term, str):
        search_term = str(search_term)
    try:
        search_bar = driver.wait.until(EC.presence_of_element_located(
            (By.ID, "citystatezip")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "zsg-icon-searchglass")))
        search_bar.clear()
        time.sleep(3)
        search_bar.send_keys(search_term)
        time.sleep(3)
        button.click()
        time.sleep(3)
        return(True)
    except (TimeoutException, NoSuchElementException):
        return(False)
    # Check to make sure a captcha page is not displayed.
    check_for_captcha(driver)

def test_for_no_results(driver):
    # Check to see if the "zoom out" msg exists (an indication that no results
    # were returned from the search).
    no_results = _is_element_displayed(driver, ".zoom-out-message", "css")
    # If the zoom-out msg is not displayed, check for "invalid zip" msg.
    if not no_results:
        no_results = _is_element_displayed(driver, "zsg-icon-x-thick", "class")
    # Check to make sure a captcha page is not displayed.
    check_for_captcha(driver)
    return(no_results)

def get_html(driver):
    output = []
    keep_going = True
    while keep_going:
        # Pull page HTML
        try:
            output.append(driver.page_source)
        except TimeoutException:
            pass
        # Check to see if a "next page" link exists.
        keep_going = _is_element_displayed(driver, "zsg-pagination-next", 
                                           "class")
        if keep_going:
            # Test to ensure the "updating results" image isnt displayed. 
            # Will try up to 5 times before giving up, with a 5 second wait 
            # between each try.             
            tries = 5
            cover = _is_element_displayed(driver, 
                                          "list-loading-message-cover", 
                                          "class")
            while cover and tries > 0:
                time.sleep(5)
                tries -= 1
                cover = _is_element_displayed(driver, 
                                              "list-loading-message-cover", 
                                              "class")
            # If the "updating results" image is confirmed to be gone 
            # (cover == False), click next page. Otherwise, give up on trying 
            # to click thru to the next page of house results, and return the 
            # results that have been scraped up to the current page.
            if not cover:
                try:
                    driver.wait.until(EC.element_to_be_clickable(
                        (By.CLASS_NAME, "zsg-pagination-next"))).click()
                    time.sleep(3)
                    # Check to make sure a captcha page is not displayed.
                    check_for_captcha(driver)
                except TimeoutException:
                    keep_going = False
            else:
                keep_going = False
    return(output)

# Split the raw page source into segments, one for each home listing.
def get_listings(list_obj):
    output = []
    for i in list_obj:
        htmlSplit = i.split('" id="zpid_')[1:]
        output += htmlSplit
    return(output)

# Helper function for testing if an object is "empty" or not.
def _is_empty(obj):
    if any([len(obj) == 0, obj == "null"]):
        return(True)
    else:
        return(False)

# For most listings, card_info will contain info on number of bedrooms, 
# number of bathrooms, square footage, and sometimes price.
def get_card_info(soup_obj):
    try:
        card = soup_obj.find(
            "span", {"class" : "zsg-photo-card-info"}).get_text().split(u" \xb7 ")
    except (ValueError, AttributeError):
        card = "NA"
    if _is_empty(card):
        card = "NA"
    return(card)

def get_street_address(soup_obj):
    try:
        street = soup_obj.find(
            "span", {"itemprop" : "streetAddress"}).get_text().strip()
    except (ValueError, AttributeError):
        street = "NA"
    if _is_empty(street):
        street = "NA"
    return(street)

def get_description(soup_obj):
    try:
        description = soup_obj.find(
            "div", {"class" : "notranslate zsg-content-item"}).get_text().strip()
    except (ValueError, AttributeError):
        description = "NA"
    if _is_empty(description):
        description = "NA"
    return(description)
    

def get_city(soup_obj):
    try:
        city = soup_obj.find(
            "span", {"itemprop" : "addressLocality"}).get_text().strip()
    except (ValueError, AttributeError):
        city = "NA"
    if _is_empty(city):
        city = "NA"
    return(city)

def get_state(soup_obj):
    try:
        state = soup_obj.find(
            "span", {"itemprop" : "addressRegion"}).get_text().strip()
    except (ValueError, AttributeError):
        state = "NA"
    if _is_empty(state):
        state = "NA"
    return(state)

def get_zipcode(soup_obj):
    try:
        zipcode = soup_obj.find(
            "span", {"itemprop" : "postalCode"}).get_text().strip()
    except (ValueError, AttributeError):
        zipcode = "NA"
    if _is_empty(zipcode):
        zipcode = "NA"
    return(zipcode)

def get_price(soup_obj, list_obj):
    # Look for price within the BeautifulSoup object.
    try:
        price = soup_obj.find(
            "span", {"class" : "zsg-photo-card-price"}).get_text().strip()
    except (ValueError, AttributeError):
        # If that fails, look for price within list_obj (object "card_info").
        try:
            price = [n for n in list_obj 
                         if any(["$" in n, "K" in n, "k" in n])]
            if len(price) > 0:
                price = price[0].split(" ")
                price = [n for n in price if re.search("\d", n)]
                if len(price[0]) > 0:
                    price = price[0]
                else:
                    price = "NA"
            else:
                price = "NA"
        except (ValueError, AttributeError):
            price = "NA"
    if _is_empty(price):
        price = "NA"
    if price != "NA":
        # Transformations to the price string.
        price = price.replace(",", "").replace("+", "").replace("$", "").lower()
        if "k" in price:
            price = price.split("k")[0].strip()
            price = price + "000"
        if "m" in price:
            price = price.split("m")[0].strip()
            if "." not in price:
                price = price + "000000"
            else:
                pricelen = len(price.split(".")[0]) + 6
                price = price.replace(".", "")
                price = price + ((pricelen - len(price)) * "0")
        if _is_empty(price):
            price = "NA"
    return(price)

def get_sqft(list_obj):
    sqft = [n for n in list_obj if "sqft" in n]
    if len(sqft) > 0:
        try:
            sqft = float(
                sqft[0].split("sqft")[0].strip().replace(",", "").replace("+", "")
            )
        except (ValueError, IndexError):
            sqft = "NA"
        if sqft == 0:
            sqft = "NA"
    else:
        sqft = "NA"
    return(sqft)

def get_bedrooms(list_obj):
    beds = [n for n in list_obj if any(["bd" in n, "tudio" in n])]
    if len(beds) > 0:
        beds = beds[0].lower()
        if beds == "studio":
            return(0.0)
        try:
            beds = float(beds.split("bd")[0].strip())
        except (ValueError, IndexError):
            beds = "NA"
    else:
        beds = "NA"
    return(beds)

def get_bathrooms(list_obj):
    baths = [n for n in list_obj if "ba" in n]
    if len(baths) > 0:
        try:
            baths = float(baths[0].split("ba")[0].strip())
        except (ValueError, IndexError):
            baths = "NA"
        if baths == 0:
            baths = "NA"
    else:
        baths = "NA"
    return(baths)

def get_days_on_market(soup_obj):
    try:
        dom = soup_obj.find_all(
            "ul", {"class" : "zsg-list_inline zsg-photo-card-badge"})
        if dom is not None:
            dom = [n.get_text().strip().lower() for n in dom]
            dom = [n for n in dom if "zillow" in n]
            if len(dom) > 0:
                dom = int(dom[0].split(" ")[0])
            else:
                dom = "NA"
        else:
            dom = "NA"
    except (ValueError, AttributeError):
        dom = "NA"
    return(dom)

def get_sale_type(soup_obj):
    try:
        sale_type = soup_obj.find(
            "span", {"class" : "zsg-photo-card-status"}).get_text().strip()
    except (ValueError, AttributeError):
        sale_type = "NA"
    if _is_empty(sale_type):
        sale_type = "NA"
    return(sale_type)

def get_url(soup_obj):
    # Try to find url in the BeautifulSoup object.
    href = [n["href"] for n in soup_obj.find_all("a", href = True)]
    url = [i for i in href if "homedetails" in i]
    if len(url) > 0:
        url = "http://www.zillow.com/homes/for_sale/" + url[0]
    else:
        # If that fails, contruct the url from the zpid of the listing.
        url = [i for i in href if "zpid" in i and "avorite" not in i]
        if len(url) > 0:
            zpid = re.findall(r"\d{8,10}", url[0])
            if zpid is not None and len(zpid) > 0:
                url = "http://www.zillow.com/homes/for_sale/" \
                        + str(zpid[0]) \
                        + "_zpid/any_days/globalrelevanceex_sort/29.759534," \
                        + "-95.335321,29.675003,-95.502863_rect/12_zm/"
            else:
                url = "NA"
        else:
            url = "NA"
    return(url)

def close_connection(driver):
    driver.quit()

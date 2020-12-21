import json
import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains


def get_texts(browser, item, output, name):
    if not os.path.exists(f'{output}{name}'):
        os.makedirs(f'{output}{name}')
    action_chains = ActionChains(browser)
    action_chains.move_to_element(item).click().perform();
    browser.implicitly_wait(5)
    images = browser.find_elements_by_class_name("img-thumbnail")
    action_chains = ActionChains(browser)
    action_chains.move_to_element(images[0]).click().perform();
    browser.implicitly_wait(5)
    old_url = ""
    i = 1
    while browser.current_url != old_url:
        page_resultat = browser.find_element_by_id("resultats_detail")
        output_file = {"url": browser.current_url, "content": page_resultat.text}
        with open(f'{output}{name}/{i}.json', 'w') as outfile:
            json.dump(output_file, outfile)
        # print(browser.current_url, page_resultat.text)
        next_image = browser.find_element_by_class_name('icon-chevron-right')
        old_url = browser.current_url
        action_chains = ActionChains(browser)
        action_chains.move_to_element(next_image).click().perform();
        browser.implicitly_wait(15)
        time.sleep(3)
        i += 1


def get_mimo_families(mimo_url, output):
    if not os.path.exists(output):
        os.makedirs(output)
    browser = webdriver.Chrome('./chromedriver')  # Optional argument, if not specified will search path.
    browser.get(mimo_url)
    browser.implicitly_wait(2)  # wait 5 seconds
    list_families = browser.find_element_by_id("InstrumentTypeLevel2_exact")
    # print(list_families)
    items_families = list_families.find_elements_by_tag_name('li')
    items_families_names = [item.get_attribute('title') for item in items_families]
    for item in range(len(items_families)):
        browser.get(mimo_url)
        browser.implicitly_wait(2)  # wait 5 seconds
        list_families = browser.find_element_by_id("InstrumentTypeLevel2_exact")
        # print(list_families)
        items_families = list_families.find_elements_by_tag_name('li')
        get_texts(browser, items_families[item], output, items_families_names[item])
    browser.stop_client()
    browser.close()
    browser.quit()
    return

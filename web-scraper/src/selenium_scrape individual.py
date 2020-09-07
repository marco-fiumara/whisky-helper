from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

chrome_options = Options()

chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("useAutomationExtension", False)
chrome_options.add_argument("--proxy-server=direct://")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

browser = webdriver.Chrome(
    'venv/bin/chromedriver', options=chrome_options)

start_url = "https://www.masterofmalt.com/"

browser.get(start_url)

search_form = browser.find_element_by_class_name('header-search')

search_whiskey: str = input("Please enter a whiskey: ")

search_form.send_keys(search_whiskey)

search_form.send_keys(Keys.RETURN)


results = browser.find_element_by_id('searchResults')


result_title: str = ""
result_img: str = ""
result_index: int = 0

results_list = results.find_elements_by_xpath('//*[@id="searchResults"]/div')

for index, result in enumerate(results_list):
    print(result.find_elements_by_tag_name('h3')[0].text)
    check = input("Is this correct? (Y/N): ")
    if check.upper() == "Y":
        # result_title = result.find_elements_by_tag_name('h3')[0].text
        # temp_img = result.find_element_by_class_name('p-2547')
        # result_img = temp_img.get_attribute('src')
        result_index = index + 1
        break

whisky_link = results.find_elements_by_xpath(f'//*[@id="searchResults"]/div[{result_index}]/h3/a')[0]

whisky_link.click()

# whisky_desc_container = browser.find_element_by_id('productDesc')

# whisky_desc = whisky_desc_container.find_element_by_tag('p').text

whisky_desc = browser.find_elements_by_xpath('//*[@id="productDesc"]/div/p')[0].text
whisky_img = browser.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_ctl00_imgProductBig"]')[0].get_attribute('src')
whisky_country = browser.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl00_wdCountry"]/span[2]')[0].text
whisky_brand = browser.find_elements_by_xpath('//*[@id="ContentPlaceHolder1_ctl00_ctl00_wdDistillery"]/span[2]')[0].text


print(f'Whisky Description: {whisky_desc}')
print(f'Whisky Image: {whisky_img}')
print(f'Whisky Country : {whisky_country}')
print(f'Whisky Brand: {whisky_brand}')

print("GOT IT!")


# browser.quit()

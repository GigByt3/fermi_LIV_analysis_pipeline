from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
from time import sleep
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

path = r'D:\\Downloads\\chromedriver_win32\\chromedriver.exe'
user_data = r'C:\\Users\\Saeed\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
options = webdriver.ChromeOptions()
options.add_argument(f'--user-data-dir={user_data}')
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(executable_path=path, options=options)
actions = ActionChains(driver)
xpath = '//*[@id="search"]/div/input'  # `search` box at header
url = 'https://stackoverflow.com//'
driver.get(url)
driver.maximize_window()
sleep(10)
position = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath))).location
print(position)
file = open('position.txt', 'a')
file.write(f'{position}, {datetime.now()}\n')
# pyautogui.click(793, 9)
driver.close()



actions = ActionChains(driver)

element = driver.find_element(By.XPATH, 'the_xpath_locator')
actions.move_to_element(element).perform()




response = requests.get('https://www.geeksforgeeks.org/python/python-programming-language-tutorial/')
soup = BeautifulSoup(response.content, 'html.parser')

pyautogui.moveTo(519, 1060, duration = 1)
# simulates a click at the present mouse position 
pyautogui.click()
pyautogui.moveTo(1717, 352, duration = 1) 
pyautogui.click()


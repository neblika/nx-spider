import os
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
FIREFOX_DRIVER_PATH = './bin/geckodriver'



class Browser:
  def __init__(self):
    super(Browser, self).__init__()
    self.instance = None
    self._start()


  # force one instance
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, '_alreadyExists'):
      cls._alreadyExists = object.__new__(cls)
      
    return cls._alreadyExists


  def _start(self):
    print("Browser -> initializing browser.")
    firefox_options = webdriver.FirefoxOptions()
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    firefox_options.add_argument('--headless')

    firefox_service = Service(
      executable_path=FIREFOX_DRIVER_PATH
    )

    browser = webdriver.Firefox(
      service=firefox_service,
      firefox_binary=binary,
      options=firefox_options
    )

    self.instance = browser


  def refresh(self):
    print("Refreshing Browser")
    self.instance.refresh()


  def take_screenshot(self, filePath=None):
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    filePathDefault = f"screenshots/screen_{time}.png"
    filePath = filePath if filePath else filePathDefault
    self.instance.save_screenshot(filePath)
    return filePath


  def quit(self):
    print("Browser -> closing browser.")
    self.instance.quit()


# os.environ.get('GECKODRIVER_PATH')
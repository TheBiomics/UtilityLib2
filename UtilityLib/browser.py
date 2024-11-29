from .project import ProjectManager

from seleniumwire import webdriver as WebDriver # pip install selenium-wire
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui, expected_conditions # WebDriverWait, Select

class BrowserManager(ProjectManager):
  headless = True
  delay = 6
  implicit_wait = 10
  maximized = True
  options = None
  def __init__(self, *args, **kwargs):
    self.wd_ui = ui
    self.wd_by = By
    self.wd_ec = expected_conditions
    self.wd_keys = Keys
    self.set_selectors()

    super().__init__(**kwargs)
    self._set_default_options()

  def _set_default_options(self):
    ...

  def set_selectors(self, *args, **kwargs):
    self.by_id = By.ID
    self.by_name = By.NAME
    self.by_xpath = By.XPATH
    self.by_link_text = By.LINK_TEXT
    self.by_link_text_part = By.PARTIAL_LINK_TEXT
    self.by_tag = By.TAG_NAME
    self.by_class = By.CLASS_NAME
    self.by_css = By.CSS_SELECTOR

  def get_status_code(self):
      _last_pg_req = [_r for _r in self.wd_instance.requests if _r.url == self.wd_instance.current_url]
      _last_pg_req = _last_pg_req[0] if len(_last_pg_req) > 0 else None
      self.wd_instance.last_page_request = _last_pg_req
      return _last_pg_req.response.status_code

  def screenshot(self, *args, **kwargs):
    _screenshot_path = args[0] if len(args) > 0 else kwargs.get("screenshot_path", 'screenshot.png')
    self.wd_instance.save_screenshot(_screenshot_path)

    _original_w_h = self.wd_instance.get_window_size()
    _req_width = self.wd_instance.execute_script('return document.body.parentNode.scrollWidth')
    _req_height = self.wd_instance.execute_script('return document.body.parentNode.scrollHeight')
    self.wd_instance.set_window_size(max([_req_width, 1440]), _req_height)
    # self.wd_instance.save_screenshot(_screenshot_path)  # has scrollbar
    self.wd_instance.find_element(self.wd_by.TAG_NAME, 'body').screenshot(_screenshot_path)
    self.wd_instance.set_window_size(_original_w_h['width'], _original_w_h['height'])

  def wait(self, *args, **kwargs):
    _type = args[0] if len(args) > 0 else kwargs.get("type", 'implicit')
    if _type == 'implicit':
      self.wd_instance.implicitly_wait(self.implicit_wait)
    else:
      self.time_pause(self.delay)
    # elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.NAME, 'chart')))

  def get_url(self, *args, **kwargs):
    _url = args[0] if len(args) > 0 else kwargs.get("url")
    _file_path = args[1] if len(args) > 1 else kwargs.get("file_path")
    _screenshot_path = args[2] if len(args) > 2 else kwargs.get("screenshot_path")
    self.wd_instance.get(_url)
    self.wait("implicit")

    _html = self.wd_instance.page_source
    # _html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    if _screenshot_path:
      self.screenshot(_screenshot_path)

    if _file_path:
      self.write(_file_path, _html)

    self.wait("delay")
    return _html

  def init_browser(self, *args, **kwargs):
    ...

  def close_browser(self, *args, **kwargs):
    if hasattr(self, 'wd_instance') and getattr(self, 'wd_instance'):
      try:
        self.wd_instance.close()
        self.wd_instance.quit()
      except Exception as _e:
        print(f"Failed to close/quit browser:: {_e}")

  close = close_browser

  def __exit__(self):
    # On exit close browser and db engine
    self.close_browser()

class ChromeManager(BrowserManager):
  headless = True
  options = ChromeOptions()
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

  def _set_default_options(self):
    self.options.add_argument("--window-size=1920,1200")

    if self.headless:
      self.options.add_argument("--headless")

  def init_browser(self, *args, **kwargs):
    from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
    self.wd_instance = WebDriver.Chrome(options=self.options,
                                        service=ChromeService(executable_path=ChromeDriverManager().install()))

    if self.maximized:
      self.wd_instance.maximize_window()

class FireFoxManager(BrowserManager):
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)

class BrowserlessManager(ProjectManager):
  browser = None
  def __init__(self, *args, **kwargs):
    super().__init__(**kwargs)
    self.require("mechanicalsoup", 'MechSoup')

  def get_url(self, *args, **kwargs):
    _url = kwargs.get("url", args[0] if len(args) > 0 else None)
    _file_path = kwargs.get("file_path", args[1] if len(args) > 1 else None)

    self.browser = self.MechSoup.StatefulBrowser(raise_on_404=False)
    self.browser.open(_url)

    _html = self.browser.page

    if not None is _file_path:
      self.write(_file_path, str(_html))

    return _html

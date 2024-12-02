# Example Code

```python

browser = ChromeManager()
browser.init_browser()
browser.add_option("--disable-extensions")
browser.toggle_headless(False)

try:
    browser.init_browser()
    browser.set_page_load_timeout(20)
    browser.set_implicit_wait(15)

    html = browser.get_url(url="https://example.com", screenshot_path="example.png", render_js=True)
    print(html)
    browser.fullpage_screenshot("full_example.png")

    # Fetch performance logs
    logs = browser.get_performance_logs()
    print("Performance logs:", logs)

    # Execute JavaScript
    title = browser.execute_js("return document.title;")
    print(f"Page title: {title}")
finally:
    browser.close_browser()

```
import selenium

def test_plugin(browserdriver):
    browserdriver.get('http://stackoverflow.com')
    print(type(browserdriver))
    assert issubclass(type(browserdriver), selenium.webdriver.Remote)

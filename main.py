# contents of runpytest.py
import sys, os, pytest, socket

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

##-- bootstrap configuration (begin) -------------------------------------------------------------
import includes.env_bootstrap as env

#when in local pc mode
__APPROOT = os.getcwd()
__CONFIGFILE = './config/.env.local'    

env.Bootstrap(os.path.join(__APPROOT, __CONFIGFILE))
dockerhost=os.getenv('HOST_NAME')
##-- bootstrap configuration (end) -------------------------------------------------------------

class WebDriverPlugin:

    driver = None
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)

    def connectBrowser(self, browser:str, port:str):
        try:
            hostip=self.getHostIP()
            print(f'Request received to establish connection:\nbrowser[{browser}]@host[{hostip}]:port[{port}]...')
            if browser.lower() == 'chrome':
                self.driver = self.getChromeDriver(hostip, port)

            if browser.lower() == 'firefox':
                self.driver = self.getFirefoxDriver(hostip, port)

            if browser.lower() == 'edge':
                self.driver = self.getEdgeDriver(hostip, port)

            if not self.driver:
                raise Exception(f'The browser[{browser}] is not supported. Suported browsers [chrome, edge, firefox].')

            print(f'Established connection!\nbrowser[{browser}]@host[{hostip}]:port[{port}]')
            return self.driver            
        except Exception as error:
            raise Exception(f'Failed to initialize WebDriver!').with_traceback(error.__traceback__)

    def notifyConnection(self, driver:webdriver):
        js = """alert('Connected to automation! This browser is running in debug mode via automation framework.')"""
        driver.execute_script(js)

    def getHostIP(self) -> str:
        try:
            dockerhostip=socket.gethostbyname(dockerhost)
            return dockerhostip
        except Exception as error:
            raise Exception(f'Host not found!\nUnable to reach host[{dockerhost}]')

    def getChromeDriver(self, hostip:str, port:str=9222) -> str:
        try:
            webdriverpath=os.getenv('CHROME_DRIVER')
            service = ChromeService(executable_path=webdriverpath)
            opt=ChromeOptions()
            opt.add_experimental_option("debuggerAddress", f"{hostip}:{port}")
            driver=webdriver.Chrome(service=service, options=opt)
            return driver
        except Exception as error:        
            raise Exception(f"""
                            Connection failed!\n
                            No client available to connect, browser[Chrome]@host[{hostip}]:port[{port}].\n
                            The automation requires a browser be running in the host machine at this port, 
                            use command to open a browser `./chrome.exe --remote-debugging-port=9222 --user-data-dir="%APPDATA%\ChromeProfile"`"""
                            ).with_traceback(error.__traceback__)

    def getEdgeDriver(self, hostip:str, port:str=9444) -> str:
        #https://lamsi.hashnode.dev/connecting-selenium-to-existing-browser-with-multiple-tabs
        try:
            webdriverpath=os.getenv('EDGE_DRIVER')
            service = EdgeService(executable_path=webdriverpath)
            opt=EdgeOptions()
            opt.add_experimental_option("debuggerAddress", f"{hostip}:{port}")
            driver=webdriver.Edge(service=service, options=opt)
            return driver
        except Exception as error:        
            raise Exception(f"""
                            Connection failed!\n
                            No client available to connect, browser[Edge]@host[{hostip}]:port[{port}].\n
                            The automation requires a browser be running in the host machine at this port, 
                            use command to open a browser `./msedge.exe --remote-debugging-port=9444 --user-data-dir="%APPDATA%\EdgeProfile""`"""
                            ).with_traceback(error.__traceback__)

    def getFirefoxDriver(self, hostip:str, port:str=2828) -> str:
        #https://stackoverflow.com/questions/72331816/how-to-connect-to-an-existing-firefox-instance-using-seleniumpython
        try:
            webdriverpath=os.getenv('GECKO_DRIVER')
            service_args=['--marionette-port', '2828', '--connect-existing']
            service = FirefoxService(executable_path=webdriverpath, port=3000, service_args=service_args)
            driver=webdriver.Firefox(service=service)
            return driver
        except Exception as error:        
            raise Exception(f"""
                            Connection failed!\n
                            No client available to connect, browser[Firefox]@host[{hostip}]:port[{port}].\n
                            The automation requires a browser be running in the host machine at this port, 
                            use command to open a browser `./firefox.exe -marionette -start-debugger-server 2828`"""
                            ).with_traceback(error.__traceback__)
    
    @pytest.fixture
    def browserdriver(self):
        return self.driver        

webdriverPlugin = WebDriverPlugin()
#webdriverPlugin.initWebDriver('firefox', '2828')
#webdriverPlugin.initWebDriver('chrome', '9222')
webdriverPlugin.initWebDriver('edge', '9444')
#webdriverPlugin.notifyConnection(webdriverPlugin.driver)

directory = sys.argv[1]
#pytest.main(['--collect-only', directory], plugins=[webdriverPlugin])
pytest.main([directory], plugins=[webdriverPlugin])

for nodeid in webdriverPlugin.collected:
    print(type(webdriverPlugin.driver))
    print('>>', nodeid)

#invocation
#python3 invoke_pytest.py ./mytests

#https://github.com/pytest-dev/pytest/discussions/2039
#If you don't want any pytest output, you can disable the terminal plugin:
#pytest.main(['--collect-only', '-p', 'no:terminal', directory], plugins=[my_plugin])

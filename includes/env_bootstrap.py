from dotenv import load_dotenv

#use __file__ to always work with relative to file
# TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'test.txt')

class Bootstrap():
    def __init__(self, configfile:str):
        load_dotenv(dotenv_path = configfile)

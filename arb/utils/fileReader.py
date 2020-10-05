from jproperties import Properties


class FileReader:

    def __init__(self, pathFile):
        self.configs = Properties()
        with open(pathFile, 'rb') as config_file:
            self.configs.load(config_file)


    def getProp(self, key):
        return (f'{self.configs.get(key).data}')
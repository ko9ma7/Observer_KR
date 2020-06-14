import re
from configparser import ConfigParser 

price_match = re.compile('.*[^\d]([\d]+,[\d]+)원')

def config_parser(config_file):
    parser = {}
    config = ConfigParser()
    config.read(config_file)
    for section in config.keys():
        if section == "DEFAULT": continue
        parser[section] = {}
        for section_key in config[section].keys():
            value = config.get(section, section_key)
            if value.isdecimal():
                parser[section][section_key] = int(value)
                continue
            parser[section][section_key] = value
    return parser

if __name__ == "__main__":
    print(config_parser('./config/product.cfg'))
    print(config_parser('./config/login.cfg'))


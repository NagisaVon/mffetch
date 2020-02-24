import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
import os.path
from os import path
import sys

config_file_name = ""

def open_config():
    global config_file_name
    if config_file_name == "":
        config_file_name = input("Config file name: ")
        if config_file_name.find('.json') == -1:
            config_file_name += '.json'

    # if True then new file added, stop the program here
    if create_config_if_not_exist(config_file_name):
        return False

    print("Using config file: " + config_file_name)
    with open(config_file_name) as json_file:
        data = json.load(json_file)
        # print(data)
        return data


def get_remote_file_list(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')
    all_link = soup.find_all('a')
    files = []
    for a in all_link:
        address = a['href']
        # hard coded only search for pdf
        if address.find("pdf") != -1:
            new_file = {"name": a.text,
                        "href": address,
                        "file_type": "pdf"}
            files.append(new_file)
    return files


def find_list_diff(file_list, remote_file_list):
    diff_list = []
    for file in remote_file_list:
        if file not in file_list:
            diff_list.append(file)
    return diff_list


def download_file(list, root_href, dir):
    for file in list:
        url = root_href + file['href']
        print(url)
        rf = requests.get(url, allow_redirects=True)
        open(dir + file['href'], 'wb').write(rf.content)


def create_dir_if_not_exist(dir):
    if not path.exists(dir):
        os.mkdir(dir)


def create_config_if_not_exist(config_file_name):
    if not path.exists(config_file_name):
        with open(config_file_name, "w+") as json_file:
            temp = {'title': 'template', 'href': 'https://xxxx/', 'dir': 'temp',
                    'sections': ['sec-01', 'sec-02', 'sec-03'],
                    'sec-01': {'href': 'https://xxxx/sec-01', 'dir': 'sec-01', 'file': []},
                    'sec-02': {'href': 'https://xxxx/sec-02', 'dir': 'sec-02', 'file': []},
                    'sec-03': {'href': 'https://xxxx/sec-03', 'dir': 'sec-02', 'file': []}}
            print(temp)
            data = json.dumps(temp, indent=2)
            json_file.write(data)
        print("File not exist, template config created. ")
        return True
    return False

def write_config_to_file(new_config):
    global config_file_name
    with open(config_file_name, "w+") as json_file:
        data = json.dumps(new_config, indent=2)
        json_file.write(data)


# Hard code config file name

config_file_name = "math121home.json"

config = open_config()
if not config:
    sys.exit("Please modify the new file created. ")

home_dir = config["dir"]
create_dir_if_not_exist(home_dir)

for sec in config["sections"]:
    # get file list from json
    file_list = config[sec]["file"]

    # get url
    url = config[sec]["href"]

    # get file list from the server
    remote_file_list = get_remote_file_list(url)

    # find diff --- disabled, always download all
    # new_file_list = find_list_diff(file_list, remote_file_list)
    new_file_list = remote_file_list

    # download diff file
    dir = home_dir + '/' + config[sec]["dir"] + '/'
    create_dir_if_not_exist(dir)
    root_href = config["href"]
    download_file(new_file_list, root_href, dir)

    # update to config
    config[sec]["file"] = remote_file_list

write_config_to_file(config)











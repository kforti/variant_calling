import requests
from bs4 import BeautifulSoup
from data_config import fast5_links, fastq_links, DATA_CONFIG as config
from pathlib import Path
import h5py
import os
import mappy as mp


def fast5dir_to_fastq(fast5dir, fastq_path):
    for file in os.listdir(fast5dir):
        if file == '.DS_Store':
            return
        fast5file_to_fastq(file, fastq_path)

def fast5file_to_fastq(fast5_file, fastq_path):
    if fast5_file == '.DS_Store':
        return

    h5 = h5py.File(fast5_file)
    fastq = h5["Analyses"]["Basecall_2D_000"]["BaseCalled_2D"]["Fastq"]
    result = fastq[()].decode("ASCII").split('\n')
    save_dir = fastq_path + result[0] + '.fq'
    with open(save_dir, 'a') as f:
        for i in result:
            f.write(i)
            f.write('\n')

def mk_int(string):
    result = [0, ""]
    if "G" in string:
        string = string.replace("G", "")
        result[1] = "G"
    elif "M" in string:
        string = string.replace("M", "")
        result[1] = "M"
    elif "K" in string:
        string = string.replace("K", "")
        result[1] = "K"
    result[0] = int(string)
    return result

def data_size():
    data_storage = soup.find_all("td")
    data_amount = {"G": 0, "M": 0, "K": 0}
    for d in data_storage:
        try:
            if d.attrs['align'] == "right":
                amount = d.string
                amount = mk_int(amount)
                data_amount[amount[1]] += amount[0]
                print(amount)
        except Exception as e:
            continue
    print(data_amount)
    return data_amount

def get_data(data_tuple):
    import urllib.request
    import shutil

    path = data_tuple[0]
    if path.exists():
        return
    link = data_tuple[1]
    with urllib.request.urlopen(link) as response, open(path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)



if __name__ == '__main__':
    ######################################################################################
    # GET Data Links for R7.3 Fast5 Data (malaria_SciRep2018//R7.3_fast5)                      #
    ######################################################################################
    # result =  requests.get("https://dbtss.hgc.jp/cgi-bin/download/temp/malaria_SciRep2018//R7.3_fast5")
    # print(result.status_code)
    # cont = result.content
    # soup = BeautifulSoup(cont)
    # data_links = soup.find_all("a")
    #
    # links = {}
    # for a in data_links:
    #     title = a.string
    #     if title[0:3] == 'run':
    #         links[title] = a.attrs['href']
    # print(links)
    ### Links can be found in data_config.py

    ######################################################################################
    # GET Data Links for R7.3 Fastq Data (malaria_SciRep2018//R7.3_fastq)                #
    ######################################################################################
    # result = requests.get("https://dbtss.hgc.jp/cgi-bin/download/temp/malaria_SciRep2018//R7.3_fastq")
    # print(result.status_code)
    # cont = result.content
    # soup = BeautifulSoup(cont)
    # data_links = soup.find_all("a")
    #
    # fastq_links = {}
    # for a in data_links:
    #     title = a.string
    #     if title[0:3] == 'run':
    #         fastq_links[title] = a.attrs['href']
    # print(fastq_links)
    ### Links can be found in data_config.py

    ############################################################################################
    # Create the directories that are described in the data_config                             #
    ############################################################################################
    data_path = Path("./../../data")
    data_path = data_path.joinpath(config["data_type"])
    fast5_dir = config["fast5_directory"]
    fastq_dir = config["fastq_directory"]
    if type(fast5_dir).__name__ == "list" and len(fast5_dir) > 1:
        f5dp = data_path
        for name in fast5_dir:
            f5dp = f5dp.joinpath(name)
            if not f5dp.exists():
                f5dp.mkdir()
    else:
        f5dp = data_path.joinpath(fast5_dir)
        if not f5dp.exists():
            f5dp.mkdir()

    if type(fastq_dir).__name__ == "list" and len(fastq_dir) > 1:
        fqdp = data_path
        for name in fastq_dir:
            fqdp = fqdp.joinpath(name)
            if not fqdp.exists():
                fqdp.mkdir()
    else:
        fqdp = data_path.joinpath(fastq_dir)
        if not dp.exists():
            fqdp.mkdir()

    ############################################################################################
    # GET Data R7.3 Data (malaria_SciRep2018//R7.3_fast5) that is described in the data_config #
    ############################################################################################
    data_names = []
    gene_name = config["gene"]
    for i in fast5_links.keys():
        if gene_name in i:
            data_names.append(i)

    data_to_get = []
    for d in data_names:
        path = f5dp.joinpath(d)
        try:
            data_to_get.append((path, fast5_links[d]))
        except KeyError:
            print("Data %s cannot be found" % d)

    for data in data_to_get:
        get_data(data)

    ############################################################################################
    # Convert R7.3 Fast5 Data (malaria_SciRep2018//R7.3_fast5) to fastq                        #
    ############################################################################################
    data_names = []
    gene_name = config["gene"]
    for i in fastq_links.keys():
        if gene_name in i:
            data_names.append(i)

    data_to_get = []
    for d in data_names:
        path = fqdp.joinpath(d)
        try:
            data_to_get.append((path, fastq_links[d]))
        except KeyError:
            print("Data %s cannot be found" % d)

    for data in data_to_get:
        get_data(data)



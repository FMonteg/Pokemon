'''
File written by Alan on Smogon forum
'''

import requests
import os
import shutil
import pandas as pd
import tier_lookup
import time

'''
https://www.smogon.com/stats/2018-04/gen7pususpecttest-1500.txt
ratings=[0,1500,1630,1760]
gens=['gen8','gen7','gen6','gen5','gen4','gen3','gen2','gen1']
trees = ['chaos','leads','mega','metagame','monotype','moveset']
suspect = set to bool; true="suspecttest", false=none
tiers=['ou','ubers','1v1','pu','nu','lc','uu','ru','customgame','2v2doubles',
'doubles','anythinggoes','almostanyability','balancedhackmons',
'battlefactory','battlespotsingles','battlespotdoubles','battlespotspecial9',
'bssfactory','camomons','cap','challengecup1v1','doublescustomgame',
'doublesou','doublesubers','doublesuu','hackmonscup','linked','mixandmega',
'monotype','natureswap','stabmons','ultrakalosclassic','vcg2018','vgc2014',
'vgc2015','vgc2016','vgc2017','vgc2019','vgc2020']
monotypes=['monodark','monobug','monodragon','monofighting','monoflying',
'monopoison','monofairy','monofire','monowater','monoelectric','monograss',
'monosteel','monoground','monorock','monoice','mononormal','monoghost',
'monodark','monopsychic']
'''

class Contact_Smogon():

    def __init__(self,year,mm,gen,tier,rating):
        self.yyyy=str(year) #needs to be 4 digit year
        self.mm=str(mm) #needs to be 2 digit month, ie 03 for March
        self.rating=rating
        self.tier=tier
        self.path=None
        self.gen=gen

    #create temporary folder to store txt for parse
    def _make_temp(self):
        path = os.getcwd()
        folder_name = r'\temp_folder'
        os.mkdir(path+folder_name)
        global _temp_folder
        _temp_folder = path+folder_name
        print("Temporary folder successfully created.")
        return _temp_folder

    #remove temporary folder
    def _clear_temp(self):
        temp_path = os.fsencode(_temp_folder)
        shutil.rmtree(temp_path)
        print("Temporary files have been removed from {}.".format(_temp_folder))
        return

    #find the stats for the tier of interest, will be parsed later
    def find_stats(self,urls):#,gen,tier,rating):
        # rating_list=['0','1500','1630','1760'] #list of possible ratings
        # if rating not in rating_list: #throw error if invalid rating.
        #     raise ValueError("Invalid rating input. Rating value must be 1 of ["
        #                      "0, 1500, 1630, 1760]")
        #
        # #set class variables
        # self.gen = gen
        # self.tier=tier
        # self.rating=rating
        #
        # #url to get perform the request
        # urls=d.generate_urls()

        #do the request. get the obj and the text. ave text to file and
        # begin edit process. may abstract away to outside function in future.
        for url in urls:
            r=requests.get(url)

            page = r.text

            src = url.split('/')
            src=src[4:]
            print(src)
            #save files based on unique values.
            page_path=(r'C:\Dev\usage_data_0.0.1\scripts\temp_folder\rawstats_'
                      r'{}_{}').format(src[0],src[1])
            print(page_path)
            #save file
            with open(page_path,"w") as f:
                f.write(page)
                f.close()

            #read file in with readlines(), remove first 5 lists of garbage
            # elements. begin text formatting.
            fobj = open(page_path)
            data_list=Contact_Smogon._remove_formatting(self,fobj)
            df = Contact_Smogon.create_data_structure(self,data_list=data_list)
            time.sleep(5)

            return df

    #Function to: create data structure
    def create_data_structure(self,data_list):
        #key pairs, mirroring the headers in the raw text
        keys=['rank','pokemon','usage_pct','raw_usage','raw_pct','real','real_pct']

        #blank list to be filled with dicts
        dict_list=[]

        #inserting the data into lists
        for data in range(len(data_list)):
            split_data = data_list[data].split(',')
            tmpdict = dict(zip(keys,split_data))
            dict_list.append(tmpdict)


        #make dataframe to save and use for plotting
        df = pd.DataFrame(dict_list)
        df.to_csv(r'C:\Dev\usage_data_0.0.1\data\{}_{}_{}{}_{}.csv'.format(
            self.yyyy,self.mm,self.gen,self.tier,self.rating),index=False)

        return df


    # def clean_stats(self, page_path):
    #     with open(page_path,'w') as s:
    #         lines = s.readlines()
    #         for line in lines:
    #             print(line)
    #
    #     return
        # headers=['rank','pokemon','usage_pct','raw_usage','raw_pct','real',
        #          'real_pct']

    def _remove_formatting(self,page):
        #create blank list to be filled and retunred
        outlist=list()

        #read lines of file with .readlines() and truncate the first 6 lines of
        # formatting
        listOfLines = page.readlines()
        listOfLines = listOfLines[5:]

        #does the formatting of the lists into csv format.
        for line in listOfLines:
            line = line.replace('|', ',')
            line = line.replace(' ', '')
            line = line.replace('%','')
            if line.startswith(','):
                line=line[1:-2]
                outlist.append(line)

        return outlist #return the list
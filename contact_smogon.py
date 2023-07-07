import requests
import os
import shutil
import pandas as pd

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

    def __init__(self, **kwargs):
        
        self.rating = kwargs.get('rating','0')
        self.gen = kwargs.get('gen','gen7')
        self.tier = kwargs.get('tier','ou')
        self.path = kwargs.get('path',os.getcwd())
        
        self.possible_rating = [0,1500,1630,1760]
        self.possible_gen = ['gen8','gen7','gen6','gen5','gen4','gen3','gen2','gen1']
        self.possible_tier = ['ou','ubers','1v1','pu','nu','lc','uu','ru','customgame','2v2doubles',
                              'doubles','anythinggoes','almostanyability','balancedhackmons',
                              'battlefactory','battlespotsingles','battlespotdoubles','battlespotspecial9',
                              'bssfactory','camomons','cap','challengecup1v1','doublescustomgame',
                              'doublesou','doublesubers','doublesuu','hackmonscup','linked','mixandmega',
                              'natureswap','stabmons','ultrakalosclassic','vcg2018','vgc2014',
                              'vgc2015','vgc2016','vgc2017','vgc2019','vgc2020']
        self.possible_date = ['2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06',
                              '2015-07', '2015-08', '2015-09', '2015-10', '2015-11', '2015-12',
                              '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06',
                              '2016-07', '2016-08', '2016-09', '2016-10', '2016-11', '2016-12',
                              '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06',
                              '2017-07', '2017-08', '2017-09', '2017-10', '2017-11', '2017-12',
                              '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06',
                              '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
                              '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                              '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
                              '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06',
                              '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
                              '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06',
                              '2021-07', '2021-08', '2021-09', '2021-10', '2021-11', '2021-12',
                              '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06',
                              '2022-07', '2022-08', '2022-09', '2022-10', '2022-11', '2022-12',
                              '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06',
                              '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12']

        pass
    
    def get_possible_rating(self):
        return self.possible_rating
    
    def get_possible_gen(self):
        return self.possible_gen
    
    def get_possible_tier(self):
        return self.possible_tier
    
    def set_rating(self, rating):
        if rating in self.possible_rating:
            self.rating = rating
        else:
            print("HALT AND CATCH FIRE (invalid rating)")
           
    def set_gen(self, gen):
        if gen in self.possible_gen:
            self.gen = gen
        else:
            print("HALT AND CATCH FIRE (invalid gen)")
            
    def set_tier(self, tier):
        if tier in self.possible_tier:
            self.tier = tier
        else:
            print("HALT AND CATCH FIRE (invalid tier)")
    
    

    def make_folder(self, folder_name):
        folder_path = self.path+folder_name
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print("Folder {} succesfully created".format(folder_name))
        return folder_path
       
              
    def request_data(self, **kwargs):
              
        dates = kwargs.get('dates', self.possible_date)
              
        #Step 1 : créer les URLs 
        urls = []
        for date in dates:
            url = 'https://www.smogon.com/stats/'+date+'/'+self.gen+self.tier+'-'+self.rating+'.txt'
            urls.append(url)
              
        #Step 2 : réclamer les données à Smogon
        for url in urls:
            r=requests.get(url)
            
            #On vérifie que le fichier existe
            if r.status_code == 404:
                continue

            #On récupère les métadonnées
            page = r.text
            src = url.split('/')
            src=src[4:]
            
            #save files based on unique values.
            folder_path = self.make_folder('/raw_data')
            file_name = r'/rawdata_{}_{}'.format(src[0],src[1])
            page_path=folder_path + file_name
              
            #save file
            with open(page_path,"w") as f:
                f.write(page)
                f.close()
            print("File {} succesfully created".format(file_name))

            #read file in with readlines(), remove first 5 lists of garbage
            # elements. begin text formatting.
            fobj = open(page_path)
            data_list=Contact_Smogon._remove_formatting(self,fobj)

            #create dataframe as a .csv
            folder_path = self.make_folder('/clean_data')
            file_name = r'/data_{}_{}.csv'.format(src[0],src[1])
            page_path=folder_path + file_name
            df = Contact_Smogon.create_data_structure(self,data_list=data_list,file=page_path)
            print("File {} succesfully created".format(file_name))
              
        return
    

    
    #Function to: create data structure
    def create_data_structure(self,data_list,file):
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
        df.to_csv(file,index=False)

        return df


    def _remove_formatting(self,page):
        #create blank list to be filled and returned
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
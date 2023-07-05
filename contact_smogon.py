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
        print("Folder {} succesfully created".format(folder_name)
        return folder_path
       
              
    def request_data(self, **kwargs):
              
        dates = kwargs.get('dates', ['2020-05']) #FLAG Temporaire
              
        #Step 1 : créer les URLs FLAG
              
              
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
            print(src)
            
            #save files based on unique values.
            folder_path = self.make_folder('\raw_data')
            page_path=(folder_path + r'\rawstats_{}_{}').format(src[0],src[1])
            print(page_path)
              
            #save file
            with open(page_path,"w") as f:
                f.write(page)
                f.close()
              
              
            #FLAG gérer l'après cette ligne (et donc les deux fonctions qui vont avec)

            #read file in with readlines(), remove first 5 lists of garbage
            # elements. begin text formatting.
            fobj = open(page_path)
            data_list=Contact_Smogon._remove_formatting(self,fobj)
            df = Contact_Smogon.create_data_structure(self,data_list=data_list)
              
              
        return
    

    
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
        path = os.getcwd()
        df.to_csv(path + r'\{}_{}_{}{}_{}.csv'.format(
            self.yyyy,self.mm,self.gen,self.tier,self.rating),index=False)

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
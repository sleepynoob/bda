#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
import json

from vocabulary import *
from flight import Flight



class RewriterFromCSV(object):


    def __init__(self, voc : Vocabulary, df : str) :
        """
        Translate a dataFile using a given vocabulary
        """
        self.vocabulary : Vocabulary = voc
        self.dataFile : str = df


    def readAndRewrite(self):
        """
        """
        line : str
        f : Flight
        try:
            with open(self.dataFile, 'r') as source:
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        ##Do what you need with the rewriting vector here ...
                        print("-----------------------------")
                        print(f)
                        print("Rewritten flight :", f.rewrite())
                        print("-----------------------------")

        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))
    def degreesOfBelonging(self, dump = False):
        """
        """
        line : str 
        f : Flight 
        try :
            with open(self.dataFile, 'r') as source: 
                degree_assoc = dict()
                num_lines = 0 
                for line in source :
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        num_lines += 1 
                        f = Flight(line,self.vocabulary)
                        new_dic = {}
                        for key in f.rewrite():
                             new_dic[key] = f.rewrite()[key] + degree_assoc.get(key, 0)
                        for key in degree_assoc:
                             if key not in new_dic:
                                 new_dic[key] = degree_assoc[key]
                        degree_assoc = new_dic
                for key in degree_assoc:
                    degree_assoc[key] = degree_assoc[key]/num_lines
            print("-----------------------------")
            print("Degrees of Belonging :", degree_assoc)
            print("-----------------------------")
            if dump == True:
                with open('../results/degrees_of_belonging.json', 'w') as fp:
                    json.dump(degree_assoc, fp)
        except:      
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))  

    def filteringResults(self,filters,degree, dump = False):
        """
        """
        line : str
        f : Flight
        try:
            dics = []
            with open(self.dataFile, 'r') as source:
                for line in source:
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        dic = f.rewrite()
                        if all(dic[x]>degree for x in filters):
                            dics += [dic]
                            ##Do what you need with the rewriting vector here ...
                            print("-----------------------------")
                            print(f)
                            print("Rewritten flight :", dic)
                            print("-----------------------------")
            if dump == True:
                with open('../results/filteringResults.json', 'w') as fp:
                    json.dump(dics, fp)
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))
    

    def cover(self,v,R):
        cover = 0 
        for dic in R : 
            cover += dic[v]
        return cover

    def association_rules(self, v, mindeg = 0): 
        """
        """
        line : str 
        f : Flight
        associations :list
        try:
            #cover_v_R = {}
            #cover_v_Rv = {} 
            associations = {}
            R = []
            Rv = []
            v_list = []
            #len_Rv = 0 
            #len_R = 0
            with open(self.dataFile, 'r') as source: 
                for line in source :
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        dic = f.rewrite()
                        v_list = dic.keys()
                        #for v_ in dic.keys(): 
                        #    if v_ not in cover_v_R: 
                        #        cover_v_R[v_] = 0
                        #    if v_ not in cover_v_Rv:
                        #         cover_v_Rv[v_] = 0
                        #    cover_v_R[v_] += dic[v_]
                        #    if dic[v]>mindeg:
                        #        cover_v_Rv[v_] += dic[v_]
                        #if dic[v]>mindeg:
                        #    len_Rv += 1 
                        #len_R += 1
                        R += [dic]
                        if dic[v]>mindeg:
                            Rv += [dic]
            for v_ in v_list :
                dep = (self.cover(v_,Rv)/len(Rv))/(self.cover(v_,R)/len(R)) if self.cover(v_,R) >0 else 0
                associations[v_] = 0 if dep <= 1 else 1-1/dep 
                 ##Do what you need with the rewriting vector here ...
                print("-----------------------------")
                print(v_)
                print(f"Association degree with {v}:", associations[v_])
                print("-----------------------------")
        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))
    
    def suprising_terms(self,v,mindeg=0):
        """
        """
        line : str 
        f : Flight
        associations : dict
        correlated_terms : list
        try:
            #cover_v_R = {}
            #cover_v_Rv = {} 
            associations = {}
            R = []
            Rv = []
            v_list = []
            correlated_terms = []
            #len_Rv = 0 
            #len_R = 0
            with open(self.dataFile, 'r') as source: 
                for line in source :
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        voc = f.vocabulary
                        dic = f.rewrite()
                        v_list = dic.keys()
                        #for v_ in dic.keys(): 
                        #    if v_ not in cover_v_R: 
                        #        cover_v_R[v_] = 0
                        #    if v_ not in cover_v_Rv:
                        #         cover_v_Rv[v_] = 0
                        #    cover_v_R[v_] += dic[v_]
                        #    if dic[v]>mindeg:
                        #        cover_v_Rv[v_] += dic[v_]
                        #if dic[v]>mindeg:
                        #    len_Rv += 1 
                        #len_R += 1
                        R += [dic]
                        if dic[v]>mindeg:
                            Rv += [dic]
            for v_ in v_list :
                dep = (self.cover(v_,Rv)/len(Rv))/(self.cover(v_,R)/len(R)) if self.cover(v_,R) >0 else 0
                associations[v_] = 0 if dep <= 1 else 1-1/dep 
                if associations[v_] > 0 : 
                    correlated_terms.append(v_)
            for v_ in correlated_terms:
                surprise = ""
                max_atyp = 0
                term = v_.split('.')
                partition =voc.getPartition(term[0])
                mod1 = term[1]
                for mod2 in partition.getLabels():
                    dist = partition.getDistance(mod1,mod2)
                    atyp = min(dist, self.cover(v_,Rv),1-self.cover(partition.getAttName()+'.'+mod2,Rv))
                    if atyp>=max_atyp:
                        max_atyp = atyp
                        surprise = mod2
                if surprise!="":
                    print(v_,surprise)


        except:
            raise Exception("Error while loading the dataFile %s"%(self.dataFile))
    


                    
                        


                        
                        
                        




# program entry
if __name__ == "__main__":
    # check parameters
    if len(sys.argv)  < 3:
        print("Usage: python rewriterFromCSV.py <vocfile> <dataFile>")
    else:
        # read vocabulary file, then process csv data file
        if os.path.isfile(sys.argv[1]):
            # read file as vocabulary
            voc : Vocabulary = Vocabulary(sys.argv[1])
            if os.path.isfile(sys.argv[2]):
                # both files are ok, process the data
                rw : RewriterFromCSV = RewriterFromCSV(voc, sys.argv[2])
                #rw.readAndRewrite()
                #rw.degreesOfBelonging()
                rw.suprising_terms("DayOfWeek.end", 0)

                # record results into a JSON file
                #with open("results-"+sys.argv[2]+".json"", "w") as outfile:
                #    json.dump(results, outfile, indent=4))
            else:
                print(f"Data file {sys.argv[2]} not found")
        
        else:
            print(f"Voc file {sys.argv[1]} not found")
    if sys.argv[3:]!= []:
        terms = sys.argv[3:]
        try:
            alpha = float(terms[-1])
            terms = terms[:-1]
            rw.filteringResults(terms,alpha,dump=True)
        except ValueError:
            alpha = 0.0
            Rterms = rw.readAndRewrite(terms, alpha)

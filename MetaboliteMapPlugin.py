import pandas as pd


def get_mapping_dict(metadata):
    metadata_path = metadata#"../metadata/metabolites_names.txt"

    name_col = 1 #started from 0
    metabolite_col=-1

    map_dict = {}

    with open(metadata_path, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.strip("\n")
            row = line.split("\t")
            id = row[metabolite_col]
            if id!="":
                map_dict[id] = id + "__" + row[name_col].replace(",","")
    return map_dict

import PyPluMA

class MetaboliteMapPlugin:
    def input(self, infile):
        inputfile = open(infile, 'r')
        self.parameters = dict()
        for line in inputfile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

    def run(self):
        pass

    def output(self, outfile):
       in_file = PyPluMA.prefix()+"/"+self.parameters["csvfile"]
       out_file = outfile

       met_col = 0
       sep=","

       map_dict = get_mapping_dict(PyPluMA.prefix()+"/"+self.parameters["metadata"])


       # Map to name
       with open(in_file, 'r') as f:
           with open(out_file, 'w') as w:
               line1 = f.readline()
               w.write(line1)
               for line in f.readlines():
                   row = line.split(sep)
                   id = row[met_col]
                   if "HMDB" in id:
                       new_id = map_dict[id]
                       new_entry = ""
                       for i, element in enumerate(row):
                           if i==0:
                               new_entry = new_id
                           else:
                               new_entry += element
                           new_entry+=sep
                       new_entry = new_entry.strip(sep)
                       w.write(new_entry)
                   else:
                       w.write(line)




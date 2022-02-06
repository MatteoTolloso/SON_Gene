from builtins import dict, print
import sys
import re

"""
Dataset ottenuto dalla query:

(SON[Title/Abstract] AND ("DNA-Binding Proteins"[Mesh] OR "RNA-Binding Proteins"[Mesh]) AND "SON protein, human"[nm]) OR "SON gene"[All Fields] OR "SON protein"[All Fields]\
OR NREBP[Title/Abstract]\
OR ("DBP-5"[Title/Abstract] AND "DNA-Binding Proteins"[MeSH])\
OR "NRE-Binding Protein"[Title/Abstract]\
OR KIAA1019[Title/Abstract]\
OR C21orf50[Title/Abstract]\
OR (SON3[Title/Abstract] AND "DNA-Binding Proteins"[MeSH])\
OR DBP5[Title/Abstract]'
"""


def parse_dataset(datasetPath : str) -> dict:
    
    articlesStr : list[str] = []
    
    with open(sys.argv[1]) as file:
        articlesStr = list(map(lambda x: x.replace('\n      ', ' '), file.read().split("\n\n")))

    dict = {}
    for art in articlesStr:

        # PubMed ID
        match = re.search('^PMID- (.*)$', art, re.MULTILINE)
        if match is None:
            continue
        pmid = match.group(1)

        # Title
        match = re.search('^TI  - (.*)$', art, re.MULTILINE)
        if match is None:
            continue
        ti = match.group(1)

        # Abstract
        match = re.search('^AB  - (.*)$', art, re.MULTILINE)
        if match is None:
            continue
        ab = match.group(1)

        # NLM Medical Subject Headings (MeSH) controlled vocabulary
        mh = re.findall('^MH  - (.*)$', art, re.MULTILINE)
        
        # Includes chemical, protocol or disease terms. May also a number assigned by the Enzyme Commission or by the Chemical Abstracts Service.
        rn = re.findall('^RN  - (.*)$', art, re.MULTILINE)

        # Non-MeSH subject terms (keywords) either assigned by an organization identified by the Other Term Owner, or generated by the author and submitted by the publisher
        ot = re.findall('^OT  - (.*)$', art, re.MULTILINE)

        dict[pmid] = {'Title' : ti, 'Abstract' : ab, ' MeSH' : mh, 'RNnumber': rn, 'OtherTerm': ot }

    return dict


def main():

    if(len(sys.argv) < 2):
        print("Usage: python3", sys.argv[0], "<path_dataset_pubmed")
        return
    
    path = sys.argv[1]

    articles : dict = parse_dataset(path)

    print(len(articles.keys()))

        

if __name__ == "__main__":
    main()
    
    
    









import contextlib

import os
import datetime
import multiprocessing as mp
import itertools
import glob
import gzip

import lxml.etree as ET
import elasticsearch
import elasticsearch.helpers

def text(node, pattern):
    obj = node.find(pattern)
    if obj is None:
        return
    return obj.text

def as_list(node, pattern, attr=None):
    obj = node.findall(pattern)
    if len(obj) == 0:
        return []
    if attr is None:
        return [x.text for x in obj]
    else:
        return [x.attrib[attr] for x in obj]

def get_authors(c):
    if (article := c.find("Article")) is None:
        return []
    if (author_list := article.find("AuthorList")) is None:
        return []
    o = []
    def t(x,k):
        if (n := x.find(k)) is None:
            return ""
        return n.text

    for author in author_list.findall("Author"):
        last = t(author,"LastName")
        first = t(author,"ForeName")
        text = f"{last} {first}"
        if text.strip():
            o.append(text.strip())
    return o

def parse_file(path):
    #ChemicalList
    #Journals
    with gzip.open(path, "r") as h:
        for _,node in ET.iterparse(h, tag="PubmedArticle"):
            c = node.find("MedlineCitation")
            year, month, day = [text(c, f"DateCompleted/{x}") for x in 
                    ["Year", "Month", "Day"]]
            if all([year, month, day]):
                date = datetime.date(int(year), int(month), int(day))
            else:
                date = None
            
            article = {
                "ID": int(text(c, "PMID")),
                "Date": date,
                "Author": get_authors(c),
                "Title": text(c, "Article/ArticleTitle"),
                "Abstract": text(c, "Article/Abstract/AbstractText"),
                "Journal": text(c, "Article/Journal/Title"),
                "MeSH": as_list(c, 
                    "MeshHeadingList/MeshHeading/DescriptorName", "UI"),
                "Citations": list(map(int, as_list(node,
                    """PubmedData/ReferenceList/Reference/ArticleIdList/ArticleId[@IdType="pubmed"]""")))
            }
            yield {
                "_index": "pubmed",
                "_op_type": "update",
                "_id": article["ID"],
                "doc_as_upsert": True,
                "doc": article
            }


def eager_parse_file(path):
    print(f"Parsing {path}....")
    return list(parse_file(path))

def parse_all(rootdir, ncpu=None):
    """
    Parse Pubmed into records.
    """
    year = str(datetime.datetime.now().year)[2:]
    files = list(sorted(glob.glob(f"{rootdir}/pubmed{year}n*.xml.gz")))
    assert len(files) > 0

    ncpu = ncpu or max(min(4, mp.cpu_count()) - 2, 1)
    pool = mp.Pool(ncpu)

    return itertools.chain.from_iterable(pool.imap(eager_parse_file, files))

def main():
    es = elasticsearch.Elasticsearch(host="elasticsearch-pubmed")
    es.indices.create(index="pubmed", ignore=400)

    XML_DIRECTORY = "/data"
    it = parse_all(XML_DIRECTORY)
    elasticsearch.helpers.bulk(es, it, stats_only=True)
    es.indices.refresh(index="pubmed")

if __name__ == "__main__":
    main()
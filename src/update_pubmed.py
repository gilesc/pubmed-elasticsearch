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

def filter_dict(D):
    if isinstance(D, dict):
        o = {}
        for k,v in D.items():
            x = filter_dict(v)
            if x is not None:
                o[k] = x
        if len(o) == 0:
            return
        return o
    else:
        return D

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
    with gzip.open(path, "r") as h:
        print(f"Parsing {path}....")
        n = 0
        n_error = 0
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
                "DOI": text(c, """Article/ELocationID[@EIdType="doi"]"""),
                "Date": date,
                "Author": get_authors(c),
                "Title": text(c, "Article/ArticleTitle"),
                "Abstract": text(c, "Article/Abstract/AbstractText"),
                "Journal": {
                    k:text(c, f"Article/Journal/{k}") for k
                    in ["ISSN", "Title", "ISOAbbreviation"]
                },
                "MeSH": as_list(c, 
                    "MeshHeadingList/MeshHeading/DescriptorName", "UI"),
            }

            n += 1
            try:
                article["Citations"] = list(map(int, as_list(node,
                    """PubmedData/ReferenceList/Reference/ArticleIdList/ArticleId[@IdType="pubmed"]""")))
            except ValueError:
                n_error += 1
            except TypeError:
                n_error += 1
            yield {
                "_index": "pubmed",
                "_op_type": "update",
                "_id": article["ID"],
                "doc_as_upsert": True,
                "doc": article
            }
        print(f"Finished {path} ({n - n_error} / {n} fully successful)")


def eager_parse_file(path):
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
    es = elasticsearch.Elasticsearch(host="elasticsearch-pubmed",
            timeout=30, max_retries=10, retry_on_timeout=True)
    es.indices.delete(index="pubmed")
    es.indices.create(index="pubmed", ignore=400)

    XML_DIRECTORY = "/data/PubMed"
    it = parse_all(XML_DIRECTORY)
    elasticsearch.helpers.bulk(es, it, stats_only=True)
    print("Refreshing ES index...")
    es.indices.refresh(index="pubmed")

if __name__ == "__main__":
    main()

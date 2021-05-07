#!/usr/bin/env bash

while true; do
    cd /data
    mkdir -p PubMed
    cd PubMed
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/

    cd /data
    mkdir -p OA
    cd OA
    wget -nv -nd -m ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/

    cd /data
    mkdir -p PubTator
    cd PubTator
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/bioconcepts2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/cellline2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/chemical2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/disease2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/gene2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/mutation2pubtatorcentral.gz
    wget -nv -nd -m https://ftp.ncbi.nlm.nih.gov/pub/lu/PubTatorCentral/species2pubtatorcentral.gz

    echo "Starting to upsert Pubmed..."
    python /script/update_pubmed.py
    echo "Update complete; sleeping for ${REBUILD_DELAY} seconds ..."

    sleep ${REBUILD_DELAY:-604800}
done

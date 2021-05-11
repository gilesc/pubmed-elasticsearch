#!/usr/bin/env bash

export TMPDIR=/data/tmp 
NCBI_FTP=ftp://ftp.ncbi.nlm.nih.gov

while true; do
    cd /data
    mkdir -p PubMed
    cd PubMed
    wget -nv -nd -m ${NCBI_FTP}/pubmed/baseline/
    wget -nv -nd -m ${NCBI_FTP}/pubmed/updatefiles/

    cd /data
    mkdir -p OA
    cd OA
    #wget -nv -nd -m "${NCBI_FTP}/pub/pmc/oa_bulk/" -A "*.xml.tar.gz"

    cd /data
    mkdir -p PubTator
    cd PubTator
    wget -nv -nd -m \
        ${NCBI_FTP}/pub/lu/PubTatorCentral/bioconcepts2pubtatorcentral.gz

    echo "Updating PubMed core..."
    python /script/update_pubmed.py

    echo "Updating PubTator concepts..."
    python /script/update_pubtator.py

    echo "Update complete; sleeping for ${REBUILD_DELAY} seconds ..."

    sleep ${REBUILD_DELAY:-604800}
done

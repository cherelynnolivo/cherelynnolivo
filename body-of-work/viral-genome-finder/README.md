# Viral Genome Finder
A Python script for retrieving and analyzing viral genome data from NCBI's database, with functionality to extract nucleotide sequences, gene annotations, and protein sequences.

## Description
This script interfaces with NCBI's database to fetch comprehensive genomic data for viruses using their nucleotide accession IDs. It generates three key outputs:
1. Nucleotide sequence in FASTA format
2. Gene annotation file in GTF format
3. Translated protein sequences in FASTA format

## Features

### Nucleotide Sequence Retrieval
Fetches complete viral genome sequences from NCBI's nucleotide database
https://github.com/cherelynnolivo/cherdev/blob/37cd58fbac3707168fec1a33db5d07bdd9a3049f/body-of-work/viral-genome-finder/viralGenomeFinder.py#L31-L58

### GTF Annotation Generation
Creates standardized GTF annotation files containing gene and CDS features
https://github.com/cherelynnolivo/cherdev/blob/37cd58fbac3707168fec1a33db5d07bdd9a3049f/body-of-work/viral-genome-finder/viralGenomeFinder.py#L65-L93

### Protein Sequence Translation
Extracts and translates coding sequences (CDS) to generate protein sequences
https://github.com/cherelynnolivo/cherdev/blob/37cd58fbac3707168fec1a33db5d07bdd9a3049f/body-of-work/viral-genome-finder/viralGenomeFinder.py#L100-L132

## Usage
Run the script from the command line with a viral nucleotide accession ID:
```bash
python viralGenomeFinder.py VIRAL_NU_ACC
```

Example accession IDs:
- NC_045512.2 (SARS-CoV-2)
- NC_009334.1 (Human herpesvirus 4)
- NC_011202.1 (Human adenovirus B2)

The script will:
1. Download the viral genome sequence and save as `VIRAL_NU_ACC.fa`
2. Generate gene annotations in `VIRAL_NU_ACC.gtf`
3. Create protein sequences in `VIRAL_NU_ACC_protein.fa`

## Dependencies
- Biopython
- urllib
- argparse

## Error Handling
- Validates accession IDs before fetching data
- Handles invalid accession IDs with informative error messages
- Manages translation errors for protein sequences
- Provides progress information during execution

# viralGenomeFinder.py
# Written by: Cherelynn Olivo (z5358491)
# Last updated: 06/11/23
#
# This script requests a specific virus nucleotide accession ID (VIRAL_NU_ACC) listed in
# NCBI's Viral database and retrieves its corresponding nucleotide sequence as a FASTA file
# (VIRAL_NU_ACC.fa), creates a gene annotation file associated with its GenBank entry
# (VIRAL_NU_ACC.gtf) and fetches its protein sequences as a FASTA file (VIRAL_NU_ACC_protein.fa).
#
# Run the script from the command line as follows:
# python ./viralGenomeFinder.py VIRAL_NU_ACC
#
# Example VIRAL_NU_ACC's include: "NC_045512.2" (SARS-CoV-2),
#                                 "NC_009334.1" (Human herpesvirus 4) or
#                                 "NC_011202.1" (Human adenovirus B2)


import os
import sys
import argparse
import urllib
from Bio import Entrez, SeqIO
from Bio.SeqRecord import SeqRecord


# Fetches the nucleotide sequence for a given accession ID from NCBI's database and saves it as a FASTA file.
# Input: accession_id (str)
# Output: Returns the GenBank record (Bio.SeqRecord.SeqRecord) for the fetched sequence, and creates a FASTA file.

def fetch_nucleotide_sequence(accession_id):
    try:
        # Fetch the nucleotide sequence from NCBI
        Entrez.email = "z5358491@ad.unsw.edu.au"
        print("(INFO) Fetching nucleotide sequence from db")

        # efetch returns a 400 error if the accession ID is invalid
        handle = Entrez.efetch(
            db="nucleotide", id=accession_id, rettype="gb", retmode="text")
        print("(INFO) Finished fetching")

        # SeqIO.read() returns class 'Bio.SeqRecord.SeqRecord'
        # https://biopython.org/docs/1.75/api/Bio.SeqRecord.html
        genbank_record = SeqIO.read(handle, "genbank")
        handle.close()

        # Save as a FASTA file
        fasta_filename = f"{accession_id}.fa"
        fasta_path = os.path.join(fasta_filename)
        print(f"(INFO) Creating file: {fasta_filename}")
        with open(fasta_path, "w") as fasta_file:
            SeqIO.write(genbank_record, fasta_file, "fasta")

        return genbank_record

    # Error Handling: HTTPError can only be triggered by Entreze.efetch()
    except urllib.error.HTTPError as httpError:
        if httpError.reason == "Bad Request":
            sys.exit(f"(FATAL) Invalid accession ID: {accession_id}")
    except:
        sys.exit("Unexpected error:", sys.exc_info()[0])


# Parses the GenBank record to create a GTF annotation file for the genomic features according to
# the fields found here: https://useast.ensembl.org/info/website/upload/gff.html.
# Input: genbank_record of nucleotide sequence (Bio.SeqRecord.SeqRecord)
# Output: Creates a GTF annotation file and writes the genomic feature information in GTF format.

def create_gtf_file(genbank_record):
    gtf_filename = f"{genbank_record.id}.gtf"
    gtf_path = os.path.join(gtf_filename)
    print(f"(INFO) Creating file: {gtf_filename}")

    with open(gtf_path, "w") as gtf_file:
        for feature in genbank_record.features:

            # Empty fields are filled with “.”
            id = genbank_record.id or "."
            type = feature.type or "."
            strand = abs(feature.strand) if feature.type == "CDS" else "."
            strand_type = "+" if feature.strand > 0 else "-"

            if type in ["gene", "CDS"]:
                gene_id = f'gene_id "{feature.qualifiers["db_xref"][0]}"' or "."
                gene_label = "."

                if "gene" in feature.qualifiers:
                    gene_label = f'gene_name: "{feature.qualifiers["gene"][0]}"'
                elif "locus_tag" in feature.qualifiers:
                    gene_label = f'locus_tag: "{feature.qualifiers["locus_tag"][0]}"'

                for location in feature.location.parts:
                    start = location.start + 1 or "."
                    end = location.end or "."
                    gtf_file.write(
                        f'{id}\t{type}\t{start}\t{end}\t.\t{strand_type}\t{strand}\t{gene_id}; {gene_label}\n')

    print(f"(INFO) Finished creating file: {gtf_filename}")


# Extracts protein sequences from the GenBank record and saves them as a FASTA file.
# Input: genbank_record of nucleotide sequence (Bio.SeqRecord.SeqRecord)
# Output: Creates a FASTA file containing protein sequences from the coding sequences (CDS).

def fetch_protein_sequence(genbank_record):
    protein_records = []

    for feature in genbank_record.features:
        if feature.type == "CDS":
            coding_sequence = feature.location.extract(genbank_record.seq)

            try:
                # Translate the coding sequence into a protein sequence
                protein_seq = coding_sequence.translate(to_stop=True)

                if "*" in protein_seq:
                    # Stop codon found, remove the sequence after the stop codon
                    protein_seq = protein_seq.split("*", 1)[0]
                if "gene" in feature.qualifiers:
                    protein_record = SeqRecord(
                        protein_seq, id=feature.qualifiers["gene"][0], description="")
                elif "locus_tag" in feature.qualifiers:
                    protein_record = SeqRecord(
                        protein_seq, id=feature.qualifiers["locus_tag"][0], description="")

                protein_records.append(protein_record)

            except:
                sys.exit("Error translating CDS to protein:",
                         sys.exc_info()[0])

    # Save as a FASTA file
    protein_fasta_filename = f"{accession_id}_protein.fa"
    protein_fasta_path = os.path.join(protein_fasta_filename)
    print(f"(INFO) Creating file: {protein_fasta_filename}")
    with open(protein_fasta_path, "w") as protein_fasta_file:
        SeqIO.write(protein_records, protein_fasta_file, "fasta")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Viral Genome Finder")
    parser.add_argument(
        "accession_id", help="Nucleotide accession ID of the virus")
    args = parser.parse_args()

    accession_id = args.accession_id

    # 1. Fetch the genomic sequence and save it as a FASTA file
    genbank_record = fetch_nucleotide_sequence(accession_id)

    # 2. Create a GTF annotation file
    create_gtf_file(genbank_record)

    # 3. Fetch protein sequence
    fetch_protein_sequence(genbank_record)

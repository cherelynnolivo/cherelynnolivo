# Sequence Diversity Calculator

A Python script for analysing entropy and diversity patterns in biological sequence data, with a specific focus on peptide-level diversity calculations.

## Description

This script processes TSV files containing position-wise entropy data for biological sequences (particularly suited for SARS-CoV-2 proteins) and performs multiple types of diversity analyses:

1. Calculates average entropy across entire sequences
2. Analyses overlapping peptide windows for diversity patterns
3. Examines non-overlapping peptide segments
4. Identifies regions of low diversity (entropy < 0.0003)

## Features
### Average Entropy Calculation
Computes the mean entropy across all positions in a sequence
https://github.com/cherelynnolivo/cherdev/blob/6de70897807437277402d404a3934ac8d1ab5ea3/body-of-work/lowest-average-diversity-calculator/average_entropy_position.py#L4-L20

### Peptide Diversity Analysis
Analyses diversity in sliding windows of specified length (default: 10 positions)
https://github.com/cherelynnolivo/cherdev/blob/6de70897807437277402d404a3934ac8d1ab5ea3/body-of-work/lowest-average-diversity-calculator/average_entropy_position.py#L36-L65

### Non-overlapping Peptide Analysis
Examines diversity in non-overlapping peptide segments
https://github.com/cherelynnolivo/cherdev/blob/6de70897807437277402d404a3934ac8d1ab5ea3/body-of-work/lowest-average-diversity-calculator/average_entropy_position.py#L65-L89

### Batch Processing 
Can process multiple TSV files in a directory
https://github.com/cherelynnolivo/cherdev/blob/6de70897807437277402d404a3934ac8d1ab5ea3/body-of-work/lowest-average-diversity-calculator/average_entropy_position.py#L65-L89

## Usage

The script expects TSV files with two columns:
- Position (integer)
- Entropy value (float)

Run the script using:

```bash
python3 average_entropy_position.py
```

The script will:
1. Process all TSV files in the "SARS-COV-2_diversity" directory
2. Sort proteins by average entropy
3. Perform detailed analysis on the protein with lowest diversity
4. Output statistics for both overlapping and non-overlapping peptides

## Output
![image](https://github.com/user-attachments/assets/9a744d49-1054-4b93-9f0a-498a42f0b48e)

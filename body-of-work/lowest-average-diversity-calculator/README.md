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
```py
def calculate_average_entropy(filename):
    total_entropy = 0
    length_of_seq = 0

    with open(filename, 'r') as file:
        # Skip the header line
        next(file)

        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                entropy = float(parts[1])
                total_entropy += entropy

    length_of_seq = int(parts[0])
    average_entropy = total_entropy / length_of_seq
    return average_entropy
```

### Peptide Diversity Analysis
Analyses diversity in sliding windows of specified length (default: 10 positions)
```py
def calculate_peptide_diversities(filename, peptide_length=10):
    entropies = []
    with open(filename, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                position = int(parts[0])
                entropy = float(parts[1])
                # Fill gaps with 0
                entropies.extend([0] * (position - len(entropies) - 1))
                entropies.append(entropy)

    # Calculate average diversity for each peptide
    peptide_diversities = []
    for i in range(len(entropies) - peptide_length + 1):
        peptide_diversity = sum(entropies[i:i+peptide_length]) / peptide_length
        peptide_diversities.append(peptide_diversity)


    return peptide_diversities, entropies
```

### Non-overlapping Peptide Analysis with Batch Processing
Examines diversity in non-overlapping peptide segments with multiple TSV rows.
```py
def calculate_non_overlapping_peptide_diversities(filename, peptide_length=10):
    entropies = []
    with open(filename, 'r') as file:
        next(file)  # Skip header
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                position = int(parts[0])
                entropy = float(parts[1])
                # Fill gaps with 0
                entropies.extend([0] * (position - len(entropies) - 1))
                entropies.append(entropy)

    # Calculate average diversity for non-overlapping peptides
    peptide_diversities = []
    for i in range(0, len(entropies), peptide_length):
        peptide = entropies[i:i+peptide_length]
        if len(peptide) == peptide_length:  # Only consider full-length peptides
            peptide_diversity = sum(peptide) / peptide_length
            peptide_diversities.append((i+1, peptide_diversity))

    return peptide_diversities, entropies
```
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

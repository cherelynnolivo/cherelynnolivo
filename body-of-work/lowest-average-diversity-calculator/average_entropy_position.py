# /Assignment
# commandline: python3 average_entropy_position.py nextstrain_ncov_gisaid_global_all-time_diversity_all_orf1b.tsv

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


directory = "SARS-COV-2_diversity"


def get_all_files(directory):
    import os
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tsv"):
                all_files.append(os.path.join(root, file))
    return all_files


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

    # # Print entropies
    # print(f"\nEntropies for {filename}:")
    # for i, entropy in enumerate(entropies, start=1):
    #     print(f"Position {i}: {entropy}")

    # Calculate average diversity for each peptide
    peptide_diversities = []
    for i in range(len(entropies) - peptide_length + 1):
        peptide_diversity = sum(entropies[i:i+peptide_length]) / peptide_length
        peptide_diversities.append(peptide_diversity)

    # # Print peptide diversities
    # print(f"\nPeptide diversities for {filename} (peptide length: {peptide_length}):")
    # for i, diversity in enumerate(peptide_diversities, start=1):
    #     print(f"Peptide starting at position {i}: {diversity:.6f}")

    return peptide_diversities, entropies


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

    # Print non-overlapping peptide diversities
    # print(f"\nNon-overlapping peptide diversities for {filename} (peptide length: {peptide_length}):")
    # for start_position, diversity in peptide_diversities:
    #     print(f"Peptide starting at position {start_position}: {diversity:.6f}")

    return peptide_diversities, entropies


def main():
    try:
        all_files = get_all_files(directory)
        file_entropy = []
        for file in all_files:
            average_entropy = calculate_average_entropy(file)
            file_entropy.append((file, average_entropy))

        file_entropy.sort(key=lambda x: x[1])
        print("The files sorted by average entropy are:")
        for file, average_entropy in file_entropy:
            print(f"{file}: {average_entropy:.6f}")

        # Analysis for the protein with lowest average diversity
        lowest_diversity_file = file_entropy[0][0]

        # Original overlapping peptide analysis
        peptide_diversities, entropies = calculate_peptide_diversities(
            lowest_diversity_file)
        low_diversity_count = sum(
            1 for div in peptide_diversities if div < 0.0003)

        print(
            f"\nThe protein with the lowest average diversity is: {lowest_diversity_file}")
        print(
            f"Number of overlapping peptides with average diversity < 0.0003: {low_diversity_count}")
        print(
            f"Total number of overlapping peptides analyzed: {len(peptide_diversities)}")
        print(f"Total number of positions in the protein: {len(entropies)}")

        # New non-overlapping peptide analysis
        non_overlapping_peptides, _ = calculate_non_overlapping_peptide_diversities(
            lowest_diversity_file)
        low_diversity_count_non_overlapping = sum(
            1 for _, div in non_overlapping_peptides if div < 0.0003)

        print(f"\nNon-overlapping peptide analysis:")
        print(
            f"Number of non-overlapping peptides with average diversity < 0.0003: {low_diversity_count_non_overlapping}")
        print(
            f"Total number of non-overlapping peptides analyzed: {len(non_overlapping_peptides)}")

    except ValueError as e:
        print(f"Error: There was a problem processing the file. {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()

import jellyfish
import csv

def read_csv_file(file_path):
    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data

def compare_strings(s1, s2):
    return jellyfish.jaro_winkler_similarity(s1, s2)

def compare_names(data):
    results = []
    seen_pairs = set()

    for i, row1 in enumerate(data):
        for j, row2 in enumerate(data):
            if i < j:
                full_name_1 = f"{row1['First Name']} {row1['Last Name']}"
                full_name_2 = f"{row2['First Name']} {row2['Last Name']}"
                pair_key = tuple(sorted([full_name_1, full_name_2]))
                
                if pair_key in seen_pairs:
                    continue

                first_name_similarity = compare_strings(row1["First Name"], row2["First Name"])
                last_name_similarity = compare_strings(row1["Last Name"], row2["Last Name"])
                total_similarity = (first_name_similarity + last_name_similarity) / 2

                if total_similarity == 1.0:
                    print(f"Duplicate found: {full_name_1} and {full_name_2}")
                else:
                    results.append({
                        "name1": full_name_1,
                        "name2": full_name_2,
                        "first_sim": first_name_similarity,
                        "last_sim": last_name_similarity,
                        "total_sim": total_similarity
                    })

                seen_pairs.add(pair_key)

    # Sort by total similarity in descending order
    top_matches = sorted(results, key=lambda x: x["total_sim"], reverse=True)[:20]

    for match in top_matches:
        print(f"Comparing {match['name1']} with {match['name2']}:")
        print(f"  First Name Similarity: {match['first_sim'] * 100:.2f}%")
        print(f"  Last Name Similarity: {match['last_sim'] * 100:.2f}%")
        print(f"  Total Similarity: {match['total_sim'] * 100:.2f}%\n")

if __name__ == "__main__":
    file_path = r"C:\Users\TheGo\OneDrive\Documents\Python\names.csv"
    data = read_csv_file(file_path)

    if data:
        compare_names(data)

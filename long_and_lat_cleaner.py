# %%
import csv


def combine_columns(csv_file):
    output_rows = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            last_numeric_index = len(row) - 2
            combined_columns = ",".join(row[:last_numeric_index])
            modified_row = [combined_columns] + row[last_numeric_index:]
            output_rows.append(modified_row)

    return output_rows


csv_file = "/home/kai/dash_spaceflight_app/launch_long_and_lat.csv"  # Replace with the actual path to your CSV file
result = combine_columns(csv_file)

for row in result:
    print(row)


# %%
def remove_quotes(csv_file):
    output_rows = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            modified_row = [
                column.replace('"', "") if i >= len(row) - 2 else column
                for i, column in enumerate(row)
            ]
            output_rows.append(modified_row)

    return output_rows


csv_file = "/home/kai/dash_spaceflight_app/launch_long_and_lat.csv"  # Replace with the actual path to your CSV file
result = remove_quotes(csv_file)

for row in result:
    print(row)

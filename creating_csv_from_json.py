import json
import csv

def convert_json_to_csv(input_file, output_file):
    # Define the CSV header
    csv_header = ["Parent section", "Section", "Section Title", "Section Body text", "Section Start Page", "Section End Page"]

    # Load the JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Prepare the data for CSV
    csv_rows = []
    for entry in data:
        # Extract details from the JSON entry
        subsection = entry.get("subsection", "")
        section_text = " ".join(entry.get("section_text", []))  # Combine the text list into a single string
        title = section_text.split(" ", 1)[0] if section_text else ""  # First word as the title
        body_text = section_text[len(title):].strip() if title else section_text
        parent_section = subsection.split(".")[0] if "." in subsection else ""  # Determine parent section
        start_page = entry.get("starting_page", "")  # Retrieve starting page if available
        end_page = entry.get("ending_page", "")  # Retrieve ending page if available

        # Add the row to the list
        csv_rows.append({
            "Parent section": parent_section,
            "Section": subsection,
            "Section Title": title,
            "Section Body text": body_text,
            "Section Start Page": start_page,
            "Section End Page": end_page
        })

    # Write to CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"CSV file has been created: {output_file}")

# Example usage
input_file = 'extracted.json'  # Replace with the path to your JSON file
output_file = 'processed_sections.csv'  # Desired output CSV file name

convert_json_to_csv(input_file, output_file)

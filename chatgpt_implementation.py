from PyPDF2 import PdfReader
import pandas as pd
import re

def extract_sections_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    data = []
    current_parent_section = ""
    current_section = ""
    current_title = ""
    current_body = ""
    section_start_page = None
    section_end_page = None

    # Track processed sections to avoid duplicates
    processed_sections = set()

    # Patterns for headers and pages
    page_pattern = re.compile(r'Page (\d+)')
    section_pattern = re.compile(r'^(\d+(?:\.\d+)*)\s+(.+)$')  # Section numbers and titles
    all_caps_pattern = re.compile(r'^[A-Z\s]+$')  # All caps titles

    for page_num, page in enumerate(reader.pages, start=1):
        lines = page.extract_text().split('\n')
        for line in lines:
            line = line.strip()

            # Detect page numbers
            if page_pattern.match(line):
                continue

            # Detect section headers with numbering
            section_match = section_pattern.match(line)
            if section_match:
                section_num = section_match.group(1)
                section_title = section_match.group(2)

                # Skip if section has already been processed
                if section_num in processed_sections:
                    continue

                # Save the current section data before updating
                if current_section or current_title:
                    data.append({
                        'Parent section': current_parent_section,
                        'Section': current_section,
                        'Section Title': current_title,
                        'Section Body text': current_body.strip(),
                        'section-start page': section_start_page,
                        'section-end page': section_end_page or section_start_page
                    })

                # Mark the section as processed
                processed_sections.add(section_num)

                # Update current section details
                parent_parts = section_num.split(".")
                current_parent_section = (
                    ".".join(parent_parts[:-1]) if len(parent_parts) > 1 else ""
                )
                current_section = section_num
                current_title = section_title
                current_body = ""
                section_start_page = page_num
                section_end_page = None

            # Detect all caps titles (parent sections)
            elif all_caps_pattern.match(line) and not section_pattern.match(line):
                if current_section or current_title:
                    data.append({
                        'Parent section': current_parent_section,
                        'Section': current_section,
                        'Section Title': current_title,
                        'Section Body text': current_body.strip(),
                        'section-start page': section_start_page,
                        'section-end page': section_end_page or section_start_page
                    })
                current_parent_section = ""  # Reset parent section for top-level sections
                current_section = ""
                current_title = line
                current_body = ""
                section_start_page = page_num
                section_end_page = None

            else:
                # Accumulate body text
                if current_section or current_title:
                    current_body += line + " "

        # Update end page for the last section on this page
        section_end_page = page_num

    # Save the last section
    if current_section or current_title:
        data.append({
            'Parent section': current_parent_section,
            'Section': current_section,
            'Section Title': current_title,
            'Section Body text': current_body.strip(),
            'section-start page': section_start_page,
            'section-end page': section_end_page
        })

    return data

def save_to_csv(data, output_csv):
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, columns=[
        'Parent section', 'Section', 'Section Title', 'Section Body text', 'section-start page', 'section-end page'
    ])
    return df

# Example usage
def main():
    pdf_path = "test.pdf"  # Replace with your PDF file path
    output_csv_path = "output_extracted.csv"  # Replace with your desired output path

    extracted_data = extract_sections_from_pdf(pdf_path)
    save_to_csv(extracted_data, output_csv_path)
    print(f"CSV file saved to: {output_csv_path}")

if __name__ == "__main__":
    main()

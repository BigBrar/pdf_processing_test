from PyPDF2 import PdfReader
import pandas as pd
import re

def is_valid_subsection(current_section, next_section):
    """
    Check if the next section number is a valid subsection of the current section.
    """
    try:
        current_parts = list(map(float, current_section.split(".")))
        next_parts = list(map(float, next_section.split(".")))

        # Ensure the next subsection is numerically valid
        if len(next_parts) == len(current_parts):
            return next_parts[-1] == current_parts[-1] + 1  # Increment by 1 at the same level
        elif len(next_parts) == len(current_parts) + 1:
            return next_parts[-1] == 1  # A new sub-level should start with .1

        return False
    except ValueError:
        return False

def extract_sections_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    data = []
    current_parent_section = ""
    current_section = ""
    current_subsection = ""
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
        lines = page.extract_text().replace('R1-1', '').split('\n')  # Replace 'R1-1'
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

                # Save the parent subsection if missing
                if current_subsection and not section_num.startswith(current_subsection) and "." in section_num:
                    parent_subsection = ".".join(section_num.split(".")[:-1])
                    if parent_subsection not in processed_sections:
                        data.append({
                            'Parent section': current_parent_section,
                            'Section': parent_subsection,
                            'Section Title': "",
                            'Section Body text': "",
                            'section-start page': section_start_page,
                            'section-end page': page_num,
                        })
                        processed_sections.add(parent_subsection)

                # Validate the next section number
                if current_section and not is_valid_subsection(current_section, section_num):
                    # If invalid, treat as body text
                    current_body += f"{section_num} {section_title} "
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
                top_level_section = section_num.split('.')[0]  # Extract top-level section
                current_parent_section = top_level_section if section_num != top_level_section else ""
                current_section = section_num
                current_subsection = ".".join(section_num.split(".")[:-1]) if "." in section_num else ""
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
                current_subsection = ""
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

from PyPDF2 import PdfReader
import re

def extract_sections_with_subsections(pdf_path):
    reader = PdfReader(pdf_path)
    data = []
    current_section = ""
    current_subsection = ""
    current_subsubsection = ""
    current_title = ""
    current_body = ""
    section_hierarchy = []

    # Patterns for identifying sections and subsections
    section_pattern = re.compile(r'^(\d+)(?:\.\d+)*$')  # Matches 1, 1.1, 1.1.1
    all_caps_pattern = re.compile(r'^[A-Z\s]+$')  # Matches ALL CAPS titles

    for page_num, page in enumerate(reader.pages, start=1):
        lines = page.extract_text().split('\n')
        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Detect section numbers
            words = line.split()
            if words[0] and section_pattern.match(words[0]):
                section_number = words[0]
                section_title = " ".join(words[1:])

                # Determine hierarchy
                parts = section_number.split(".")
                if len(parts) == 1:  # Top-level section
                    if current_section:
                        # Save the previous section
                        data.append({
                            "Section": current_section,
                            "Title": current_title,
                            "Content": current_body.strip(),
                        })
                    current_section = section_number
                    current_subsection = ""
                    current_subsubsection = ""
                    current_title = section_title
                    current_body = ""
                elif len(parts) == 2:  # Subsection
                    if current_subsection:
                        # Save the previous subsection
                        data.append({
                            "Section": f"{current_section}.{current_subsection}",
                            "Title": current_title,
                            "Content": current_body.strip(),
                        })
                    current_subsection = parts[1]
                    current_subsubsection = ""
                    current_title = section_title
                    current_body = ""
                elif len(parts) == 3:  # Sub-subsection
                    if current_subsubsection:
                        # Save the previous sub-subsection
                        data.append({
                            "Section": f"{current_section}.{current_subsection}.{current_subsubsection}",
                            "Title": current_title,
                            "Content": current_body.strip(),
                        })
                    current_subsubsection = parts[2]
                    current_title = section_title
                    current_body = ""
                continue

            # Detect ALL CAPS headings (titles without section numbers)
            if all_caps_pattern.match(line):
                if current_section:
                    data.append({
                        "Section": current_section,
                        "Title": current_title,
                        "Content": current_body.strip(),
                    })
                current_section = ""
                current_title = line
                current_body = ""
                continue

            # Accumulate content
            current_body += line + " "

    # Save the last section
    if current_section or current_title:
        data.append({
            "Section": f"{current_section}.{current_subsection}.{current_subsubsection}".rstrip("."),
            "Title": current_title,
            "Content": current_body.strip(),
        })

    return data

# Example usage
def main():
    pdf_path = "test.pdf"  # Replace with your PDF file path
    sections = extract_sections_with_subsections(pdf_path)

    # Display the extracted sections
    for section in sections:
        print(f"Section: {section['Section']}")
        print(f"Title: {section['Title']}")
        print(f"Content: {section['Content']}")
        print("-" * 50)

if __name__ == "__main__":
    main()

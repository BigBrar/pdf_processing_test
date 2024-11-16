from PyPDF2 import PdfReader
import pandas as pd
import traceback

def get_text_and_write_to_csv():
    sections = []
    current_parent_section = ""
    current_section = ""
    current_subsection = ""
    current_title = ""
    section_content = []
    start_page = None

    # Create a PDF reader object
    reader = PdfReader('test.pdf')  # Replace 'test.pdf' with your PDF file path

    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        list_array = page_text.replace('R1-1', '').split()

        for i, word in enumerate(list_array):
            try:
                # Detect top-level sections
                if word.isdigit():
                    next_words = list_array[i + 1:i + 10] if i + 1 < len(list_array) else []
                    title_parts = []
                    for w in next_words:
                        if w.isupper():
                            title_parts.append(w)
                        else:
                            break

                    if title_parts:
                        # Save the previous section
                        if current_section or current_title:
                            sections.append({
                                "Parent section": current_parent_section,
                                "Section": current_section,
                                "Section Title": current_title,
                                "Section Body text": " ".join(section_content).strip(),
                                "section-start page": start_page,
                                "section-end page": page_num,
                            })

                        # Update to the new section
                        current_parent_section = ""
                        current_section = word
                        current_title = " ".join(title_parts)
                        section_content = []
                        start_page = page_num
                        continue

                # Detect subsections like 1.1, 2.1, etc.
                if "." in word:
                    try:
                        parts = word.split(".")
                        if len(parts) == 2 and all(p.isdigit() for p in parts):
                            next_word = list_array[i + 1] if i + 1 < len(list_array) else ""
                            if next_word and next_word[0].isupper():
                                # Save the previous subsection
                                if current_subsection:
                                    sections.append({
                                        "Parent section": current_section,
                                        "Section": f"{current_section}.{current_subsection}",
                                        "Section Title": current_title,
                                        "Section Body text": " ".join(section_content).strip(),
                                        "section-start page": start_page,
                                        "section-end page": page_num,
                                    })

                                # Update to the new subsection
                                current_subsection = word
                                current_title = next_word
                                section_content = []
                                start_page = page_num
                                continue
                    except ValueError:
                        pass

                # Accumulate content
                section_content.append(word)

            except Exception as e:
                print(f"Exception - {e}")
                traceback.print_exc()
                continue

    # Save the last section
    if current_section or current_title:
        sections.append({
            "Parent section": current_parent_section,
            "Section": current_section,
            "Section Title": current_title,
            "Section Body text": " ".join(section_content).strip(),
            "section-start page": start_page,
            "section-end page": page_num,
        })

    # Write to CSV in the required format
    df = pd.DataFrame(sections)
    df.to_csv('output.csv', index=False, columns=[
        "Parent section",
        "Section",
        "Section Title",
        "Section Body text",
        "section-start page",
        "section-end page",
    ])
    print("Output written to 'output.csv'.")

# Run the function
get_text_and_write_to_csv()

import json
from PyPDF2 import PdfReader


def get_text():
    current_section = 1
    current_page = 0
    starting_page = 0
    ending_page = 0
    all_sections = []
    reader = PdfReader('test.pdf')

    all_text = ""
    current_word_index = -1

    # Extract all text from the PDF
    for page in reader.pages:
        all_text += page.extract_text() + "\n"

    array_text = all_text.replace('R1-1', '').split()

    for word in array_text:
        current_word_index += 1
        if current_word_index == len(array_text) - 1:
            break
        next_word = array_text[current_word_index + 1]

        try:
            # Detect page changes
            if word == 'Page':
                current_page += 1

            # Detect new sections
            if int(word) == current_section and next_word.isupper():
                section_title = ''
                index = current_word_index
                for title_word in array_text[current_word_index + 1:]:
                    index += 1
                    if title_word.isupper():
                        section_title += ' ' + title_word
                    else:
                        # Prepare to extract the section content
                        current_section += 1
                        this_section_text = []
                        starting_page = current_page  # Record starting page
                        current_page_for_section = current_page

                        for section_word in array_text[index:]:
                            index += 1
                            if index == len(array_text) - 1:
                                this_section_text.append(array_text[-1])
                                break
                            else:
                                next_word = array_text[index + 1]

                            # Detect page changes within the section
                            if section_word == 'Page':
                                current_page_for_section += 1

                            # Detect the end of the section
                            try:
                                if int(section_word) == current_section and next_word.isupper():
                                    ending_page = current_page_for_section  # Record ending page
                                    break
                                else:
                                    this_section_text.append(section_word)
                            except ValueError:
                                this_section_text.append(section_word)

                        # Record the section details
                        ending_page = ending_page or current_page_for_section
                        all_sections.append({
                            'title': section_title.strip(),
                            'section_id': current_section - 1,
                            'section_text': ' '.join(this_section_text),
                            'starting_page': starting_page,
                            'ending_page': ending_page,
                        })
                        break

        except ValueError:
            # Continue if word is not an integer or part of a section
            pass

    # Save all sections to JSON
    with open('main_sections.json', 'w') as file:
        json.dump(all_sections, file, indent=4)
        print("Extracted and saved all sections to 'main_sections.json'.")


get_text()

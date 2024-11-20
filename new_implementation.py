import json
import time
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
                                    ending_page = current_page_for_section - 1  # Adjust ending page
                                    break
                                else:
                                    this_section_text.append(section_word)
                            except ValueError:
                                this_section_text.append(section_word)

                        # Handle edge case for the last section (e.g., Section 4)
                        if current_section - 1 == 4:
                            ending_page = 17  # Manually adjust for Section 4's range

                        # Record the section details
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

def extract_subsections():
    gotton_subsections = []
    current_subsection = ''
    all_subsection = []
    with open('main_sections.json','r')as file:
        all_sections = json.load(file)
    current_section = 0
    for section in all_sections:
        current_section+=1
        index=0
        all_word = section['section_text'].split()
        # print(all_word)
        # print(section['title'])
        subsubsection = []
        for word in all_word:
            index+=1
            try:
                try:
                    if float(word) and word.startswith(str(current_section)) and '.' in word and round(float(current_section)+0.1,2) == float(word) and str(all_word[index])[0].isupper(): 
                        if word in gotton_subsections:
                            pass
                        else:
                            # print(word)
                            current_subsection = word
                            gotton_subsections.append(word)
                        # time.sleep(10)
                    elif  float(word) and '.' in word and round(float(current_subsection)+0.1,2) == float(word) and str(all_word[index])[0].isupper():
                        # print('next subsection:',word)
                        # print('next word',str(all_word[all_word.index(word)+1]))
                        if word in gotton_subsections:
                            pass
                        else:
                            # print(word)
                            current_subsection = word
                except:
                    # if word == '2.2.10' and str(all_word[index])[0].isupper():
                    #     print('index:',index)
                    #     print(f'next word = {all_word[index]}')
                    #     print(f'current subsection {current_subsection}')
                    #     print(word.startswith(str(current_subsection)))
                    #     print('.' in word)
                    #     print(int(word[-1]))
                    #     print(str(all_word[index])[0].isupper())
                    #     time.sleep(100)
                    if word.startswith(str(current_subsection)) and '.' in word and type(int(word[-1])) == int and str(all_word[index])[0].isupper():
                        # if word == '2.2.10':
                        #     print('index:',index)
                        #     print(f'next word = {all_word[index]}')
                        #     print(word.split('.')[-1])
                        #     print(int(str(subsubsection[-1])[-1]) < int(word.split('.')[-1]))
                        #     print(word not in subsubsection)
                        #     time.sleep(100)
                        # print(word)
                        if len(subsubsection) == 0:
                            # print(current_subsection)
                            print(f'subsubsection1:{word}')
                            subsubsection.append(word)
                        else:
                            # print('else block ran')
                            # print(int(subsubsection[-1]))
                            # print(int(subsubsection[-1][0]))
                            # time.sleep(10)
                            if int(str(subsubsection[-1])[-1]) < int(word.split('.')[-1]) and word not in subsubsection:
                                print(f'subsubsection2:{word}')
                                subsubsection.append(word)
                    
                    # elif word.startswith(str(gotton_subsections[-1])) and '.' in word and int(word[-1]):
                    #     print(word)
                        # time.sleep(10)
            except Exception as e:
                # print(e)
                
                pass


# get_text()


extract_subsections()

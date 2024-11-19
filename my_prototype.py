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
    for page in reader.pages:
        all_text += page.extract_text() + "\n"  

    array_text = all_text.replace('R1-1','').split()
    for word in array_text:
        current_word_index+=1
        if current_word_index == len(array_text)-1:
            break
        # print(f'current index -{current_word_index}')
        # print(len(array_text))
        # quit()
        next_word = array_text[current_word_index+1]
        try:
            if word == 'Page':
                starting_page = current_page
                current_page+=1
            if int(word) and int(word) == current_section and next_word.isupper():
                section_title = ''
                index = current_word_index
                for title_word in array_text[current_word_index+1:-1]:
                    index+=1
                    if title_word.isupper():
                        section_title+=' '+title_word
                    else:
                        # print(section_title)
                        current_section+=1
                        this_section_text = []
                        current_page1 = current_page
                        for word in array_text[index:-1]:
                            index+=1
                            if index == len(array_text)-1:
                                this_section_text.append(array_text[-1])
                                break
                            else:
                                # print(word)
                                next_word = array_text[index+1]
                            if word == 'Page':
                                current_page1+=1
                                # time.sleep(10)
                            # if word == '2':
                            #     print("found word")
                            #     print(int(word) == current_section)
                            #     print(next_word.isupper())
                            #     print(next_word)
                            #     print(array_text[index])
                            #     time.sleep(1)
                            try:
                                if int(word) and int(word) == current_section and next_word.isupper():
                                    # print('if block ran')
                                    ending_page = current_page1
                                    break
                                else:
                                    this_section_text.append(word)
                                
                            except Exception as e:
                                # print(e)
                                this_section_text.append(word)
                        # print('break statement ran')
                        # print(section_title)
                        # input('continue ?')
                        # time.sleep(100)
                        all_sections.append({'title':section_title, 'section_id':int(current_section)-1, 'section_text':this_section_text, 'starting_page':starting_page, 'ending_page':ending_page})
                        # print("section added")
                        break
                # input('done?')

                
        except Exception as e:
            pass
    with open('main_sections.json','w')as file:
        json.dump(all_sections,file)
        print("extracted and saved all sections to 'main_sections.json'")
    # print(all_sections)


get_text()

import time
from PyPDF2 import PdfReader
import traceback
from decimal import Decimal
def is_float(string,current_subsection):
    try:
        next_subsection = round(current_subsection+0.1,2)
        if float(string) and next_subsection == float(string):  
            return True     
    except ValueError:
        return False  


def get_text():
    current_page = 0
    current_section = 0
    all_sections = []
    total_sections = []
    subsection_heading  = []
    current_subsection = 0
    reader = PdfReader('test.pdf')  

    all_text = ""

    for page in reader.pages:
        all_text += page.extract_text() + "\n"  

    

    list_array = all_text.replace('R1-1','').split()

    for i,word in enumerate(list_array):
        try:
            if word.isdigit(): #getting into the main sectino such as '1'
                if list_array[i+1] == 'USE':
                    print(word)
                    time.sleep(3)

                next_word = list_array[i+1]
                if next_word.isupper() and not next_word.startswith('R1-'): 
                    print(word)
                    section = ''
                    new_list = list_array[i+1:-1]
                    current_section +=1
                    current_subsection = 0
                    for word in new_list: #breaking down smaller sub sections of the main
                        if word.isupper():
                            section+=' '+word
                        else:
                            all_sections.append(section)
                            try:
                                if float(word) and '.' in word and round(float(current_section)+0.1,2) == float(word) and str(new_list[new_list.index(word)+1])[0].isupper() and float(word) != current_subsection:# 1.1
                                    # quit()
                                    current_subsection = float(word)
                                    print(f'current subsection = {current_subsection}')
                                    print('current word = ',word)
                                    current_index = new_list.index(word)
                                    next_word = new_list[current_index+1]
                                    print("next word = ",next_word)
                                    input('continue?')
                                    if not next_word[0].isupper():
                                        break
                                    subsection_heading.append(next_word)
                                        
                                elif  float(word) and '.' in word and round(float(current_subsection)+0.1,2) == float(word) and str(new_list[new_list.index(word)+1])[0].isupper():
                                    print(new_list[3:new_list.index(word)])
                                    input("Move ?")
                                    current_subsection = float(word)
                                    print('word = ',word)
                                    next_word = list_array[list_array.index(word)+1]
                                    if next_word[0].isupper():
                                        subsection_heading.append(next_word)
                                        print(subsection_heading)
                                
                                # elif  float(word) and '.' in word and round(float(current_subsection)+'0.0.1',2) == float(word) and str(new_list[new_list.index(word)+1])[0].isupper():
                                
                                
                            except Exception as e:
                                pass
            
                
        except Exception as e:
            print(f'Exception - {e}')
            traceback.print_exc()
            continue
get_text()

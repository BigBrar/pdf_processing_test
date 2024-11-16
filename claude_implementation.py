import pandas as pd
import re
from main import get_text

def extract_sections(text):
    # Initialize lists to store data
    data = []
    current_parent_section = ""
    current_section = ""
    current_title = ""
    current_body = ""
    current_page = None
    
    # Split text into lines
    lines = text.split('\n')
    
    # Regular expressions for matching patterns
    page_pattern = re.compile(r'Page (\d+)')
    section_pattern = re.compile(r'^(?![\s\d.]+$)(\d+(?:\.\d+)*)\s+(.+)$')
    
    for line in lines:
        # Check for page numbers
        page_match = page_pattern.search(line)
        if page_match:
            current_page = int(page_match.group(1))
            continue
            
        # Check for section headers
        section_match = section_pattern.match(line.strip())
        if section_match:
            # If we have accumulated content, save it
            if current_section:
                data.append({
                    'Parent section': current_parent_section,
                    'Section': current_section,
                    'Section Title': current_title,
                    'Section Body text': current_body.strip(),
                    'section-start page': current_page,
                    'section-end page': current_page
                })
            
            # Update current section information
            section_num = section_match.group(1)
            section_title = section_match.group(2)
            
            # Determine parent section
            parent_section = section_num.split('.')[0] if '.' in section_num else ""
            
            current_parent_section = parent_section
            current_section = section_num
            current_title = section_title
            current_body = ""
            
        else:
            # Accumulate body text
            if current_section and line.strip():
                current_body += line.strip() + " "
    
    # Add the last section
    if current_section:
        data.append({
            'Parent section': current_parent_section,
            'Section': current_section,
            'Section Title': current_title,
            'Section Body text': current_body.strip(),
            'section-start page': current_page,
            'section-end page': current_page
        })
    
    return data

def process_pdf_to_csv(pdf_text, output_csv):
    # Extract sections from PDF text
    sections_data = extract_sections(pdf_text)
    
    # Create DataFrame
    df = pd.DataFrame(sections_data)
    
    # Sort by section numbers
    df['sort_key'] = df['Section'].apply(lambda x: [int(n) for n in x.split('.')] if x else [0])
    df = df.sort_values(by='sort_key')
    df = df.drop('sort_key', axis=1)
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    return df

# Example usage
def main():
    # Your PDF text would come from a PDF parser
    sample_text = """
    Page 1
    1 INTENT AND OVERVIEW
    1.1 Intent
    The intent of this Residential Inclusive district schedule is to enable a variety of small-scale housing options...
    
    1.2 Overview
    The table below provides an overview of the outright and conditional approval uses...
    
    Page 2
    2 USE REGULATIONS
    2.1 Outright and Conditional Approval Uses
    All outright and conditional approval uses are subject to all other provisions...
    """
    
    # Process and save to CSV
    df = process_pdf_to_csv(get_text(), 'output.csv')
    print("CSV file has been created successfully.")
    return df

if __name__ == "__main__":
    main()

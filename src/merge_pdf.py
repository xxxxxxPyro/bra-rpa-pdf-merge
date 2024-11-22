import os
import yaml
import PyPDF2
import logging
import datetime

def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def load_folders(yaml_path):
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

def merge_pdf(folders, output_pdf):
    pdf_writer = PyPDF2.PdfWriter()
    pdf_count = 0

    for folder in folders:
        for foldername, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.endswith('.pdf'):
                    pdf_path = os.path.join(foldername, filename)
                    try:
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_reader = PyPDF2.PdfReader(pdf_file)
                            if len(pdf_reader.pages) == 0:
                                logging.warning(f'Warning: {pdf_path} is empty.')
                            else:
                                for page in range(len(pdf_reader.pages)):
                                    pdf_writer.add_page(pdf_reader.pages[page])
                                pdf_count += 1
                                logging.info(f'Successfully added {pdf_path} to the merge.')
                    except Exception as e:
                        logging.error(f'Error processing {pdf_path}: {e}')
    
    if pdf_count > 0:
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)
            logging.info(f'Merged {pdf_count} PDFs into {output_pdf}.')
    else:
        logging.warning('No PDFs were added to the merge. Output file will not be created.')

if __name__ == '__main__':
    logging.basicConfig(filename='./var/logs/processing_log.log', level=logging.INFO)
    folders = load_folders('./data/folders_path.yml')['folders']
    merge_pdf(folders, './var/cache/output_file/merged_output.pdf')
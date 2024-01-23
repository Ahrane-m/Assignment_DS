import json
import csv
from pathlib import Path
import pandas as pd


def token_list_to_string(token_list):
    sentence = ""
    for element in token_list:
        sentence = sentence + " " + element['token']
    return sentence


def append_data_set_headers(initial_list, temp_list):
    for item in temp_list:
        initial_list.append(item)

    return initial_list


def write_csv_file(field, data):
    with Path('./results/data_set.csv').open('w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(field)
        writer.writerows(data)


def extract_json_data():
    with open("files/dev.jsonl", "r", encoding="utf-8") as file:
        data_set_header_list = ['document_title', 'question_text', 'yes_no_answer']
        short_answer_header_list = list()
        data_set_data_list = list()
        for line in file:
            data = json.loads(line)
            document_tokens = data['document_tokens']
            data_annotation_list = start_byte = data['annotations']
            document_title = data['document_title']
            question_text = data['question_text']
            if len(data_annotation_list) > 0:
                short_answers_set = set()
                yes_no_answer = ''
                for i in data_annotation_list:
                    short_answers_data_list = i['short_answers']
                    if len(short_answers_data_list) > 0:
                        for e in short_answers_data_list:
                            start_token = e['start_token']
                            end_token = e['end_token']
                            start_token = int(start_token)
                            end_token = int(end_token)
                            short_answer_tokens = document_tokens[start_token:end_token]
                            short_answer = token_list_to_string(short_answer_tokens)
                            short_answers_set.add(short_answer.strip())
                            # print(f"Short answer is {short_answer}")
                    if i['yes_no_answer'] != 'NONE':
                        yes_no_answer = i['yes_no_answer']

                        # print(f"Short answers set {short_answers_set}")
                if yes_no_answer != '':
                    data = [document_title, question_text, yes_no_answer]
                    data_set_data_list.append(data)
                elif len(short_answers_set) > 0:
                    data = [document_title, question_text, 'NONE']
                    short_answers_list = list(short_answers_set)
                    for item in short_answers_list:
                        data.append(item)
                    if len(short_answer_header_list) < len(short_answers_list):
                        initial_index = len(short_answer_header_list)
                        index_different = len(short_answers_list) - len(short_answer_header_list)
                        for index in range(index_different):
                            short_answer_header_list.append(f"short_answer{index + initial_index + 1}")

                    data_set_data_list.append(data)
        updated_headers_list = append_data_set_headers(data_set_header_list, short_answer_header_list)
        write_csv_file(updated_headers_list, list(data_set_data_list))


def clean_data(data_frame):
    data_frame.fillna(value='UNKNOWN', inplace=True)
    data_frame.drop_duplicates(inplace=True)


def main():
    extract_json_data()

    # Read the CSV file into a DataFrame
    df = pd.read_csv('./results/data_set.csv')

    # Apply data cleaning strategies
    clean_data(df)

    # Save the cleaned DataFrame back to the CSV file
    df.to_csv('./results/cleaned_data_set.csv', index=False)


if __name__ == "__main__":
    main()

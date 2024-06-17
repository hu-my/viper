import json
import os
import csv

# create queries.csv file for GQA dataset

file_path = '/data/huminyang/dataset/ViperGPT-dataset/vGPT_data/gqa/questions'
output_path = '/data/huminyang/dataset/ViperGPT-dataset/vGPT_data/gqa/testdev'
if os.path.exists(output_path) is False:
    os.makedirs(output_path)

with open(os.path.join(file_path, 'testdev_balanced_questions.json'), 'r') as file:
    data = json.load(file)

with open(os.path.join(output_path, 'queries.csv'), 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['index', 'sample_id', 'possible_answers', 'query_type', 'query', 'answer', 'image_name'])
    index = 0
    for item in data.items():
        row_data = [str(index), '', item[1]['answer'], '', item[1]['question'], item[1]['answer'], item[1]['imageId'] + '.jpg']
        csvwriter.writerow(row_data)
        index += 1
print("Done!")
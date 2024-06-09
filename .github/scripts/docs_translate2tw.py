import os
import requests
import opencc

converter = opencc.OpenCC('s2twp.json')

token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')
pr_number = os.getenv('GITHUB_REF').split('/')[-1]

headers = {'Authorization': f'token {token}'}
url = f'https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files'
response = requests.get(url, headers=headers)
files = response.json()

translations = []
for file in files:
    if 'docs/' in file['filename'].lower():
        original_content = requests.get(file['raw_url'], headers=headers).text
        translated_content = converter.convert(original_content)
        translations.append(f'File: {file["filename"]}\nOriginal:\n{original_content}\n\nTranslated:\n{translated_content}\n')

with open('translation_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(translations))

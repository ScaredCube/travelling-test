import os
import opencc
from github import Github

converter = opencc.OpenCC('s2twp.json')
g = Github(os.getenv('GITHUB_TOKEN'))

repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
pr = repo.get_pull(int(os.getenv('GITHUB_REF').split('/')[-1]))

changed_files = pr.get_files()
docs_files = [f for f in changed_files]

translations = []
for file in docs_files:
    original_content = file.patch
    translated_content = converter.convert(original_content)
    translations.append(f'File: {file.filename}\nOriginal:\n{original_content}\n\nTranslated:\n{translated_content}\n')

with open('translation_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(translations))

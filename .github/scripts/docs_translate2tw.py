import os
import requests
import opencc
import json

# Initialize the OpenCC converter
converter = opencc.OpenCC('s2twp.json')

# Get the GitHub token and repository information from environment variables
# Get the GitHub token and repository information from environment variables
token = os.getenv('GITHUB_TOKEN')
repo_name = os.getenv('GITHUB_REPOSITORY')

# Read event data to get the PR number
with open(os.getenv('GITHUB_EVENT_PATH')) as f:
    event_data = json.load(f)
pr_number = event_data['number']

# Get the list of files changed in the pull request
headers = {'Authorization': f'token {token}'}
url = f'https://api.github.com/repos/ScaredCube/travelling-test/pulls/{pr_number}/files'
response = requests.get(url, headers=headers)

# Check for errors in the API response
if response.status_code != 200:
    print(f"Failed to fetch PR files: {response.status_code} {response.text} \nUrl: {url}")
    exit(1)

files = response.json()

# Filter docs, announcements, and blog files and translate their content
translations = []
directories_to_check = ['docs/', 'announcements/', 'blog/']
for file in files:
    if any(directory in file['filename'].lower() for directory in directories_to_check):
        raw_url = file['raw_url']
        original_content_response = requests.get(raw_url, headers=headers)
        original_content = original_content_response.text
        translated_content = converter.convert(original_content)
        translations.append(f'File: {file["filename"]}\nOriginal:\n{original_content}\n\nTranslated:\n{translated_content}\n')

# Write the translation suggestions to a file
with open('translation_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(translations))

with open('translation_output.txt', 'r', encoding='utf-8') as f:
    print(f.read())

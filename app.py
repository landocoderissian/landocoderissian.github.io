import os
import tempfile
import subprocess
import shutil
import requests
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

# Define global variables for GitHub repo
OWNER = 'Hopefullyidontgetbanned'
REPO = 'CharMorph_Docs'
HTML_DIR = 'docs'
EXISTING_CONF_PY = './docs/conf.py'  # Path to your existing conf.py

def fetch_repo_contents(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content.decode('utf-8')

def build_html(rst_files):
    # Ensure sphinx_rtd_theme is installed
    subprocess.run(['pip', 'install', 'sphinx_rtd_theme'], check=True)

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Write .rst files to the temporary directory with underscores instead of spaces
        for file_name, file_content in rst_files.items():
            sanitized_file_name = file_name.replace('_', ' ')
            file_path = os.path.join(temp_dir, sanitized_file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(file_content)

        # Copy the existing conf.py to the temporary directory
        shutil.copy(EXISTING_CONF_PY, temp_dir)

        # Ensure the output directory exists
        os.makedirs(HTML_DIR, exist_ok=True)

        # Run Sphinx
        source_dir = temp_dir
        build_dir = HTML_DIR
        sphinx_build_command = ['sphinx-build', '-b', 'html', source_dir, build_dir]
        subprocess.run(sphinx_build_command, check=True)

def process_repo_contents(contents, base_path):
    rst_files = {}
    for item in contents:
        if item['type'] == 'file' and item['name'].endswith('.rst'):
            print(f"Downloading {item['name']}...")
            rst_content = download_file(item['download_url'])
            rst_files[item['name']] = rst_content

        elif item['type'] == 'dir':
            new_base_path = os.path.join(base_path, item['name'])
            new_contents = fetch_repo_contents(OWNER, REPO, path=new_base_path)
            rst_files.update(process_repo_contents(new_contents, new_base_path))

    return rst_files

def update_docs():
    repo_contents = fetch_repo_contents(OWNER, REPO, '')
    rst_files = process_repo_contents(repo_contents, '')
    build_html(rst_files)

@app.route('/update_docs', methods=['POST'])
def update_docs_endpoint():
    try:
        update_docs()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/docs/<path:filename>')
def serve_html(filename):
    return send_from_directory(HTML_DIR, filename)

if __name__ == '__main__':
    update_docs()  # Initial update
    app.run(debug=True)

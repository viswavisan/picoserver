from miniserver import Server
import os

app = Server()

@app.get("/")
def home(data=None):
    context = {
        'title': 'My FastAPI App',
        'heading': 'Hello, World!',
        'message': 'Welcome to my FastAPI-like application!'}
    return app.template_response('index.html', context)

@app.get("/files")
def get_files(data=None):
    directory = '.'
    files_and_dirs = {'files': [], 'dirs': ['']}
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:dirs.remove('.git')
        for name in dirs:files_and_dirs['dirs'].append(os.path.relpath(os.path.join(root, name), directory))  # Add directories
        for name in files:files_and_dirs['files'].append(os.path.relpath(os.path.join(root, name), directory))  # Add files
    return files_and_dirs

@app.post("/upload")
def upload_file(data: dict):
    os.makedirs(data['directory'], exist_ok=True)
    content_bytes = bytearray(data['content'])
    with open(os.path.join(data['directory'], data['file_name']), 'wb') as f:f.write(content_bytes)
    return {'message': 'File uploaded successfully'}

@app.get("/download")
def download_file(data: dict):
    file_path = os.path.join(data['directory'], data['file_name'])
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:content = f.read()
        return {'file_name': data['file_name'], 'content': list(content)}  # Return file content as a list of bytes
    else:return {'error': 'File not found'}, 404

@app.delete("/delete")
def delete_file(data: dict):
    file_path = os.path.join(data['directory'], data['file_name'])
    if os.path.exists(file_path):
        os.remove(file_path)
        return {'message': 'File deleted successfully'}
    else:return {'error': 'File not found'}, 404

app.run()
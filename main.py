import hotspot
from miniserver import Server
import os
import machine
import gc
gc.mem_free()

led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()

app = Server()

@app.get("/")
def home(data=None):
    temp=27 - (machine.ADC(4).read_u16() * (3.3 / 65535.0)- 0.706) / 0.001721
    memory=f'{264-(gc.mem_free()// 1024)} KB/264 KB'
    context = {'temperature':temp,'memory':memory}
    return app.template_response('index.html', context)

@app.get("/files")
def get_files(data=None):
    directory = '.'
    files_and_dirs = {'files': os.listdir(), 'dirs': ['']}  
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
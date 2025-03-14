import inspect,requests,os, easygui

proxy_url='http://192.168.0.167/execute'
proxy_header={}

class proxy:
    def __init__(self):
        self.proxy_url='http://192.168.0.167/execute'
        self.proxy_header=''
    def convert_to_string(self,function):
        source = inspect.getsource(function)
        function_string='\n'.join(source.splitlines())+'\n'
        return function_string
    def proxy_run(self,cmd):     
        response=requests.post(self.proxy_url,headers=self.proxy_header,json={'cmd':cmd})
        try:result=response.json()
        except Exception:print(response.text);return {}
        return result

def upload_file():

    file='index.html'
    folder=''
    f=open(file,'rb')
    lines=f.readlines()
    filename=os.path.basename(file)
    path=folder+'/'+filename
    cmd=f"with open('{path}', 'wb') as f:f.writelines({lines})"
    response=requests.post(proxy_url,headers=proxy_header,json={'cmd':cmd})
    print(response.json())

def download_file(file):
    cmd=f"with open('{file}', 'rb') as f:return_value['lines']=f.read()"

    response=requests.post(proxy_url,headers=proxy_header,json={'cmd':cmd},verify=False)
    print(response.text)
    lines=response.json()
    print(lines)
    lines=lines['lines']
  
    print(lines)
    x=easygui.diropenbox()
    filename=os.path.basename(file)
    with open(x+'/'+filename,'w') as f:
        f.write(lines)
        f.close()

download_file('main.py')
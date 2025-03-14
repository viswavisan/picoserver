

        document.addEventListener('DOMContentLoaded', () => {
            fetchFiles();
            document.getElementById('upload-button').onclick = upload;
            document.getElementById('add-directory-button').onclick = addDirectory;
        });
        
        function fetchFiles() {
        console.log('1')
            fetch('/files')
                .then(response => response.json())
                .then(data => {
                console.log(data)
                    const fileList = document.getElementById('file-list');
                    const directorySelect = document.getElementById('directory');
                    fileList.innerHTML = '';
                    data.files.forEach(file => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            <span class="file-name">${file}</span>
                            <button onclick="downloadFile('${file}')">&#8681;</button>
                            <button onclick="deleteFile('${file}')">&#128465;</button>
                        `;
                        fileList.appendChild(li);
                    });
                    directorySelect.innerHTML = data.dirs.map(dir => `<option value="${dir}">${dir}</option>`).join('');
                })
                .catch(console.error);
        }
        

        function upload(event) {
            event.preventDefault();
            const fileInput = document.getElementById('file');
            const directorySelect = document.getElementById('directory');
            const file = fileInput.files[0];
            if (!file) return alert('Please select a file to upload.');

            const reader = new FileReader();
            reader.onload = function(event) {
                const data = {
                    file_name: file.name,
                    directory: directorySelect.value,
                    content: Array.from(new Uint8Array(event.target.result))
                };
                fetch('/upload', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    fetchFiles();
                })
                .catch(console.error);
            };
            reader.readAsArrayBuffer(file);
        }

        

        function downloadFile(fileName) {
            const selectedDirectory = document.getElementById('directory').value;
            fetch('/download', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_name: fileName, directory: selectedDirectory })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) return alert(data.error);
                const blob = new Blob([new Uint8Array(data.content)], { type: 'application/octet-stream' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url; a.download = data.file_name;
                document.body.appendChild(a); a.click(); document.body.removeChild(a);
            })
            .catch(console.error);
        }

        function deleteFile(fileName) {
            const selectedDirectory = document.getElementById('directory').value;
            fetch('/delete', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_name: fileName, directory: selectedDirectory })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message || data.error);
                fetchFiles();
            })
            .catch(console.error);
        }

        function addDirectory() {
            const newDirectoryName = document.getElementById('new-directory-name').value;
            if (!newDirectoryName) return alert('Please enter a directory name.');
            const option = document.createElement('option');
            option.value = newDirectoryName; option.textContent = newDirectoryName;
            document.getElementById('directory').appendChild(option);
            document.getElementById('new-directory-name').value = '';
        }

// select file input
const input = document.getElementById('upload');

// add event listener
input.addEventListener('change', () => {
    uploadFile(input.files[0]);
});


const uploadFile = (file) => {
    console.log(file.type);
    // check file type
    if(!['application/json'].includes(file.type)) {
        alert("Allowed file type is json. ");
    } else {
        // add file to FormData object
        const fd = new FormData();
        fd.append('json', file);

        // send `POST` request
        fetch('/api/upload/json/', {
            method: 'POST',
            body: fd
        })
        .then(res => res.json())
        .then(json => document.getElementById('controlTextarea').innerHTML = '<a href="' + json.message + '">click here to download generated csv.</a>')
        .catch(err => console.error(err));
    }
};


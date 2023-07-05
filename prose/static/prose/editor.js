// This code goes in /static/prose/editor.js or similar
function uploadAttachment(host, attachment) {
    uploadFile(host, attachment.file, setProgress, setAttributes);

    function setProgress(progress) {
        attachment.setUploadProgress(progress);
    }

    function setAttributes(attributes) {
        attachment.setAttributes(attributes);
    }
}

function uploadFile(host, file, progressCallback, successCallback) {
    var key = createStorageKey(file);
    var formData = createFormData(key, file);
    var xhr = new XMLHttpRequest();

    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    formData.append('csrfmiddlewaretoken', csrfToken);

    xhr.open("POST", host, true);

    xhr.upload.addEventListener("progress", function(event) {
        var progress = event.loaded / event.total * 100;
        progressCallback(progress);
    });

    xhr.addEventListener("load", function(event) {
        if (xhr.status == 201) {
            const data = JSON.parse(xhr.response);

            var attributes = {
                url: data.url,
                href: `${data.url}?content-disposition=attachment`
            };
            successCallback(attributes);
        }
    });

    xhr.send(formData);
}

function createStorageKey(file) {
    var date = new Date();
    var day = date.toISOString().slice(0,10);
    var name = date.getTime() + "-" + file.name;
    return [day, name].join("/");
}

function createFormData(key, file) {
    var data = new FormData();
    data.append("key", key);
    data.append("file", file);
    data.append("Content-Type", file.type);
    return data;
}

function initializeEditors() {
    const editors = document.querySelectorAll('.django-prose-editor:not(.initialized)');

    editors.forEach(editor => {
        editor.addEventListener("trix-attachment-add", function(event) {
            uploadAttachment(editor.dataset.uploadAttachmentUrl, event.attachment);
        });
        editor.classList.add('initialized');
    });
}

// When the DOM is initially loaded
document.addEventListener("DOMContentLoaded", initializeEditors);

// Export the initializeEditors function so it can be called from other scripts
window.initializeEditors = initializeEditors;

// Handle uploads

function uploadAttachment(host, attachment) {
  uploadFile(host, attachment, setProgress, setAttributes);

  function setProgress(progress) {
    attachment.setUploadProgress(progress);
  }

  function setAttributes(attributes) {
    attachment.setAttributes(attributes);
  }
}

document.addEventListener("DOMContentLoaded", function(event) {
  const editors = document.querySelectorAll('.django-prose-editor');

  editors.forEach(editor => {
    addEventListener("trix-attachment-add", function(event) {
      uploadAttachment(editor.dataset.uploadAttachmentUrl, event.attachment);
    });
  });
});

function uploadFile(host, attachment, progressCallback, successCallback) {
  var formData = createFormData(attachment.file);
  var xhr = new XMLHttpRequest();

  const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

  formData.append('csrfmiddlewaretoken', csrfToken);

  xhr.open("POST", host, true);

  xhr.upload.addEventListener("progress", function(event) {
    var progress = event.loaded / event.total * 100;
    progressCallback(progress);
  });

  xhr.addEventListener("load", function(event) {
    let data = {};
    switch (xhr.status) {
      case 201:
        data = JSON.parse(xhr.response);
        var attributes = {
          url: data.url,
          href: `${data.url}?content-disposition=attachment`
        };
        successCallback(attributes);
        break;
      case 400:
        data = JSON.parse(xhr.response);
        alert(data.error);
        attachment.remove();
        break;
      default:
        alert("The upload failed.");
        attachment.remove();
    }
  });

  xhr.send(formData);
}

function createFormData(file) {
  var data = new FormData();
  data.append("file", file);
  data.append("Content-Type", file.type);
  return data;
}

function uploadError(progressbar, textField, errorMsg) {
    textField.innerHTML += "<br>" + errorMsg.msg
    progressbar.style.width = "100%"
    progressbar.classList.add("bg-danger");
}

function removeFile(fileName) {
    console.log("updating")
    $.ajax({
        type: 'GET',
        url: 'removeFile.cgi?fileName=' + fileName,
        success: function (rawMsg) {
            if (rawMsg.status === "success") {
                console.log("success")
                console.log(rawMsg.msg)
                updateCurrentFiles()
            } else {
                console.error("remove failed")
                console.error(errorMsg.msg)
            }
        },
        fail: function (rawMsg) {
            console.log("failed")
            console.log(rawMsg)
        }
    });
}

function addCurrentFileListItem(name) {
    var listElement = document.createElement('li')
    var linkElement = document.createElement('a')
    var buttonElement = document.createElement('button')

    listElement.classList.add('list-group-item')
    listElement.classList.add('d-flex')
    listElement.classList.add('justify-content-between')
    listElement.classList.add('align-items-center')

    linkElement.classList.add('col-md-10')
    linkElement.href = "data/" + name
    linkElement.innerHTML = name

    buttonElement.classList.add('btn')
    buttonElement.classList.add('btn-danger')
    buttonElement.type = 'button'
    buttonElement.innerHTML = 'x'
    buttonElement.setAttribute('onClick', 'removeFile("' + name + '")')

    listElement.appendChild(linkElement)
    listElement.appendChild(buttonElement)

    document.getElementById("file-list").appendChild(listElement)
}

function updateCurrentFiles() {
    console.log("updating")
    $.ajax({
        type: 'GET',
        url: 'currentFiles.cgi',
        success: function (rawMsg) {
            if (rawMsg.status === "success") {
                console.log("success")
                console.log(rawMsg.msg)
                var result = rawMsg.msg.split("\n")
                console.log(result)
                document.getElementById("file-list").innerHTML = ""

                $.each(result, function(index, value){
                    if (value.length != 0) {
                        console.log(index +" "+ value)
                        addCurrentFileListItem(value)
                    }
                });
            } else {
                console.error("update failed")
                console.error(errorMsg.msg)
            }
        },
        fail: function (rawMsg) {
            console.log("failed")
            console.log(rawMsg)
        }
    });
}

function uploadFile(formData, fileName) {
    
    var progressbar = document.getElementById(fileName);
    var textField = document.getElementById('p'+fileName)

    console.log("uploading file" + fileName)
    
    $.ajax({
        type: 'POST',
        url: 'upload.cgi?fileName=' + fileName,
        data: formData,
        contentType: false,
        cache: false,
		
        processData: false,
        beforeSend: function () {
            progressbar.style.width = "50%"
        },
        success: function (rawMsg) {
            console.log(rawMsg)
            if (rawMsg.status === "success") {
                console.log("upload successful")
                console.log(rawMsg.msg)
                progressbar.style.width = "100%"
                progressbar.classList.add("bg-success");
                updateCurrentFiles()
            } else {
                console.error("upload failed")
                console.error(rawMsg.msg)
                uploadError(progressbar, textField, rawMsg)
            }
        },
        fail: function (rawMsg) {
            console.error("upload failed")
            console.error(rawMsg.msg)
            uploadError(progressbar, textField, rawMsg)
        }
    });
}

$(document).ready(function (e) {

    // Add Drop Effect "copy"
    $('#drop-zone').on('dragover', function (e) {
        e.stopPropagation();
        e.preventDefault();
        e.originalEvent.dataTransfer.dropEffect = 'copy';
    });

    // Handle on drop
    $('#drop-zone').on('drop', function(e){
        e.stopPropagation();
        e.preventDefault();
        // Get files
        var files = e.originalEvent.dataTransfer.files;

        //$('#list').html('<p>' + output.join('') + '</p>')
        $.each(files, function(index, value){
            console.log(index)
            console.log(value)
        });

        for (var i = 0, f; f = files[i]; i++) {
            var fileName = escape(f.name)
            $('#list').prepend('<div class="upload-item border border-light"><p id="p' + fileName + '">' + fileName + '</p> <div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%" id=' + fileName + ' aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div></div></div>')
            document.getElementById(escape(f.name)).style.width = "25%"
            var formData = new FormData()
            formData.append('singleFile', files[i])
			
            uploadFile(formData, fileName)
        }
   });

    updateCurrentFiles();
    
});

/*
function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    //dropZone.addEventListener('', handleFileSelect, false);
}
*/
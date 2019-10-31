// Get vars for buttons and forms and hide them by default
var buttonGrp = document.getElementById("btnGrp");
var submitButton = document.getElementById("submitAll");
var deleteButton = document.getElementById("deleteAll");
var imgForm = document.getElementById("imgForm");
var tagBtn = document.getElementById("addTag");
var tagTitle = document.getElementById("tagTitle")
//tagTitle.style.display = 'none';
//buttonGrp.style.display = 'none';
imgForm.style.display = 'none';

// This modifies the default dropzone options
Dropzone.options.drop = {
    autoProcessQueue: false,
    acceptedFiles: "image/*",
    paramName: "file",
    uploadMultiple: false,
    maxFiles: 1,
    init: function() {
        var myDropzone = this;

        // This triggers when a file is added to the dropzone
        this.on("addedfile", function(file) {

            // Show the buttons and forms
            buttonGrp.style.display = "block";
            imgForm.style.display = 'block';

            // If trying to add more than one, remove
            if (myDropzone.files.length > 1) {
                myDropzone.removeFile(file);
                alert("You may only upload one picture at a time")
            }
        });

        // This triggers when a file is removed. Checks to see if there are any files queued and hides the form/buttons accordingly
        this.on("removedfile", function() {
            if (myDropzone.files.length < 1) {
                //tagTitle.style.display = 'none';
                buttonGrp.style.display = 'none';
                imgForm.reset();
                imgForm.style.display = 'none';
            }
        });

        // Prevents default auto submit of dropzone. It instead processes when clicking on the button
        submitButton.addEventListener("click", function(e) {
			e.preventDefault();
            myDropzone.processQueue();
        });

		this.on("sending", function(file, xhr, formData) {
			console.log(file);
			var data = $("#imgForm").serializeArray();
			$.each(data, function(key, el) {
				formData.append(el.name, el.value);
			});
			console.log(formData);
		});

        // For the clear button
        deleteButton.addEventListener("click", function() {
            myDropzone.removeAllFiles(true);
            document.getElementById("tags").innerHTML = "";
        });

		// Commenting out for now - does not let us pass tags through the form doing it like this.
        //tagBtn.addEventListener("click", function() {
        //    var tag = document.getElementById("tag").value;
        //    document.getElementById("tag").value = "";

        //    if (tag != "") {
        //        tagTitle.style.display = 'block';
        //        document.getElementById("tags").innerHTML += '<li class="list-group-item list-group-item-dark">' + tag + '</li>'
        //    }

        //});

    }
};

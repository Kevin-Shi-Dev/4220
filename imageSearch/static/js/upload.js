// Get vars for buttons and forms and hide them by default
var buttonGrp = document.getElementById("btnGrp");
var submitButton = document.getElementById("submitAll");
var deleteButton = document.getElementById("deleteAll");
var imgForm = document.getElementById("imgForm");
var tagBtn = document.getElementById("addTag");
var tagTitle = document.getElementById("tagTitle");
var blocktagging = document.getElementById("blocktagging");
var checkboxtext = document.getElementById("copy");

//tagTitle.style.display = 'none';
//buttonGrp.style.display = 'none';
imgForm.style.display = 'none';
blocktagging.style.visibility = 'hidden';
buttonGrp.style.display = 'none';


const tagblockContainer = document.querySelector('.tagblock-container');
const input = document.querySelector('.tagblock-container input');

let tagblocks = [];



// This modifies the default dropzone options
Dropzone.options.drop = {
    autoProcessQueue: false,
    acceptedFiles: "image/*",
    paramName: "file",
    uploadMultiple: false,
    maxFiles: 10,
    init: function() {
        var myDropzone = this;

        // This triggers when a file is added to the dropzone
        this.on("addedfile", function(file) {

            // Show the buttons and forms
            buttonGrp.style.display = "block";
            imgForm.style.display = 'block';
            blocktagging.style.visibility = 'visible';

            // If trying to add more than one, remove
            if (myDropzone.files.length > 10) {
                myDropzone.removeFile(file);
                alert("You may only upload ten pictures at a time")
            }
        });

        // This triggers when a file is removed. Checks to see if there are any files queued and hides the form/buttons accordingly
        this.on("removedfile", function() {
            if (myDropzone.files.length < 1) {
                //tagTitle.style.display = 'none';
                buttonGrp.style.display = 'none';
                imgForm.reset();
                imgForm.style.display = 'none';
                blocktagging.style.visibility = 'hidden';

            }
        });

        // Prevents default auto submit of dropzone. It instead processes when clicking on the button
        submitButton.addEventListener("click", function(e) {
            if (checkboxtext.checked == true) {
                var i;
                var tmp = "";
                for (i = 0; i < tagblocks.length; i++) {
                    tmp = tmp + tagblocks[i];
                    if (i + 1 < tagblocks.length) {
                        tmp = tmp + ', '
                    }
                }
                console.log(tmp);
                document.getElementById("HTMLtags").value = tmp;
                checkboxtext.checked = false;

                e.preventDefault();
                myDropzone.processQueue();

                //myDropzone.removeAllFiles(true);
            }else {
                alert("You must agree to the Copyright")
            }

        });

		this.on("sending", function(file, xhr, formData) {
			console.log(file);
			var data = $("#imgForm").serializeArray();
			$.each(data, function(key, el) {
				formData.append(el.name, el.value);
			});
			console.log(formData);
		});
        this.on('success', function(file,responseText) {
            //console.log("test");
            //console.log(file);
            console.log(responseText);
            //window.location.href = '/media/'+responseText['id'];
             window.open('/media/'+responseText['id']);
             alert("Images Uploaded");
        });
        // For the clear button
        deleteButton.addEventListener("click", function() {
            myDropzone.removeAllFiles(true);
            document.getElementById("HTMLtags").innerHTML = "";
            tagblocks =[];
            addtagblocks();
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

function createtagblock(label) {
  const div = document.createElement('div');
  div.setAttribute('class', 'tagblock');
  const span = document.createElement('span');
  span.innerHTML = label;
  const closeIcon = document.createElement('i');
  closeIcon.innerHTML = '';
  closeIcon.setAttribute('class', 'material-icons');
  closeIcon.setAttribute('data-item', label);
  div.appendChild(span);
  div.appendChild(closeIcon);
  return div;
}

function cleartagblocks() {
  document.querySelectorAll('.tagblock').forEach(tagblock => {
    tagblock.parentElement.removeChild(tagblock);
  });
}

function addtagblocks() {
  cleartagblocks();
  tagblocks.slice().reverse().forEach(tagblock => {
    tagblockContainer.prepend(createtagblock(tagblock));
  });
}

input.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
      e.target.value.split(',').forEach(tagblock => {
        tagblocks.push(tagblock);
      });

      addtagblocks();
      input.value = '';
    }
});
document.addEventListener('click', (e) => {
  console.log(e.target.tagblockName);
  if (e.target.tagblockName === 'I') {
    const tagblockLabel = e.target.getAttribute('data-item');
    const index = tagblocks.indexOf(tagblockLabel);
    tagblocks = [...tagblocks.slice(0, index), ...tagblocks.slice(index+1)];
    addtagblocks();
  }
})

input.focus();

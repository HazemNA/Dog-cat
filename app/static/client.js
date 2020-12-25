var el = x => document.getElementById(x);

function showPicker() {
  el("file-input").click();
  el("extradata-label").innerHTML = `showPicker`;
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  el("extradata-label").innerHTML = `showPicked`;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
    el("result-label").innerHTML = `Click "Start Analysis" to figure our the breed`;
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  el("extradata-label").innerHTML = `Analyze`;
  var uploadFiles = el("file-input").files;
  // before size
  var beforesize = el("file-input").files[0].size;
  // next 2 lines will show the file size before resizing
  //alert("before size");
  //alert(beforesize);
  
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");
  
  el("analyze-button").innerHTML = "Analysis in Progress...";
  el("result-label").innerHTML = `  `;
  
  //el("extradata-label").innerHTML = `before resize`;
  // resize image
  //ResizeImage()
  //el("extradata-label").innerHTML = `after resize`;
  
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      var response = JSON.parse(e.target.responseText);
      el("result-label").innerHTML = `Breed is: ${response["result"]}`;
    }
    el("analyze-button").innerHTML = "Start Analysis";
  };

  var fileData = new FormData();
  // after size
  //var aftersize = uploadFiles[0].size;
  
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

// the next function to resize the image. incomplete?
function ResizeImage() {
    el("extradata-label").innerHTML = `ResizeImage`;
    // next 2 lines to take the uploaded filename
    var filesToUpload = el("file-input").files;
    var file = filesToUpload[0];
  
    // Original
    //var filesToUpload = document.getElementById('imageFile').files;
    //var file = filesToUpload[0];
  
    // Create an image
    var img = document.createElement("img");
    // Create a file reader
    var reader = new FileReader();
    // Set the image once loaded into file reader
    reader.onload = function(e) {
            img.src = e.target.result;

            var canvas = document.createElement("canvas");
            //var canvas = $("<canvas>", {"id":"testing"})[0];
            var ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0);

            // maximum size
            var MAX_WIDTH = 200;
            var MAX_HEIGHT = 200;
            var width = img.width;
            var height = img.height;

            if (width > height) {
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
            } else {
                if (height > MAX_HEIGHT) {
                    width *= MAX_HEIGHT / height;
                    height = MAX_HEIGHT;
                }
            }
            canvas.width = width;
            canvas.height = height;
            var ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            var dataurl = canvas.toDataURL("image/png");
            document.getElementById('output').src = dataurl;
        }
        // Load files into file reader
    reader.readAsDataURL(file);
}

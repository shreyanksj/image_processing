document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  var fileInput = document.getElementById('fileInput');
  var originalImage = document.getElementById('originalImage');
  var processedImage = document.getElementById('processedImage');
  
  var file = fileInput.files[0];
  var formData = new FormData();
  formData.append('file', file);

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Set original image
    originalImage.src = URL.createObjectURL(file);
    
    // Set processed image
    processedImage.src = `/uploads/${data.processed_image_path}`;


  })
  .catch(error => {
    console.error('Error:', error);
  });
});

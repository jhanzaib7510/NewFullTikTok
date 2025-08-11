// Change this if your backend runs somewhere else
const API_BASE = 'http://127.0.0.1:5000';

// Handle form submit with progress bar
document.getElementById('uploadForm').addEventListener('submit', (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('videoInput');
  if (fileInput.files.length === 0) {
    alert("Please select a video");
    return;
  }

  const formData = new FormData();
  formData.append('video', fileInput.files[0]);

  const xhr = new XMLHttpRequest();
  xhr.open('POST', `${API_BASE}/upload`, true);

  // Progress tracking
  xhr.upload.onprogress = (event) => {
    if (event.lengthComputable) {
      const percent = Math.round((event.loaded / event.total) * 100);
      document.getElementById('progressArea').style.display = 'block';
      document.getElementById('progressText').innerText = `Uploading... ${percent}%`;
      document.getElementById('progressBar').style.width = `${percent}%`;
    }
  };

  xhr.onload = () => {
    if (xhr.status === 200) {
      document.getElementById('status').innerText = '✅ Upload complete!';
      loadVideos();
    } else {
      const err = JSON.parse(xhr.responseText);
      document.getElementById('status').innerText = `❌ Error: ${err.error}`;
    }

    setTimeout(() => {
      document.getElementById('progressArea').style.display = 'none';
    }, 2000);
  };

  xhr.send(formData);
});

// Load videos from backend
async function loadVideos() {
  const res = await fetch(`${API_BASE}/videos`);
  const videos = await res.json();

  const videoFeed = document.getElementById('videoFeed');
  videoFeed.innerHTML = '';

  videos.forEach(filename => {
    const video = document.createElement('video');
    video.src = `${API_BASE}/uploads/${filename}`;
    video.controls = true;
    video.width = 300;
    videoFeed.appendChild(video);
  });
}

// Load videos on page load
loadVideos();

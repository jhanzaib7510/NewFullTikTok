// Change this if your backend runs somewhere else
const API_BASE = 'http://127.0.0.1:5000';

// Handle form submit
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('videoInput');
  if (fileInput.files.length === 0) {
    alert("Please select a video");
    return;
  }

  const formData = new FormData();
  formData.append('video', fileInput.files[0]);

  // Show progress bar
  document.getElementById('progressArea').style.display = 'block';
  document.getElementById('progressText').innerText = 'Uploading...';
  document.getElementById('progressBar').style.width = '0%';

  // Upload
  const res = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  });

  const data = await res.json();

  if (res.ok) {
    document.getElementById('status').innerText = '✅ Upload complete!';
    loadVideos();
  } else {
    document.getElementById('status').innerText = `❌ Error: ${data.error}`;
  }

  // Hide progress bar after 2s
  setTimeout(() => {
    document.getElementById('progressArea').style.display = 'none';
  }, 2000);
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

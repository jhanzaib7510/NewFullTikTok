const API_BASE = 'https://lively-bush-0d5f5f803.2.azurestaticapps.net/';

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('videoInput');
  const formData = new FormData();
  formData.append('video', fileInput.files[0]);

  await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData
  });

  loadVideos();
});

async function loadVideos() {
  const res = await fetch(`${API_BASE}/videos`);
  const videos = await res.json();

  const videoFeed = document.getElementById('videoFeed');
  videoFeed.innerHTML = '';
  videos.forEach(filename => {
    const video = document.createElement('video');
    video.src = `${API_BASE}/uploads/${filename}`;
    video.controls = true;
    videoFeed.appendChild(video);
  });
}

loadVideos();

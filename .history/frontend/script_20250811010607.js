// === CONFIGURE THIS ===
// https://ftiktok-f8f4fwfsbkcdgbd8.azurewebsites.net/uploads
const API_BASE = 'https://ftiktok-f8f4fwfsbkcdgbd8.azurewebsites.net'; // Update if needed

const uploadForm = document.getElementById('uploadForm');
const fileInput = document.getElementById('videoInput');
const statusEl = document.getElementById('status');
const videoFeed = document.getElementById('videoFeed');
const progressArea = document.getElementById('progressArea');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');

uploadForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Please select a video file first.');
    return;
  }
  const file = fileInput.files[0];
  const form = new FormData();
  form.append('video', file);

  statusEl.textContent = 'Uploading...';
  progressArea.style.display = 'block';
  progressBar.style.width = '0%';
  progressText.textContent = '';

  try {
    await new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('POST', API_BASE + '/upload', true);
      xhr.onload = () => (xhr.status >= 200 && xhr.status < 300) ? resolve(xhr.responseText) : reject(new Error(`Upload failed: ${xhr.status} ${xhr.statusText} – ${xhr.responseText}`));
      xhr.onerror = () => reject(new Error('Network error'));
      xhr.upload.onprogress = (evt) => {
        if (evt.lengthComputable) {
          const pct = Math.round((evt.loaded / evt.total) * 100);
          progressBar.style.width = pct + '%';
          progressText.textContent = `Uploaded ${pct}% (${Math.round(evt.loaded / 1024)} KB / ${Math.round(evt.total / 1024)} KB)`;
        }
      };
      xhr.send(form);
    });

    statusEl.textContent = 'Upload complete ✅';
    fileInput.value = '';
    await loadVideos();
  } catch (err) {
    console.error(err);
    statusEl.textContent = 'Upload error ❌';
    alert('Upload failed: ' + (err.message || err));
  } finally {
    setTimeout(() => {
      progressArea.style.display = 'none';
      progressBar.style.width = '0%';
      progressText.textContent = '';
    }, 1500);
  }
});

async function loadVideos() {
  try {
    const res = await fetch(API_BASE + '/videos');
    if (!res.ok) throw new Error(`Failed to list videos: ${res.status}`);
    const list = await res.json();
    videoFeed.innerHTML = '';
    if (!Array.isArray(list) || list.length === 0) {
      videoFeed.innerHTML = '<div class="small">No videos yet</div>';
      return;
    }
    list.forEach(name => {
      const wrap = document.createElement('div');
      wrap.style.width = '320px';
      wrap.style.display = 'flex';
      wrap.style.flexDirection = 'column';
      wrap.style.gap = '8px';

      const v = document.createElement('video');
      v.src = `${API_BASE}/uploads/${encodeURIComponent(name)}`;
      v.controls = true;
      v.width = 320;

      const info = document.createElement('div');
      info.className = 'small';
      info.textContent = name;

      wrap.appendChild(v);
      wrap.appendChild(info);
      videoFeed.appendChild(wrap);
    });
  } catch (err) {
    console.error(err);
    videoFeed.innerHTML = '<div class="small">Could not load videos. Check backend or CORS.</div>';
  }
}

window.addEventListener('load', loadVideos);

// const API_BASE = 'http://127.0.0.1:5000';

// document.getElementById('uploadForm').addEventListener('submit', async (e) => {
//   e.preventDefault();
//   const fileInput = document.getElementById('videoInput');
//   const formData = new FormData();
//   formData.append('video', fileInput.files[0]);

//   await fetch(`${API_BASE}/upload`, {
//     method: 'POST',
//     body: formData
//   });

//   loadVideos();
// });

// async function loadVideos() {
//   const res = await fetch(`${API_BASE}/videos`);
//   const videos = await res.json();

//   const videoFeed = document.getElementById('videoFeed');
//   videoFeed.innerHTML = '';
//   videos.forEach(filename => {
//     const video = document.createElement('video');
//     video.src = `${API_BASE}/uploads/${filename}`;
//     video.controls = true;
//     videoFeed.appendChild(video);
//   });
// }

// loadVideos();

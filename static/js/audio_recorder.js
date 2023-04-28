let mediaRecorder;
let recordedChunks = [];
const recordButton = document.getElementById('recordButton');

function sendAudioToServer(blob) {
  const formData = new FormData();
  formData.append('audio', blob, 'audio.webm'); 

  fetch('/process_audio', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const img = document.getElementById('generated-image');
        img.src = data.image_url;
      } else {
        console.error('Error processing audio:', data.error);
      }
    })
    .catch(err => {
      console.error('Error sending audio to server:', err);
    });
}

function startRecording() {
  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then((mediaStream) => {
      mediaRecorder = new MediaRecorder(mediaStream);
      mediaRecorder.start();

      mediaRecorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) {
          recordedChunks.push(event.data);
        }
      });
    })
    .catch(err => {
      console.error('Error getting user media:', err);
    });
}

function stopRecording() {
  mediaRecorder.stop();
  mediaRecorder.addEventListener('stop', () => {
    sendAudioToServer(new Blob(recordedChunks, { type: 'audio/mpeg' })); 
    recordedChunks = [];
  });
}


if (recordButton) {
  recordButton.addEventListener('click', () => {
    console.log(mediaRecorder?.state)
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      stopRecording();
      recordButton.textContent = 'Start Recording';
      recordButton.style.backgroundColor = 'red';
    } else {
      startRecording();
      recordButton.textContent = 'Stop Recording';
      recordButton.style.backgroundColor = 'green';
    }
  });
}

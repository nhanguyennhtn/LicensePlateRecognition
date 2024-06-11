import React, { useRef, useEffect, useState } from 'react';
import axios from 'axios';

const WebcamComponent = () => {
  const cameraUrl = "http://192.168.10.14:4747/video";
  const videoRef1 = useRef(null);
  const intervalRef1 = useRef(null);
  const [isProcessing1, setIsProcessing1] = useState(false);
  const [detections1, setDetections1] = useState([]);
  const [processedImage1, setProcessedImage1] = useState(null);

  const processFrame = async (imageData) => {
    setIsProcessing1(true);  // Indicate processing is starting
    try {
      console.log("Sending frame to server");
      const response = await axios.post('http://localhost:5000/upload-frame-external', { image: imageData });
      const result = response.data;
      console.log("Received response from server");
      setDetections1(result.detections);
      setProcessedImage1(result.image);
    } catch (error) {
      console.error('Error:', error);
    }
    setIsProcessing1(false);  // Indicate processing has finished
  };

  const captureFrame = (videoRef) => {
    const video = videoRef.current;
    if (!video) {
      console.log('Video element is not available');
      return null;
    }

    console.log(`Video dimensions: width=${video.videoWidth}, height=${video.videoHeight}`);

    if (!video.videoWidth || !video.videoHeight) {
      console.log('Video dimensions are not set');
      return null;
    }

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    return imageData;
  };

  useEffect(() => {
    const handleLoadedMetadata = () => {
      console.log('Video metadata loaded');
    };

    const handleLoadedData = () => {
      console.log('Video data loaded');
      const startSendingFrames = () => {
        intervalRef1.current = setInterval(() => {
          if (!isProcessing1 && videoRef1.current) {
            const frame = captureFrame(videoRef1);
            if (frame) {
              processFrame(frame);
            }
          }
        }, 5000);
      };

      startSendingFrames();
    };

    const videoElement = videoRef1.current;
    if (videoElement) {
      videoElement.addEventListener('loadedmetadata', handleLoadedMetadata);
      videoElement.addEventListener('loadeddata', handleLoadedData);
    }

    return () => {
      if (videoElement) {
        videoElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
        videoElement.removeEventListener('loadeddata', handleLoadedData);
      }
      clearInterval(intervalRef1.current);
    };
  }, [isProcessing1]);

  return (
    <div className="App">
      <div>
        <video
          title="DroidCam Stream"
          ref={videoRef1}
          style={{ border: 'none', width: '100%', height: '15em' }}
          onLoad={() => {
            const videoElement = videoRef1.current.contentWindow.document.querySelector('video');
            if (videoElement) {
              videoRef1.current = videoElement;
              console.log('Video element found inside iframe1111111111111111111111');
            }
          }}
        />
        <div>
          {detections1.map((detection, index) => (
            <div key={index}>
              <p>{`Label: ${detection.name}, Confidence: ${detection.confidence}`}</p>
            </div>
          ))}
        </div>
      </div>
      <div>
        {processedImage1 && (
          <img src={`data:image/jpeg;base64,${processedImage1}`} alt="Processed Frame" style={{ width: '100%', height: 'auto' }} />
        )}
      </div>
    </div>
  );
};

export default WebcamComponent;

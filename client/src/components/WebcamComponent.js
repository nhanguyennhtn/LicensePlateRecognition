import React, { useRef, useEffect, useState } from 'react';
import axios from 'axios';

const WebcamComponent = () => {
    const cameraUrl = "http://10.3.64.95:4747/video";
    const videoRef1 = useRef(null);
    const intervalRef1 = useRef(null);
    const [isProcessing1, setIsProcessing1] = useState(false);
    const [detections1, setDetections1] = useState([]);
    const [processedImage1, setProcessedImage1] = useState(null);

    const processFrame = async (imageData, setIsProcessing, setDetections, setProcessedImage, intervalRef) => {
        setIsProcessing(true);
        try {
            const response = await axios.post('http://localhost:5000/api/webcam-model', {
                image: imageData,
            });
            const result = response.data;
            setDetections(result.detections);
            setProcessedImage(result.image);
            if (result.detections.length > 0) {
                clearInterval(intervalRef.current);
            }
        } catch (error) {
            console.error('Error:', error);
        }
        setIsProcessing(false);
    };

    const captureFrame = (videoRef) => {
        const canvas = document.createElement('canvas');
        const video = videoRef.current;
        if (!video || !video.videoWidth || !video.videoHeight) return null;

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = canvas.toDataURL('image/jpeg');
        return imageData;
    };

    useEffect(() => {
        intervalRef1.current = setInterval(() => {
            if (!isProcessing1 && videoRef1.current) {
                const frame = captureFrame(videoRef1);
                if (frame) {
                    processFrame(frame, setIsProcessing1, setDetections1, setProcessedImage1, intervalRef1);
                }
            }
        }, 1000);

        return () => {
            clearInterval(intervalRef1.current);
        };
    }, [isProcessing1]);
    console.log(processedImage1);
    return (
        <div className="App">
            <div style={{ display: 'flex', justifyContent: 'space-around' }}>
                <div>
                    <img ref={videoRef1} src={cameraUrl} alt="IP Camera Stream" style={{ width: '100%', height: 'auto' }}/>
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
        </div>
    );
};

export default WebcamComponent;

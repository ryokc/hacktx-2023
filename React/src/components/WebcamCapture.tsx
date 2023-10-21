import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

function WebcamCapture() {
  const webcamRef = useRef<Webcam | null>(null);
  const [capturedImageSrc, setCapturedImageSrc] = useState<string | null>(null);

  const capture = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setCapturedImageSrc(imageSrc);
    }
  };

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <button onClick={capture}>Capture Photo</button>
      {capturedImageSrc && (
        <div>
          <img src={capturedImageSrc} alt="Captured" />
        </div>
      )}
    </div>
  );
}

export default WebcamCapture;

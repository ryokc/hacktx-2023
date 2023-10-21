import React, { useRef } from 'react';
import Webcam from 'react-webcam';

function WebcamCapture() {
  const webcamRef = useRef<Webcam | null>(null);

  const capture = () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    // Do something with the captured image source, e.g., send it to the server or display it.
  };

  return (
    <div>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
      />
      <button onClick={capture}>Capture Photo</button>
    </div>
  );
}

export default WebcamCapture;

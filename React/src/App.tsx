import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

function App() {
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
    <Webcam className = "Cam"
      audio={false}
      ref={webcamRef}
      screenshotFormat="image/jpeg"
    />
    <button className = "Capture" onClick={capture}>Capture Photo</button>
    {capturedImageSrc && (
    <img src={capturedImageSrc} alt="Captured"/>
    )}
  </div>
  );
}

export default App;

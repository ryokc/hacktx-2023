import React, { useRef } from 'react';
import Webcam from 'react-webcam';

function WebcamCapture() {
  const webcamRef = useRef<Webcam | null>(null);

  const capture = () => {
    // Use the `getScreenshot` method to capture the picture.
    const imageSrc = webcamRef.current?.getScreenshot();

    // You can now work with the captured image source, such as displaying it or sending it to the server.
    if (imageSrc) {
      // Example: Display the captured image in an <img> element.
      const imgElement = document.createElement('img');
      imgElement.src = imageSrc;
      document.body.appendChild(imgElement);
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

    </div>
  );
}

export default WebcamCapture;

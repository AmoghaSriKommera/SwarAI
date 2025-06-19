import React, { useState, useEffect, useRef } from 'react';
import { FaMicrophone, FaStop } from 'react-icons/fa';
import MicRecorder from 'mic-recorder-to-mp3';

interface RecorderProps {
  isRecording: boolean;
  onRecordingChange: (isRecording: boolean) => void;
  onTranscription: (text: string) => void;
}

// Create recorder instance outside component to persist between renders
const recorder = new MicRecorder({ bitRate: 128 });

function Recorder({
  isRecording,
  onRecordingChange,
  onTranscription
}: RecorderProps) {
  // State for permission status
  const [hasPermission, setHasPermission] = useState<boolean>(false);
  // State for recording duration
  const [duration, setDuration] = useState<number>(0);
  // Reference for recording timer
  const timerRef = useRef<number | null>(null);
  // Reference for audio blob
  const audioRef = useRef<Blob | null>(null);

  // Request microphone permission on mount
  useEffect(() => {
    const requestMicrophonePermission = async () => {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
        setHasPermission(true);
      } catch (error) {
        console.error('Microphone permission denied:', error);
        setHasPermission(false);
      }
    };

    requestMicrophonePermission();

    // Clean up timer on unmount
    return () => {
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
      }
    };
  }, []);

  // Update timer when recording state changes
  useEffect(() => {
    // Send audio to backend for transcription
    const sendAudioForTranscription = async (audioBlob: Blob) => {
      try {
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.mp3');
        
        // Set up progress indicator
        const startTime = Date.now();
        
        try {
          // Send to backend transcription endpoint
          const response = await fetch('http://localhost:8000/transcribe', {
            method: 'POST',
            body: formData,
          });
          
          if (!response.ok) {
            throw new Error(`Transcription failed: ${response.status}`);
          }
          
          const result = await response.json();
          console.log('Transcription completed in', Date.now() - startTime, 'ms');
          console.log('Transcription result:', result);
          
          onTranscription(result.text);
        } catch (fetchError) {
          console.error('Backend transcription failed:', fetchError);
          console.log('Falling back to mock transcription for development');
          
          // For development only: provide mock transcription if backend fails
          const mockTranscription = "This is a simulated fallback transcription. In production, this would come from the Whisper API via the backend.";
          onTranscription(mockTranscription);
        }
      } catch (error) {
        console.error('Transcription error:', error);
        onTranscription("Sorry, I couldn't transcribe your speech. Please try again.");
      }
    };

    if (isRecording) {
      // Start timer
      setDuration(0);
      timerRef.current = window.setInterval(() => {
        setDuration(prev => prev + 1);
      }, 1000);

      // Start recording
      recorder
        .start()
        .then(() => {
          console.log('Recording started');
        })
        .catch((error: Error) => {
          console.error('Recording error:', error);
          onRecordingChange(false);
        });
    } else {
      // Stop timer
      if (timerRef.current) {
        window.clearInterval(timerRef.current);
        timerRef.current = null;
      }

      // Stop recording if it was active
      if (duration > 0) {
        recorder
          .stop()
          .getMp3()
          .then(([buffer, blob]: [Buffer, Blob]) => {
            audioRef.current = blob;
            
            // Send audio to backend for transcription
            sendAudioForTranscription(blob);
          })
          .catch((error: Error) => {
            console.error('Error stopping recording:', error);
          });
      }
    }
  }, [isRecording, duration, onRecordingChange, onTranscription]);

  // Format seconds to MM:SS
  const formatTime = (seconds: number): string => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };



  // Toggle recording state
  const toggleRecording = () => {
    if (!hasPermission) {
      // Request permission again if not granted
      navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then(() => {
          setHasPermission(true);
          onRecordingChange(!isRecording);
        })
        .catch(error => {
          console.error('Microphone permission denied:', error);
          setHasPermission(false);
        });
    } else {
      onRecordingChange(!isRecording);
    }
  };

  return (
    <div className="recorder-container flex items-center justify-between">
      <div className="flex-1">
        {isRecording ? (
          <div className="recording-status text-red-500 font-medium flex items-center">
            <div className="recording-pulse mr-2 h-3 w-3 bg-red-500 rounded-full"></div>
            Recording... {formatTime(duration)}
          </div>
        ) : (
          <div className="recorder-prompt text-gray-500">
            {hasPermission 
              ? "Press the microphone button and start speaking" 
              : "Microphone access is required for voice input"}
          </div>
        )}
      </div>
      
      <button
        onClick={toggleRecording}
        className={`record-button p-3 rounded-full ml-4 flex items-center justify-center ${
          isRecording 
            ? 'bg-red-500 hover:bg-red-600' 
            : 'bg-primary hover:bg-primary-dark'
        } text-white transition-colors`}
        aria-label={isRecording ? 'Stop recording' : 'Start recording'}
      >
        {isRecording ? (
          <FaStop className="h-6 w-6" />
        ) : (
          <FaMicrophone className="h-6 w-6" />
        )}
      </button>
    </div>
  );
};

export default Recorder;
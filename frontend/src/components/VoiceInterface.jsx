import React, { useState, useEffect, useRef } from 'react';

function VoiceInterface({ isActive, isConnected, onStart, onStop, onMessage }) {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [statusMessage, setStatusMessage] = useState('Ready to start!');
    const [recognition, setRecognition] = useState(null);
    const [isSupported, setIsSupported] = useState(true);

    useEffect(() => {
        // Check if Web Speech API is supported
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            setIsSupported(false);
            setStatusMessage('Speech recognition not supported in this browser');
            return;
        }

        // Initialize speech recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognitionInstance = new SpeechRecognition();

        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        recognitionInstance.lang = 'en-US';
        recognitionInstance.maxAlternatives = 1;

        recognitionInstance.onstart = () => {
            setIsListening(true);
            setStatusMessage('🎤 Listening... Speak now!');
        };

        recognitionInstance.onresult = (event) => {
            const speechResult = event.results[0][0].transcript;
            setTranscript(speechResult);
            onMessage(speechResult);
            setStatusMessage(`You said: "${speechResult}"`);

            // Auto-restart listening if conversation is active
            setTimeout(() => {
                if (isActive && recognitionInstance) {
                    try {
                        recognitionInstance.start();
                    } catch (e) {
                        // Already started, ignore
                    }
                }
            }, 1000);
        };

        recognitionInstance.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            setIsListening(false);

            if (event.error === 'no-speech') {
                setStatusMessage('No speech detected. Try again!');
                // Auto-retry
                setTimeout(() => {
                    if (isActive) {
                        try {
                            recognitionInstance.start();
                        } catch (e) {
                            // Already started, ignore
                        }
                    }
                }, 1000);
            } else if (event.error === 'not-allowed') {
                setStatusMessage('❌ Microphone access denied');
            } else {
                setStatusMessage(`Error: ${event.error}`);
            }
        };

        recognitionInstance.onend = () => {
            setIsListening(false);
            if (isActive) {
                setStatusMessage('Ready to listen...');
            }
        };

        setRecognition(recognitionInstance);

        return () => {
            if (recognitionInstance) {
                recognitionInstance.stop();
            }
        };
    }, []);

    // Auto-start listening when conversation becomes active
    useEffect(() => {
        if (isActive && recognition && !isListening) {
            setTimeout(() => {
                try {
                    recognition.start();
                } catch (e) {
                    console.log('Recognition already started or error:', e);
                }
            }, 2000); // Give time for AI greeting to play
        } else if (!isActive && recognition && isListening) {
            recognition.stop();
            setStatusMessage('Conversation ended');
        }
    }, [isActive, recognition]);

    const handleStart = () => {
        if (!isConnected) {
            alert('Not connected to server. Please refresh the page.');
            return;
        }

        if (!isSupported) {
            alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
            return;
        }

        onStart();
    };

    const handleStop = () => {
        if (recognition) {
            recognition.stop();
        }
        onStop();
        setStatusMessage('Conversation stopped');
    };

    const handleManualListen = () => {
        if (recognition && !isListening) {
            try {
                recognition.start();
            } catch (e) {
                console.error('Error starting recognition:', e);
            }
        }
    };

    return (
        <div className="voice-interface">
            <div className="voice-status">
                {isListening && <div className="voice-indicator"></div>}
                <span>{statusMessage}</span>
            </div>

            <div className="voice-controls">
                {!isActive ? (
                    <button
                        className="voice-button primary"
                        onClick={handleStart}
                        disabled={!isConnected || !isSupported}
                    >
                        🎤 Start Talking
                    </button>
                ) : (
                    <>
                        <button
                            className={`voice-button primary ${isListening ? 'listening' : ''}`}
                            onClick={handleManualListen}
                            disabled={isListening}
                        >
                            {isListening ? '👂 Listening...' : '🎤 Speak'}
                        </button>
                        <button
                            className="voice-button danger"
                            onClick={handleStop}
                        >
                            ⏹️ Stop
                        </button>
                    </>
                )}
            </div>

            {!isSupported && (
                <div style={{
                    padding: '1rem',
                    background: 'rgba(239, 68, 68, 0.2)',
                    borderRadius: '8px',
                    color: '#fff',
                    textAlign: 'center',
                    fontSize: '0.9rem'
                }}>
                    ⚠️ Please use Chrome, Edge, or Safari for voice features
                </div>
            )}
        </div>
    );
}

export default VoiceInterface;

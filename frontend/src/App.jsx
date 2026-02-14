import React, { useState, useEffect, useRef } from 'react';
import ImageDisplay from './components/ImageDisplay';
import VoiceInterface from './components/VoiceInterface';
import ConversationDisplay from './components/ConversationDisplay';

const WS_URL = 'ws://localhost:8000/ws/conversation';
const API_URL = 'http://localhost:8000/api';
const SESSION_ID = `session_${Date.now()}`;

function App() {
    const [ws, setWs] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [conversationActive, setConversationActive] = useState(false);
    const [messages, setMessages] = useState([]);
    const [status, setStatus] = useState({ remaining_seconds: 60, is_active: false });
    const [imageContext, setImageContext] = useState('');
    const [toolNotification, setToolNotification] = useState(null);
    const [imageEffect, setImageEffect] = useState(null);

    // Initialize WebSocket connection
    useEffect(() => {
        connectWebSocket();
        loadImageContext();

        return () => {
            if (ws) {
                ws.close();
            }
        };
    }, []);

    const connectWebSocket = () => {
        const websocket = new WebSocket(`${WS_URL}/${SESSION_ID}`);

        websocket.onopen = () => {
            console.log('WebSocket connected');
            setIsConnected(true);
        };

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleWebSocketMessage(data);
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = () => {
            console.log('WebSocket closed');
            setIsConnected(false);
        };

        setWs(websocket);
    };

    const loadImageContext = async () => {
        try {
            const response = await fetch(`${API_URL}/image-context/sample_image.png`);
            const data = await response.json();
            if (data.success) {
                setImageContext(data.context);
            }
        } catch (error) {
            console.error('Error loading image context:', error);
            setImageContext('A beautiful, colorful image perfect for a fun conversation!');
        }
    };

    const handleWebSocketMessage = (data) => {
        console.log('Received:', data);

        if (data.type === 'message') {
            // Add message to conversation
            setMessages(prev => [...prev, {
                role: data.role,
                content: data.content,
                timestamp: new Date().toISOString()
            }]);

            // Update status
            if (data.status) {
                setStatus(data.status);
            }

            // Handle tool calls
            if (data.tool_calls && data.tool_calls.length > 0) {
                data.tool_calls.forEach(toolCall => {
                    handleToolCall(toolCall);
                });
            }

            // Speak the AI response
            if (data.role === 'assistant') {
                speakText(data.content);
            }
        } else if (data.type === 'status') {
            setStatus(data.status);
        } else if (data.type === 'end') {
            setConversationActive(false);
            setMessages(prev => [...prev, {
                role: 'system',
                content: data.message,
                timestamp: new Date().toISOString()
            }]);
            speakText(data.message);
        } else if (data.type === 'error') {
            alert(`Error: ${data.message}`);
        }
    };

    const handleToolCall = (toolCall) => {
        console.log('Tool call:', toolCall);

        switch (toolCall.name) {
            case 'highlight_area':
                setImageEffect('highlight');
                setTimeout(() => setImageEffect(null), 2000);
                break;

            case 'show_fun_fact':
                showNotification(`✨ Fun Fact!\n${toolCall.args.fact}`, 4000);
                break;

            case 'play_animation':
                const animationType = toolCall.args.animation_type || 'sparkles';
                setImageEffect(animationType);
                setTimeout(() => setImageEffect(null), 2000);
                break;

            case 'show_emoji':
                const emoji = toolCall.args.emoji || '😊';
                const size = toolCall.args.size || 'large';
                showNotification(emoji, 2000, size);
                break;

            default:
                console.log('Unknown tool:', toolCall.name);
        }
    };

    const showNotification = (content, duration = 3000, size = 'large') => {
        setToolNotification({ content, size });
        setTimeout(() => setToolNotification(null), duration);
    };

    const speakText = (text) => {
        if ('speechSynthesis' in window) {
            // Cancel any ongoing speech
            window.speechSynthesis.cancel();

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.9; // Slightly slower for children
            utterance.pitch = 1.1; // Slightly higher pitch (friendlier)
            utterance.volume = 1;

            // Try to use a friendly voice
            const voices = window.speechSynthesis.getVoices();
            const preferredVoice = voices.find(v =>
                v.name.includes('Google') || v.name.includes('Female') || v.name.includes('Samantha')
            );
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }

            window.speechSynthesis.speak(utterance);
        }
    };

    const startConversation = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'start',
                image_context: imageContext
            }));
            setConversationActive(true);
            setMessages([]);
        } else {
            alert('Not connected to server. Please refresh the page.');
        }
    };

    const sendMessage = (text) => {
        if (ws && ws.readyState === WebSocket.OPEN && text.trim()) {
            // Add user message immediately
            setMessages(prev => [...prev, {
                role: 'user',
                content: text,
                timestamp: new Date().toISOString()
            }]);

            // Send to backend
            ws.send(JSON.stringify({
                type: 'message',
                content: text
            }));
        }
    };

    const endConversation = () => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'end'
            }));
        }
        setConversationActive(false);
    };

    return (
        <div className="app-container">
            <header className="app-header">
                <h1 className="app-title">🤖 AI Voice Bot</h1>
                <p className="app-subtitle">Let's have a fun conversation!</p>
            </header>

            <main className="main-content">
                <ImageDisplay
                    imagePath="/sample_image.png"
                    effect={imageEffect}
                />

                <div className="conversation-section">
                    <div className="status-bar">
                        <div>
                            {conversationActive ? (
                                <span>🎙️ Active</span>
                            ) : (
                                <span>⏸️ Waiting</span>
                            )}
                        </div>
                        <div className={`timer ${status.remaining_seconds <= 10 && conversationActive ? 'warning' : ''}`}>
                            ⏱️ {status.remaining_seconds}s
                        </div>
                    </div>

                    <ConversationDisplay messages={messages} />

                    <VoiceInterface
                        isActive={conversationActive}
                        isConnected={isConnected}
                        onStart={startConversation}
                        onStop={endConversation}
                        onMessage={sendMessage}
                    />
                </div>
            </main>

            {toolNotification && (
                <div className="tool-notification">
                    <div className={`emoji-${toolNotification.size || 'large'}`}>
                        {toolNotification.content}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;

import React, { useEffect, useRef } from 'react';

function ConversationDisplay({ messages }) {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    return (
        <div className="conversation-display">
            {messages.length === 0 ? (
                <div style={{
                    textAlign: 'center',
                    color: '#718096',
                    fontStyle: 'italic',
                    padding: '2rem'
                }}>
                    Click "Start Talking" to begin the conversation! 🎤
                </div>
            ) : (
                messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <div className="message-role">{msg.role === 'user' ? 'You' : msg.role === 'assistant' ? 'AI' : 'System'}</div>
                        <div>{msg.content}</div>
                    </div>
                ))
            )}
            <div ref={messagesEndRef} />
        </div>
    );
}

export default ConversationDisplay;

import React, { useState, useEffect } from 'react';

function ImageDisplay({ imagePath, effect }) {
    const [hasEffect, setHasEffect] = useState(false);

    useEffect(() => {
        if (effect) {
            setHasEffect(true);
            const timer = setTimeout(() => setHasEffect(false), 2000);
            return () => clearTimeout(timer);
        }
    }, [effect]);

    return (
        <div className="image-section">
            <div className={`image-container ${hasEffect ? 'highlight' : ''}`}>
                <img
                    src={imagePath}
                    alt="Conversation topic"
                    onError={(e) => {
                        e.target.src = 'https://via.placeholder.com/800x600/667eea/ffffff?text=Sample+Image';
                    }}
                />
                {effect === 'sparkles' && <div className="sparkles"></div>}
            </div>
            <div style={{
                marginTop: '1rem',
                textAlign: 'center',
                color: '#2d3748',
                fontWeight: '600',
                fontSize: '1.1rem'
            }}>
                👀 Look at this picture and let's talk about it!
            </div>
        </div>
    );
}

export default ImageDisplay;

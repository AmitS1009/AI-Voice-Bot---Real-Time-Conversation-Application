"""
FastAPI Main Application - Real-Time AI Voice Bot
"""
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import json
from dotenv import load_dotenv
import base64

from gemini_client import GeminiClient
from conversation_manager import ConversationManager

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Voice Bot API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not set. Please set it in .env file")

gemini_client = GeminiClient(GOOGLE_API_KEY) if GOOGLE_API_KEY else None

# Store active conversations (in production, use Redis or similar)
active_conversations: Dict[str, ConversationManager] = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "AI Voice Bot API is running",
        "gemini_available": gemini_client is not None
    }

@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded image and return context for conversation
    """
    if not gemini_client:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Analyze image
        context = gemini_client.analyze_image(temp_path)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return {
            "success": True,
            "context": context,
            "filename": file.filename
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/image-context/{image_name}")
async def get_image_context(image_name: str):
    """
    Get context for a predefined image (e.g., sample image)
    """
    if not gemini_client:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    
    try:
        # Look for image in frontend public folder or backend folder
        possible_paths = [
            f"../frontend/public/{image_name}",
            f"../frontend/public/images/{image_name}",
            f"images/{image_name}",
            image_name
        ]
        
        image_path = None
        for path in possible_paths:
            if os.path.exists(path):
                image_path = path
                break
        
        if not image_path:
            raise HTTPException(status_code=404, detail=f"Image not found: {image_name}")
        
        # Analyze image
        context = gemini_client.analyze_image(image_path)
        
        return {
            "success": True,
            "context": context,
            "image_name": image_name
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.websocket("/ws/conversation/{session_id}")
async def conversation_websocket(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time conversation
    """
    await websocket.accept()
    
    if not gemini_client:
        await websocket.send_json({
            "type": "error",
            "message": "Gemini API not configured. Please set GOOGLE_API_KEY in .env"
        })
        await websocket.close()
        return
    
    # Create or get conversation manager
    if session_id not in active_conversations:
        conversation_duration = int(os.getenv("CONVERSATION_DURATION_SECONDS", "60"))
        active_conversations[session_id] = ConversationManager(conversation_duration)
    
    conversation = active_conversations[session_id]
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            message_type = message.get("type")
            
            if message_type == "start":
                # Start conversation with image context
                image_context = message.get("image_context", "")
                conversation.start_conversation(image_context)
                
                # Generate greeting
                greeting_response = gemini_client.generate_greeting(image_context)
                conversation.add_message("assistant", greeting_response["text"])
                
                # Send greeting to client
                await websocket.send_json({
                    "type": "message",
                    "role": "assistant",
                    "content": greeting_response["text"],
                    "tool_calls": greeting_response.get("tool_calls", []),
                    "status": conversation.get_status()
                })
                
            elif message_type == "message":
                # User message
                user_text = message.get("content", "")
                
                if not conversation.is_conversation_active():
                    await websocket.send_json({
                        "type": "end",
                        "message": "Conversation time is up! Thanks for chatting!",
                        "status": conversation.get_status()
                    })
                    continue
                
                # Add user message to history
                conversation.add_message("user", user_text)
                
                # Check if we should wrap up
                if conversation.should_wrap_up():
                    wrap_up_prompt = f"{user_text}\n\n[Note: This is the last exchange. Say a brief, friendly goodbye in 1 sentence.]"
                    response = gemini_client.generate_conversation_response(
                        wrap_up_prompt,
                        conversation.image_context,
                        conversation.conversation_history
                    )
                else:
                    # Generate response
                    response = gemini_client.generate_conversation_response(
                        user_text,
                        conversation.image_context,
                        conversation.conversation_history
                    )
                
                # Add AI response to history
                conversation.add_message("assistant", response["text"])
                
                # Send response to client
                await websocket.send_json({
                    "type": "message",
                    "role": "assistant",
                    "content": response["text"],
                    "tool_calls": response.get("tool_calls", []),
                    "status": conversation.get_status()
                })
                
                # Check if conversation should end
                if not conversation.is_conversation_active():
                    await websocket.send_json({
                        "type": "end",
                        "message": "Our chat time is up! That was so much fun!",
                        "status": conversation.get_status()
                    })
                    
            elif message_type == "status":
                # Send current status
                await websocket.send_json({
                    "type": "status",
                    "status": conversation.get_status()
                })
                
            elif message_type == "end":
                # End conversation manually
                conversation.end_conversation()
                await websocket.send_json({
                    "type": "end",
                    "message": "Goodbye! Thanks for the fun conversation!",
                    "status": conversation.get_status()
                })
                break
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session: {session_id}")
        if session_id in active_conversations:
            active_conversations[session_id].end_conversation()
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "message": f"An error occurred: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print(f"\n{'='*60}")
    print(f"🤖 AI Voice Bot API Starting...")
    print(f"{'='*60}")
    print(f"Server: http://{host}:{port}")
    print(f"API Docs: http://{host}:{port}/docs")
    print(f"Gemini API: {'✓ Configured' if GOOGLE_API_KEY else '✗ Not configured'}")
    print(f"{'='*60}\n")
    
    uvicorn.run(app, host=host, port=port)

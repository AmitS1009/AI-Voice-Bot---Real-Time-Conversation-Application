"""
Gemini API Client for image analysis and conversation
"""
import os
import base64
from typing import Dict, List, Any
import google.generativeai as genai
from PIL import Image
import io

class GeminiClient:
    def __init__(self, api_key: str):
        """Initialize Gemini client"""
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.0 Flash for conversation (supports vision and function calling)
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            tools=self._get_tools()
        )
        
    def _get_tools(self) -> List[Dict]:
        """Define tools that the AI can call during conversation"""
        return [
            {
                "function_declarations": [
                    {
                        "name": "highlight_area",
                        "description": "Highlight a specific area of the displayed image to draw attention to it",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "area": {
                                    "type": "string",
                                    "description": "Description of the area to highlight (e.g., 'top-left', 'center', 'bottom-right')"
                                },
                                "reason": {
                                    "type": "string",
                                    "description": "Why this area is being highlighted"
                                }
                            },
                            "required": ["area", "reason"]
                        }
                    },
                    {
                        "name": "show_fun_fact",
                        "description": "Display an interesting fun fact related to the conversation topic",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "fact": {
                                    "type": "string",
                                    "description": "The fun fact to display"
                                }
                            },
                            "required": ["fact"]
                        }
                    },
                    {
                        "name": "play_animation",
                        "description": "Trigger a visual animation to make the interaction more engaging",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "animation_type": {
                                    "type": "string",
                                    "enum": ["sparkles", "bounce", "pulse", "confetti"],
                                    "description": "Type of animation to play"
                                }
                            },
                            "required": ["animation_type"]
                        }
                    },
                    {
                        "name": "show_emoji",
                        "description": "Display an emoji that matches the conversation mood",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "emoji": {
                                    "type": "string",
                                    "description": "The emoji to display (e.g., '😊', '🎉', '🤔')"
                                },
                                "size": {
                                    "type": "string",
                                    "enum": ["small", "medium", "large"],
                                    "description": "Size of the emoji"
                                }
                            },
                            "required": ["emoji"]
                        }
                    }
                ]
            }
        ]
    
    def analyze_image(self, image_path: str) -> str:
        """Analyze an image and return a description suitable for child conversation"""
        try:
            # Load and prepare image
            img = Image.open(image_path)
            
            # Create a prompt for image analysis
            prompt = """
            You are talking to a young child (age 5-10). Look at this image and describe what you see.
            Focus on:
            - Main subjects (animals, people, objects)
            - Colors and interesting details
            - Things that would interest a child
            - Potential conversation starters
            
            Keep your description concise but engaging. This will help you have a fun 1-minute conversation
            with the child about this image.
            """
            
            # Generate content with image
            response = self.model.generate_content([prompt, img])
            return response.text
            
        except Exception as e:
            return f"I see an interesting picture! Let me tell you about it... (Error: {str(e)})"
    
    def generate_conversation_response(
        self, 
        user_message: str, 
        image_context: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate a conversation response with potential tool calls
        
        Returns:
            {
                "text": "AI response text",
                "tool_calls": [{"name": "tool_name", "args": {...}}]
            }
        """
        try:
            # Build conversation with context
            system_prompt = f"""
            You are a friendly AI talking to a young child (age 5-10) about an image they're looking at.
            
            IMAGE CONTEXT: {image_context}
            
            Guidelines:
            - Keep responses short (1-2 sentences max)
            - Use simple, child-friendly language
            - Ask engaging questions
            - Be enthusiastic and encouraging
            - Use tools to make the conversation interactive and fun
            - Call at least one tool during the conversation to create visual engagement
            
            This is a 1-minute conversation, so keep it dynamic and engaging!
            """
            
            # Build message history
            messages = [system_prompt]
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                messages.append(f"{role}: {content}")
            
            messages.append(f"user: {user_message}")
            
            # Generate response with function calling
            chat = self.model.start_chat(history=[])
            response = chat.send_message("\n".join(messages))
            
            # Extract text and tool calls
            result = {
                "text": response.text if response.text else "That's interesting! Tell me more!",
                "tool_calls": []
            }
            
            # Check for function calls
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            fc = part.function_call
                            result["tool_calls"].append({
                                "name": fc.name,
                                "args": dict(fc.args) if fc.args else {}
                            })
            
            return result
            
        except Exception as e:
            return {
                "text": f"Wow, that's so cool! What else do you notice?",
                "tool_calls": []
            }
    
    def generate_greeting(self, image_context: str) -> Dict[str, Any]:
        """Generate an opening greeting based on the image"""
        try:
            prompt = f"""
            You are starting a 1-minute fun conversation with a child about this image:
            
            {image_context}
            
            Create an enthusiastic, short greeting (1-2 sentences) that:
            - Welcomes the child
            - Mentions something interesting from the image
            - Asks an engaging opening question
            
            Also, call a fun tool to make it exciting!
            """
            
            chat = self.model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            result = {
                "text": response.text if response.text else "Hey! I love this picture! What do you see?",
                "tool_calls": []
            }
            
            # Check for function calls
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            fc = part.function_call
                            result["tool_calls"].append({
                                "name": fc.name,
                                "args": dict(fc.args) if fc.args else {}
                            })
            
            return result
            
        except Exception as e:
            return {
                "text": "Hi there! I can't wait to talk about this amazing picture with you! What catches your eye first?",
                "tool_calls": [{"name": "play_animation", "args": {"animation_type": "sparkles"}}]
            }

"""
Conversation Manager - Handles conversation state and timing
"""
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

class ConversationManager:
    def __init__(self, duration_seconds: int = 60):
        """Initialize conversation manager"""
        self.duration_seconds = duration_seconds
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.image_context: str = ""
        self.conversation_history: List[Dict[str, str]] = []
        self.is_active: bool = False
        
    def start_conversation(self, image_context: str) -> None:
        """Start a new conversation"""
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=self.duration_seconds)
        self.image_context = image_context
        self.conversation_history = []
        self.is_active = True
        
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_remaining_time(self) -> int:
        """Get remaining conversation time in seconds"""
        if not self.is_active or not self.end_time:
            return 0
        
        remaining = (self.end_time - datetime.now()).total_seconds()
        return max(0, int(remaining))
    
    def is_conversation_active(self) -> bool:
        """Check if conversation should still be active"""
        if not self.is_active:
            return False
            
        remaining = self.get_remaining_time()
        if remaining <= 0:
            self.is_active = False
            return False
            
        return True
    
    def should_wrap_up(self) -> bool:
        """Check if conversation should start wrapping up (last 10 seconds)"""
        remaining = self.get_remaining_time()
        return 0 < remaining <= 10
    
    def end_conversation(self) -> None:
        """End the conversation"""
        self.is_active = False
        
    def get_status(self) -> Dict[str, Any]:
        """Get current conversation status"""
        return {
            "is_active": self.is_active,
            "remaining_seconds": self.get_remaining_time(),
            "total_messages": len(self.conversation_history),
            "image_context": self.image_context,
            "should_wrap_up": self.should_wrap_up()
        }

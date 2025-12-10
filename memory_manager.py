#!/usr/bin/env python3
"""
Memory Manager - Handles persistent conversation history and context
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ConversationMessage:
    """A message in a conversation."""
    role: str  # 'system', 'user', 'assistant', 'agent'
    content: str
    agent_name: Optional[str] = None
    timestamp: str = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationMessage':
        """Create from dictionary."""
        return cls(**data)


class ConversationSession:
    """Represents a conversation session."""
    
    def __init__(self, session_id: str, title: str = "Untitled"):
        self.session_id = session_id
        self.title = title
        self.messages: List[ConversationMessage] = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at
        self.metadata = {}
    
    def add_message(self, message: ConversationMessage):
        """Add a message to the session."""
        self.messages.append(message)
        self.updated_at = datetime.now().isoformat()
    
    def get_messages(self, limit: Optional[int] = None) -> List[ConversationMessage]:
        """Get messages, optionally limited to most recent."""
        if limit:
            return self.messages[-limit:]
        return self.messages
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'session_id': self.session_id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata,
            'messages': [msg.to_dict() for msg in self.messages]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ConversationSession':
        """Create from dictionary."""
        session = cls(data['session_id'], data['title'])
        session.created_at = data['created_at']
        session.updated_at = data['updated_at']
        session.metadata = data.get('metadata', {})
        session.messages = [
            ConversationMessage.from_dict(msg) for msg in data.get('messages', [])
        ]
        return session


class MemoryManager:
    """Manages persistent conversation memory."""
    
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[ConversationSession] = None
        self.sessions_index: Dict[str, Dict] = {}
        self.load_index()
    
    def create_session(self, title: str = "New Conversation") -> ConversationSession:
        """Create a new conversation session."""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session = ConversationSession(session_id, title)
        self.current_session = session
        self._update_index(session)
        return session
    
    def load_session(self, session_id: str) -> Optional[ConversationSession]:
        """Load a session from disk."""
        session_path = self.storage_dir / f"{session_id}.json"
        if not session_path.exists():
            return None
        
        try:
            with open(session_path) as f:
                data = json.load(f)
                session = ConversationSession.from_dict(data)
                self.current_session = session
                return session
        except Exception:
            return None
    
    def save_session(self, session: Optional[ConversationSession] = None):
        """Save session to disk."""
        if session is None:
            session = self.current_session
        
        if session is None:
            return
        
        session_path = self.storage_dir / f"{session.session_id}.json"
        with open(session_path, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
        
        self._update_index(session)
    
    def list_sessions(self) -> List[Dict]:
        """List all available sessions."""
        return sorted(
            self.sessions_index.values(),
            key=lambda x: x['updated_at'],
            reverse=True
        )
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        session_path = self.storage_dir / f"{session_id}.json"
        if session_path.exists():
            session_path.unlink()
            if session_id in self.sessions_index:
                del self.sessions_index[session_id]
            self.save_index()
            return True
        return False
    
    def add_message(self, role: str, content: str, agent_name: Optional[str] = None):
        """Add a message to the current session."""
        if self.current_session is None:
            self.create_session()
        
        message = ConversationMessage(role, content, agent_name)
        self.current_session.add_message(message)
        self.save_session()
    
    def get_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation context."""
        if self.current_session is None:
            return []
        
        messages = self.current_session.get_messages(limit)
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'agent_name': msg.agent_name
            }
            for msg in messages
        ]
    
    def _update_index(self, session: ConversationSession):
        """Update sessions index."""
        self.sessions_index[session.session_id] = {
            'session_id': session.session_id,
            'title': session.title,
            'created_at': session.created_at,
            'updated_at': session.updated_at,
            'message_count': len(session.messages)
        }
        self.save_index()
    
    def save_index(self):
        """Save sessions index."""
        index_path = self.storage_dir / "index.json"
        with open(index_path, 'w') as f:
            json.dump(self.sessions_index, f, indent=2)
    
    def load_index(self):
        """Load sessions index."""
        index_path = self.storage_dir / "index.json"
        if index_path.exists():
            try:
                with open(index_path) as f:
                    self.sessions_index = json.load(f)
            except Exception:
                self.sessions_index = {}

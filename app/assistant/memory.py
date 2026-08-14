"""
Memory Management Module

Handles persistent storage of user information and assistant state.
Follows Single Responsibility Principle - only manages data persistence.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

from app.config import Config
from app.utils.logger import logger


class Memory:
    """
    Persistent memory storage for Jarvis AI.
    
    Handles saving and loading of user data, preferences, and
    any information that needs to persist across sessions.
    
    Attributes:
        memory_file: Path to the memory JSON file
        data: In-memory cache of all stored data
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure single memory instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize memory storage."""
        if not hasattr(self, 'initialized'):
            self.memory_file: Path = Config.MEMORY_FILE
            self.data: Dict[str, Any] = {}
            self._load()
            self.initialized = True
            logger.info("Memory system initialized")
    
    def _load(self) -> None:
        """Load memory data from file."""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.debug(f"Loaded {len(self.data)} memory items")
            else:
                self.data = {}
                self._save()
                logger.info("Created new memory file")
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted memory file: {e}")
            self.data = {}
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
            self.data = {}
    
    def _save(self) -> None:
        """Save memory data to file."""
        try:
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.debug("Memory saved successfully")
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def remember(self, key: str, value: Any) -> bool:
        """
        Store information in memory.
        
        Args:
            key: Identifier for the information
            value: Data to store (must be JSON serializable)
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.data[key.lower()] = {
                'value': value,
                'timestamp': datetime.now().isoformat(),
                'type': type(value).__name__
            }
            self._save()
            logger.info(f"Remembered: {key}")
            return True
        except Exception as e:
            logger.error(f"Failed to remember {key}: {e}")
            return False
    
    def recall(self, key: str) -> Optional[Any]:
        """
        Retrieve information from memory.
        
        Args:
            key: Identifier for the information
            
        Returns:
            Stored value or None if not found.
        """
        try:
            key = key.lower()
            if key in self.data:
                logger.debug(f"Recalled: {key}")
                return self.data[key]['value']
            return None
        except Exception as e:
            logger.error(f"Failed to recall {key}: {e}")
            return None
    
    def forget(self, key: str) -> bool:
        """
        Remove information from memory.
        
        Args:
            key: Identifier for the information
            
        Returns:
            True if successful, False otherwise.
        """
        try:
            key = key.lower()
            if key in self.data:
                del self.data[key]
                self._save()
                logger.info(f"Forgot: {key}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to forget {key}: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all stored memories.
        
        Returns:
            Dictionary of all memory items.
        """
        return self.data.copy()
    
    def clear(self) -> bool:
        """
        Clear all memory.
        
        Returns:
            True if successful, False otherwise.
        """
        try:
            self.data = {}
            self._save()
            logger.info("Memory cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear memory: {e}")
            return False
    
    def get_count(self) -> int:
        """
        Get number of stored memory items.
        
        Returns:
            Number of items in memory.
        """
        return len(self.data)
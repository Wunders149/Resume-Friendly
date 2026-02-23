"""
Logging utility for CV Forge
Simple logging system for debugging and error tracking
"""
import os
import logging
from datetime import datetime
from pathlib import Path


class Logger:
    """Simple logging utility for CV Forge"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize logger"""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging configuration"""
        # Create logs directory
        log_dir = Path.home() / ".cvforge" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        log_file = log_dir / f"cvforge_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configure logger
        self._logger = logging.getLogger('CVForge')
        self._logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler (only for errors)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        if self._logger:
            self._logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        if self._logger:
            self._logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        if self._logger:
            self._logger.warning(message)
    
    def error(self, message: str, exc_info: Exception = None):
        """Log error message"""
        if self._logger:
            self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: Exception = None):
        """Log critical message"""
        if self._logger:
            self._logger.critical(message, exc_info=exc_info)
    
    def get_log_file_path(self) -> str:
        """Get current log file path"""
        return str(Path.home() / ".cvforge" / "logs" / f"cvforge_{datetime.now().strftime('%Y%m%d')}.log")


# Convenience functions
def get_logger() -> Logger:
    """Get logger instance"""
    return Logger()


def log_debug(message: str):
    """Log debug message"""
    Logger().debug(message)


def log_info(message: str):
    """Log info message"""
    Logger().info(message)


def log_warning(message: str):
    """Log warning message"""
    Logger().warning(message)


def log_error(message: str, exc_info: Exception = None):
    """Log error message"""
    Logger().error(message, exc_info=exc_info)

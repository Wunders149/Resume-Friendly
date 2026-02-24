#!/usr/bin/env python3
"""
CV-Forge - ATS-Friendly Resume Generator
=========================================

A desktop application for creating ATS-compatible resumes.

Usage:
    python main.py
"""

import customtkinter as ctk
import sys
from pathlib import Path

# Add cv-forge directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.main_window import MainWindow


def main():
    """Launch the CV-Forge application."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()

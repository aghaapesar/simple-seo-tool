"""
File Selector Module

Interactive file selection for Excel input files with multi-select support.
"""

import os
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class FileSelector:
    """
    Interactive file selector for Excel input files.
    
    Features:
    - Automatic detection of Excel files in input directory
    - Multi-select support
    - File size and modification date display
    - User-friendly interactive interface
    """
    
    def __init__(self, input_dir: str = "input"):
        """
        Initialize FileSelector.
        
        Args:
            input_dir: Directory containing input Excel files
        """
        self.input_dir = Path(input_dir)
        self.input_dir.mkdir(exist_ok=True)
        logger.info(f"Input directory: {self.input_dir}")
    
    def _get_excel_files(self) -> List[Dict]:
        """
        Get list of Excel files in input directory with metadata.
        
        Returns:
            List of file info dictionaries
        """
        excel_extensions = ['.xlsx', '.xls']
        files_info = []
        
        for file_path in self.input_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in excel_extensions:
                # Get file metadata
                stat = file_path.stat()
                size_kb = stat.st_size / 1024
                
                # Format modification time
                from datetime import datetime
                mod_time = datetime.fromtimestamp(stat.st_mtime)
                
                files_info.append({
                    'path': file_path,
                    'name': file_path.name,
                    'size_kb': size_kb,
                    'modified': mod_time
                })
        
        # Sort by modification time (newest first)
        files_info.sort(key=lambda x: x['modified'], reverse=True)
        
        return files_info
    
    def _format_size(self, size_kb: float) -> str:
        """
        Format file size for display.
        
        Args:
            size_kb: File size in KB
            
        Returns:
            Formatted size string
        """
        if size_kb < 1024:
            return f"{size_kb:.1f} KB"
        else:
            return f"{size_kb/1024:.2f} MB"
    
    def _format_date(self, dt) -> str:
        """
        Format date for display.
        
        Args:
            dt: datetime object
            
        Returns:
            Formatted date string
        """
        return dt.strftime("%Y-%m-%d %H:%M")
    
    def select_files_interactive(self, custom_dir: str = None) -> List[Path]:
        """
        Interactive file selection interface.
        
        Args:
            custom_dir: Optional custom directory to search (overrides self.input_dir)
        
        Returns:
            List of selected file paths
        """
        # Use custom directory if provided
        if custom_dir:
            original_dir = self.input_dir
            self.input_dir = Path(custom_dir)
            self.input_dir.mkdir(exist_ok=True)
        
        # Get available files
        files = self._get_excel_files()
        
        # Restore original directory if custom was used
        if custom_dir:
            self.input_dir = original_dir
        
        if not files:
            print("\n" + "="*60)
            print("❌ NO EXCEL FILES FOUND")
            print("="*60)
            print(f"\nPlease copy your Google Search Console Excel files to:")
            print(f"  📁 {self.input_dir.absolute()}")
            print("\nThen run the program again.")
            print("="*60)
            return []
        
        # Display files
        print("\n" + "="*60)
        print(f"📊 FOUND {len(files)} EXCEL FILE(S)")
        print("="*60)
        
        for idx, file_info in enumerate(files, 1):
            size_str = self._format_size(file_info['size_kb'])
            date_str = self._format_date(file_info['modified'])
            
            print(f"  [{idx}] {file_info['name']}")
            print(f"      📏 {size_str:>10} | 📅 {date_str}")
        
        # Selection interface
        print("\n" + "-"*60)
        print("Selection options:")
        print("  - Enter numbers separated by commas (e.g., 1,3)")
        print("  - Enter 'all' to select all files")
        print("  - Enter 'finish' or 'exit' to quit")
        print("-"*60)
        
        selected_files = []
        
        while True:
            choice = input("\nYour selection: ").strip().lower()
            
            if choice in ['finish', 'exit', 'quit', 'q']:
                if selected_files:
                    print(f"\n✅ Selected {len(selected_files)} file(s)")
                    return selected_files
                else:
                    print("❌ No files selected. Exiting...")
                    return []
            
            if choice == 'all':
                selected_files = [f['path'] for f in files]
                print(f"✅ Selected all {len(selected_files)} file(s)")
                return selected_files
            
            # Parse comma-separated numbers
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                
                # Validate indices
                if all(1 <= idx <= len(files) for idx in indices):
                    selected_files = [files[idx-1]['path'] for idx in indices]
                    
                    print(f"\n✅ Selected {len(selected_files)} file(s):")
                    for path in selected_files:
                        print(f"   • {path.name}")
                    
                    # Ask if user wants to continue or finish
                    confirm = input("\nContinue selecting? (y/N): ").strip().lower()
                    if confirm not in ['y', 'yes']:
                        return selected_files
                else:
                    print(f"❌ Invalid selection. Numbers must be between 1 and {len(files)}")
            
            except ValueError:
                print("❌ Invalid format. Use comma-separated numbers, 'all', or 'finish'")
    
    def move_processed_files(self, files: List[Path], processed_dir: str = "processed"):
        """
        Move processed files to a separate directory.
        
        Args:
            files: List of file paths to move
            processed_dir: Destination directory name
        """
        dest_dir = self.input_dir / processed_dir
        dest_dir.mkdir(exist_ok=True)
        
        print(f"\n📦 Moving {len(files)} processed file(s) to {processed_dir}/...")
        
        for file_path in files:
            if file_path.exists():
                dest_path = dest_dir / file_path.name
                
                # Handle duplicate names
                counter = 1
                while dest_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                file_path.rename(dest_path)
                print(f"   ✅ {file_path.name} → {processed_dir}/")
        
        logger.info(f"Moved {len(files)} files to {dest_dir}")


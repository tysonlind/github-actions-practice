"""Core encoding functionality for the file encoder package."""

import os
from pathlib import Path
from typing import Optional


class FileEncoder:
    """A class for encoding files with various character encodings."""
    
    DEFAULT_ENCODING = "utf-8"
    SUPPORTED_ENCODINGS = [
        "utf-8", "utf-16", "utf-32", "ascii", "latin-1", "cp1252",
        "iso-8859-1", "windows-1252", "big5", "gb2312", "shift_jis"
    ]
    
    def __init__(self):
        """Initialize the FileEncoder."""
        pass
    
    def encode_file(self, input_path: str, output_path: Optional[str] = None, 
                   encoding: str = DEFAULT_ENCODING) -> str:
        """
        Encode a file with the specified encoding.
        
        Args:
            input_path: Path to the input file
            output_path: Path to the output file (optional, defaults to input_path with suffix)
            encoding: Target encoding (defaults to utf-8)
            
        Returns:
            Path to the encoded output file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If encoding is not supported
            UnicodeDecodeError: If file cannot be decoded
            UnicodeEncodeError: If file cannot be encoded
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if encoding not in self.SUPPORTED_ENCODINGS:
            raise ValueError(f"Unsupported encoding: {encoding}. "
                           f"Supported encodings: {', '.join(self.SUPPORTED_ENCODINGS)}")
        
        # Generate output path if not provided
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(input_file.parent / f"{input_file.stem}_{encoding}{input_file.suffix}")
        
        # Read the file with automatic encoding detection
        content = self._read_file_with_fallback(input_path)
        
        # Write the file with the target encoding
        with open(output_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return output_path
    
    def _read_file_with_fallback(self, file_path: str) -> str:
        """
        Read a file with automatic encoding detection using fallback encodings.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Content of the file as a string
            
        Raises:
            UnicodeDecodeError: If file cannot be decoded with any encoding
        """
        # Common encodings to try in order
        # Note: utf-16 variants to handle BOM issues
        encodings_to_try = ['utf-8', 'utf-16-le', 'utf-16-be', 'utf-16', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    # Remove BOM character if present (common in UTF-16 and UTF-8 files)
                    if content.startswith('\ufeff'):
                        content = content[1:]
                    return content
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        # If all encodings fail, raise an error
        raise UnicodeDecodeError(
            "unknown", b"", 0, 1,
            "Could not decode file with any of the attempted encodings: " + 
            ", ".join(encodings_to_try)
        )
    
    def get_file_encoding(self, file_path: str) -> str:
        """
        Detect the encoding of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Detected encoding name
        """
        encodings_to_try = ['utf-8', 'utf-16-le', 'utf-16-be', 'utf-16', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    f.read()
                return encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        return "unknown"

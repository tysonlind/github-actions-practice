"""Tests for the FileEncoder class."""

import os
import tempfile
import pytest

from file_encoder.encoder import FileEncoder


class TestFileEncoder:
    """Test cases for the FileEncoder class."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.encoder = FileEncoder()
        self.test_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up after each test method."""
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_file(self, content: str, filename: str = "test.txt", 
                        encoding: str = "utf-8") -> str:
        """Create a test file with the given content and encoding."""
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return file_path
    
    def test_encode_file_default_encoding(self):
        """Test encoding a file with default encoding (utf-8)."""
        content = "Hello, World! 🌍"
        input_file = self.create_test_file(content)
        
        output_file = self.encoder.encode_file(input_file)
        
        # Check that output file exists
        assert os.path.exists(output_file)
        
        # Check that content is preserved
        with open(output_file, 'r', encoding='utf-8') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_encode_file_custom_encoding(self):
        """Test encoding a file with a custom encoding."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        output_file = self.encoder.encode_file(input_file, encoding="ascii")
        
        # Check that output file exists
        assert os.path.exists(output_file)
        
        # Check that content is preserved
        with open(output_file, 'r', encoding='ascii') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_encode_file_custom_output_path(self):
        """Test encoding a file with a custom output path."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        output_path = os.path.join(self.test_dir, "custom_output.txt")
        
        result_path = self.encoder.encode_file(input_file, output_path=output_path)
        
        assert result_path == output_path
        assert os.path.exists(output_path)
        
        # Check content
        with open(output_path, 'r', encoding='utf-8') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_encode_file_nonexistent_file(self):
        """Test encoding a file that doesn't exist."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.txt")
        
        with pytest.raises(FileNotFoundError):
            self.encoder.encode_file(nonexistent_file)
    
    def test_encode_file_unsupported_encoding(self):
        """Test encoding with an unsupported encoding."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        with pytest.raises(ValueError) as exc_info:
            self.encoder.encode_file(input_file, encoding="unsupported-encoding")
        
        assert "Unsupported encoding" in str(exc_info.value)
    
    def test_encode_file_unicode_content(self):
        """Test encoding a file with Unicode content."""
        content = "Hello, 世界! 🌍 Café naïve résumé"
        input_file = self.create_test_file(content)
        
        output_file = self.encoder.encode_file(input_file, encoding="utf-8")
        
        # Check that content is preserved
        with open(output_file, 'r', encoding='utf-8') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_encode_file_latin1_encoding(self):
        """Test encoding to latin-1 encoding."""
        content = "Hello, World! Café"
        input_file = self.create_test_file(content)
        
        output_file = self.encoder.encode_file(input_file, encoding="latin-1")
        
        # Check that content is preserved
        with open(output_file, 'r', encoding='latin-1') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_get_file_encoding(self):
        """Test detecting file encoding."""
        content = "Hello, World!"
        
        # Test UTF-8 file
        utf8_file = self.create_test_file(content, "utf8.txt", "utf-8")
        detected_encoding = self.encoder.get_file_encoding(utf8_file)
        assert detected_encoding in ["utf-8", "ascii"]  # ASCII is subset of UTF-8
        
        # Test ASCII file
        ascii_content = "Hello World"
        ascii_file = self.create_test_file(ascii_content, "ascii.txt", "ascii")
        detected_encoding = self.encoder.get_file_encoding(ascii_file)
        assert detected_encoding in ["utf-8", "ascii"]
    
    def test_supported_encodings_list(self):
        """Test that the supported encodings list is not empty."""
        assert len(FileEncoder.SUPPORTED_ENCODINGS) > 0
        assert "utf-8" in FileEncoder.SUPPORTED_ENCODINGS
        assert "ascii" in FileEncoder.SUPPORTED_ENCODINGS
    
    def test_default_encoding(self):
        """Test that the default encoding is utf-8."""
        assert FileEncoder.DEFAULT_ENCODING == "utf-8"
    
    def test_read_file_with_fallback_success(self):
        """Test reading a file with encoding fallback."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        result_content = self.encoder._read_file_with_fallback(input_file)
        assert result_content == content
    
    def test_output_filename_generation(self):
        """Test that output filenames are generated correctly."""
        content = "Hello, World!"
        input_file = self.create_test_file(content, "input.txt")
        
        output_file = self.encoder.encode_file(input_file, encoding="ascii")
        
        # Should contain the encoding in the filename
        assert "ascii" in os.path.basename(output_file)
        assert output_file.endswith(".txt")

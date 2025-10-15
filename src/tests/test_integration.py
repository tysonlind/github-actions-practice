"""Integration tests for the file encoder package."""

import os
import tempfile

from file_encoder import FileEncoder
from file_encoder.cli import main
from click.testing import CliRunner


class TestIntegration:
    """Integration tests for the complete file encoder functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.encoder = FileEncoder()
        self.runner = CliRunner()
        self.test_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up after each test method."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_file(self, content: str, filename: str = "test.txt", 
                        encoding: str = "utf-8") -> str:
        """Create a test file with the given content and encoding."""
        file_path = os.path.join(self.test_dir, filename)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return file_path
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from CLI to file encoding."""
        # Create a test file with mixed content
        content = "Hello, World! 🌍\nThis is a test file.\nWith multiple lines."
        input_file = self.create_test_file(content, "input.txt")
        
        # Use CLI to encode the file
        result = self.runner.invoke(main, [
            input_file, 
            '--encoding', 'utf-16',
            '--verbose'
        ])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output
        
        # Extract output filename from CLI output
        output_line = [line for line in result.output.split('\n') 
                      if line.startswith('File encoded successfully:')][0]
        output_file = output_line.split(': ', 1)[1]
        
        # Verify the output file exists and has correct content
        assert os.path.exists(output_file)
        with open(output_file, 'r', encoding='utf-16') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_multiple_encoding_conversions(self):
        """Test converting a file through multiple encodings."""
        original_content = "Hello, World! Café naïve"
        
        # Create original file
        original_file = self.create_test_file(original_content, "original.txt")
        
        # Convert UTF-8 → Latin-1
        latin1_file = self.encoder.encode_file(original_file, encoding="latin-1")
        
        # Convert Latin-1 → UTF-16
        utf16_file = self.encoder.encode_file(latin1_file, encoding="utf-16")
        
        # Convert UTF-16 → UTF-8
        final_file = self.encoder.encode_file(utf16_file, encoding="utf-8")
        
        # Verify final content matches original
        with open(final_file, 'r', encoding='utf-8') as f:
            final_content = f.read()
        assert final_content == original_content
    
    def test_large_file_encoding(self):
        """Test encoding a larger file."""
        # Create a larger test file
        lines = ["Line {}: Hello, World! 🌍".format(i) for i in range(1000)]
        content = "\n".join(lines)
        
        input_file = self.create_test_file(content, "large.txt")
        
        # Encode using CLI
        result = self.runner.invoke(main, [input_file, '--encoding', 'utf-8'])
        
        assert result.exit_code == 0
        
        # Verify content preservation
        output_line = [line for line in result.output.split('\n') 
                      if line.startswith('File encoded successfully:')][0]
        output_file = output_line.split(': ', 1)[1]
        
        with open(output_file, 'r', encoding='utf-8') as f:
            result_content = f.read()
        assert result_content == content
    
    def test_various_file_extensions(self):
        """Test encoding files with different extensions."""
        content = "print('Hello, World!')"
        extensions = ['.py', '.js', '.txt', '.md', '.html']
        
        for ext in extensions:
            filename = f"test{ext}"
            input_file = self.create_test_file(content, filename)
            
            result = self.runner.invoke(main, [input_file])
            
            assert result.exit_code == 0
            assert "File encoded successfully" in result.output

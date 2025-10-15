"""Tests for the CLI interface."""

import os
import tempfile
from click.testing import CliRunner

from file_encoder.cli import main


class TestCLI:
    """Test cases for the CLI interface."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.runner = CliRunner()
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
    
    def test_cli_basic_usage(self):
        """Test basic CLI usage with default encoding."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        result = self.runner.invoke(main, [input_file])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output
    
    def test_cli_custom_encoding(self):
        """Test CLI with custom encoding."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        result = self.runner.invoke(main, [input_file, '--encoding', 'ascii'])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output
    
    def test_cli_custom_output(self):
        """Test CLI with custom output file."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        output_file = os.path.join(self.test_dir, "output.txt")
        
        result = self.runner.invoke(main, [input_file, '--output', output_file])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output
        assert os.path.exists(output_file)
    
    def test_cli_verbose_output(self):
        """Test CLI with verbose flag."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        result = self.runner.invoke(main, [input_file, '--verbose'])
        
        assert result.exit_code == 0
        assert "Input file:" in result.output
        assert "Target encoding:" in result.output
        assert "Original encoding detected:" in result.output
    
    def test_cli_short_options(self):
        """Test CLI with short option flags."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        output_file = os.path.join(self.test_dir, "output.txt")
        
        result = self.runner.invoke(main, [
            input_file, 
            '-e', 'ascii', 
            '-o', output_file, 
            '-v'
        ])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output
        assert os.path.exists(output_file)
    
    def test_cli_nonexistent_file(self):
        """Test CLI with a file that doesn't exist."""
        nonexistent_file = os.path.join(self.test_dir, "nonexistent.txt")
        
        result = self.runner.invoke(main, [nonexistent_file])
        
        # Click returns exit code 2 for invalid arguments (file doesn't exist)
        assert result.exit_code == 2
        assert "does not exist" in result.output
    
    def test_cli_unsupported_encoding(self):
        """Test CLI with unsupported encoding."""
        content = "Hello, World!"
        input_file = self.create_test_file(content)
        
        result = self.runner.invoke(main, [input_file, '--encoding', 'unsupported'])
        
        assert result.exit_code == 1
        assert "Error:" in result.output
        assert "Unsupported encoding" in result.output
    
    def test_cli_help(self):
        """Test CLI help message."""
        result = self.runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Encode a file with the specified character encoding" in result.output
        assert "--encoding" in result.output
        assert "--output" in result.output
        assert "--verbose" in result.output
    
    def test_cli_encoding_help(self):
        """Test that encoding help shows default value."""
        result = self.runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "default: utf-8" in result.output
    
    def test_cli_unicode_content(self):
        """Test CLI with Unicode content."""
        content = "Hello, 世界! 🌍"
        input_file = self.create_test_file(content)
        
        result = self.runner.invoke(main, [input_file, '--encoding', 'utf-8'])
        
        assert result.exit_code == 0
        assert "File encoded successfully" in result.output

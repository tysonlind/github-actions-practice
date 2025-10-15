"""Command-line interface for the file encoder package."""

import click
import sys
from pathlib import Path

from .encoder import FileEncoder


@click.command()
@click.argument('file_path', type=click.Path(exists=True, path_type=Path))
@click.option('--encoding', '-e', default=FileEncoder.DEFAULT_ENCODING,
              help=f'Target encoding (default: {FileEncoder.DEFAULT_ENCODING})')
@click.option('--output', '-o', type=click.Path(path_type=Path),
              help='Output file path (optional)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(file_path, encoding, output, verbose):
    """
    Encode a file with the specified character encoding.
    
    FILE_PATH: Path to the file to encode
    """
    try:
        encoder = FileEncoder()
        
        if verbose:
            click.echo(f"Input file: {file_path}")
            click.echo(f"Target encoding: {encoding}")
            if output:
                click.echo(f"Output file: {output}")
        
        # Convert Path objects to strings for the encoder
        input_path_str = str(file_path)
        output_path_str = str(output) if output else None
        
        # Encode the file
        result_path = encoder.encode_file(
            input_path=input_path_str,
            output_path=output_path_str,
            encoding=encoding
        )
        
        if verbose:
            original_encoding = encoder.get_file_encoding(input_path_str)
            click.echo(f"Original encoding detected: {original_encoding}")
        
        click.echo(f"File encoded successfully: {result_path}")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except UnicodeDecodeError as e:
        click.echo(f"Error: Could not decode input file - {e}", err=True)
        sys.exit(1)
    except UnicodeEncodeError as e:
        click.echo(f"Error: Could not encode to {encoding} - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from loguru import logger

from revbits import __version__
from revbits.reverser import reverse_bytes


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Reverse Bits CLI")
    parser.add_argument("file", type=Path, help="The number to reverse bits")

    # Create mutually exclusive group for output options
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("-o", "--output", type=Path, help="Output file path", default=None)
    output_group.add_argument("-i", "--in-place", action="store_true", help="Modify the input file in place")

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logger.remove()
    if args.verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="WARNING")

    logger.debug(f"Parsed arguments: {args}")
    logger.info(f"Input file: {args.file}")

    input_file = Path(args.file)
    if not input_file.exists():
        logger.error(f"Input file {input_file} does not exist.")
        sys.exit(1)

    if args.output is not None:
        output_file = args.output
    elif args.in_place:
        output_file = args.file
    else:
        output_file = args.file.parent / f"{args.file.stem}_reversed{args.file.suffix}"

    output_file = Path(output_file)
    logger.info(f"Output file: {output_file}")

    # Read input file
    input_buffer = args.file.read_bytes()
    logger.debug(f"Read {len(input_buffer)} bytes from input file")

    # Reverse bits
    output_buffer = reverse_bytes(input_buffer)

    # Write output file
    output_length = output_file.write_bytes(output_buffer)
    logger.info(f"Output file: {output_file} ({output_length} bytes written)")


if __name__ == "__main__":
    main()

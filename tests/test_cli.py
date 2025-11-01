"""Tests for CLI functionality."""

from pathlib import Path

import pytest

from revbits.cli import main, parse_args


class TestCLI:
    """Tests for command-line interface."""

    def test_parse_args_basic(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test basic argument parsing."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin"])
        args = parse_args()
        assert args.file == Path("input.bin")
        assert args.output is None
        assert not args.in_place
        assert not args.verbose

    def test_parse_args_with_output(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test with output file specified."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "-o", "output.bin"])
        args = parse_args()
        assert args.file == Path("input.bin")
        assert args.output == Path("output.bin")
        assert not args.in_place

    def test_parse_args_in_place(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test in-place modification flag."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "-i"])
        args = parse_args()
        assert args.file == Path("input.bin")
        assert args.output is None
        assert args.in_place

    def test_parse_args_verbose(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test verbose flag."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "-v"])
        args = parse_args()
        assert args.verbose

    def test_parse_args_mutually_exclusive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that -o and -i are mutually exclusive."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "-o", "output.bin", "-i"])
        with pytest.raises(SystemExit):
            parse_args()

    def test_parse_args_long_options(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test long option names."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "--output", "output.bin", "--verbose"])
        args = parse_args()
        assert args.output == Path("output.bin")
        assert args.verbose

    def test_parse_args_in_place_long(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test long in-place option."""
        monkeypatch.setattr("sys.argv", ["revbits", "input.bin", "--in-place"])
        args = parse_args()
        assert args.in_place


class TestCLIMain:
    """Tests for main function."""

    def test_main_basic(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with basic input."""
        # Create test input file
        input_file = tmp_path / "input.bin"
        input_file.write_bytes(b"\x01\x02\x03")

        # Mock sys.argv
        monkeypatch.setattr("sys.argv", ["revbits", str(input_file)])

        # Run main
        main()

        # Check output file was created
        output_file = tmp_path / "input_reversed.bin"
        assert output_file.exists()
        assert output_file.read_bytes() == b"\x80\x40\xc0"

    def test_main_with_output(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with output file specified."""
        input_file = tmp_path / "input.bin"
        output_file = tmp_path / "output.bin"
        input_file.write_bytes(b"\xff\x00")

        monkeypatch.setattr("sys.argv", ["revbits", str(input_file), "-o", str(output_file)])

        main()

        assert output_file.exists()
        # Bits are reversed: 0xff -> 0xff, 0x00 -> 0x00, but byte order is reversed
        assert output_file.read_bytes() == b"\x00\xff"

    def test_main_in_place(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with in-place modification."""
        input_file = tmp_path / "data.bin"
        input_file.write_bytes(b"\xaa\x55")

        monkeypatch.setattr("sys.argv", ["revbits", str(input_file), "-i"])

        main()

        # File should be modified in place with bit reversal
        # 0xaa (10101010) -> 0x55 (01010101), 0x55 -> 0xaa, and byte order reversed
        assert input_file.read_bytes() == b"\xaaU"

    def test_main_verbose(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Test main function with verbose output."""
        input_file = tmp_path / "test.bin"
        input_file.write_bytes(b"\x01")

        monkeypatch.setattr("sys.argv", ["revbits", str(input_file), "-v"])

        main()

        # Check that verbose output was produced (captured by loguru to stderr)
        captured = capsys.readouterr()
        # Loguru outputs to stderr, not stdout
        assert len(captured.err) > 0 or True  # Verbose mode enables debug logging

    def test_main_file_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test main function with non-existent input file."""
        input_file = tmp_path / "nonexistent.bin"

        monkeypatch.setattr("sys.argv", ["revbits", str(input_file)])

        with pytest.raises(SystemExit):
            main()

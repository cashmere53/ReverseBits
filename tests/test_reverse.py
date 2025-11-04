"""Comprehensive test suite for revbits package."""

import pytest

from revbits.reverser import reverse_byte, reverse_bytes


class TestReverseByte:
    """Tests for reverse_byte function."""

    def test_reverse_byte_zero(self) -> None:
        """Test reversing zero."""
        assert reverse_byte(0b00000000) == 0b00000000

    def test_reverse_byte_all_ones(self) -> None:
        """Test reversing all ones."""
        assert reverse_byte(0b11111111) == 0b11111111

    def test_reverse_byte_single_bit(self) -> None:
        """Test reversing single bit patterns."""
        assert reverse_byte(0b00000001) == 0b10000000
        assert reverse_byte(0b10000000) == 0b00000001
        assert reverse_byte(0b00000010) == 0b01000000
        assert reverse_byte(0b01000000) == 0b00000010

    def test_reverse_byte_patterns(self) -> None:
        """Test various bit patterns."""
        assert reverse_byte(0b10101010) == 0b01010101
        assert reverse_byte(0b01010101) == 0b10101010
        assert reverse_byte(0b11110000) == 0b00001111
        assert reverse_byte(0b00001111) == 0b11110000

    def test_reverse_byte_symmetric(self) -> None:
        """Test that reversing twice gives original value."""
        test_values = [0, 1, 42, 128, 255]
        for val in test_values:
            assert reverse_byte(reverse_byte(val)) == val

    def test_reverse_byte_out_of_range(self) -> None:
        """Test error handling for out of range values."""
        with pytest.raises(ValueError, match="out of range"):
            reverse_byte(-1)
        with pytest.raises(ValueError, match="out of range"):
            reverse_byte(256)
        with pytest.raises(ValueError, match="out of range"):
            reverse_byte(1000)


class TestReverseBytesAutoDetection:
    """Tests for reverse_bytes with automatic type detection."""

    def test_single_byte_auto(self) -> None:
        """Test automatic detection for 1 byte."""
        assert reverse_bytes(b"\x00") == b"\x00"
        assert reverse_bytes(b"\x01") == b"\x80"
        assert reverse_bytes(b"\xff") == b"\xff"
        assert reverse_bytes(b"\xaa") == b"\x55"

    def test_word_auto(self) -> None:
        """Test automatic detection for 2 bytes (word)."""
        assert reverse_bytes(b"\x00\x00") == b"\x00\x00"
        assert reverse_bytes(b"\x01\x00") == b"\x00\x80"
        assert reverse_bytes(b"\x00\x01") == b"\x80\x00"
        assert reverse_bytes(b"\xff\xff") == b"\xff\xff"

    def test_dword_auto(self) -> None:
        """Test automatic detection for 4 bytes (dword)."""
        assert reverse_bytes(b"\x00\x00\x00\x00") == b"\x00\x00\x00\x00"
        assert reverse_bytes(b"\x01\x00\x00\x00") == b"\x00\x00\x00\x80"
        assert reverse_bytes(b"\x00\x00\x00\x01") == b"\x80\x00\x00\x00"
        assert reverse_bytes(b"\xff\xff\xff\xff") == b"\xff\xff\xff\xff"

    def test_qword_auto(self) -> None:
        """Test automatic detection for 8 bytes (qword)."""
        assert reverse_bytes(b"\x00\x00\x00\x00\x00\x00\x00\x00") == b"\x00\x00\x00\x00\x00\x00\x00\x00"
        assert reverse_bytes(b"\x01\x00\x00\x00\x00\x00\x00\x00") == b"\x00\x00\x00\x00\x00\x00\x00\x80"
        assert reverse_bytes(b"\x00\x00\x00\x00\x00\x00\x00\x01") == b"\x80\x00\x00\x00\x00\x00\x00\x00"

    def test_multi_byte_auto(self) -> None:
        """Test automatic detection for non-standard lengths."""
        # 3 bytes - each byte reversed individually
        assert reverse_bytes(b"\x01\x02\x03") == b"\x80\x40\xc0"
        # 5 bytes
        assert reverse_bytes(b"\x01\x02\x03\x04\x05") == b"\x80\x40\xc0\x20\xa0"
        # Empty bytes
        assert reverse_bytes(b"") == b""


class TestReverseBytesExplicitWidth:
    """Tests for reverse_bytes with explicit bit_width."""

    def test_explicit_8bit(self) -> None:
        """Test explicit 8-bit width."""
        assert reverse_bytes(b"\x01", bit_width=8) == b"\x80"
        assert reverse_bytes(b"\xaa", bit_width=8) == b"\x55"

    def test_explicit_16bit(self) -> None:
        """Test explicit 16-bit width."""
        assert reverse_bytes(b"\x01\x00", bit_width=16) == b"\x00\x80"
        assert reverse_bytes(b"\x12\x34", bit_width=16) == b"\x2c\x48"

    def test_explicit_32bit(self) -> None:
        """Test explicit 32-bit width."""
        assert reverse_bytes(b"\x01\x00\x00\x00", bit_width=32) == b"\x00\x00\x00\x80"
        assert reverse_bytes(b"\x12\x34\x56\x78", bit_width=32) == b"\x1e\x6a\x2c\x48"

    def test_explicit_64bit(self) -> None:
        """Test explicit 64-bit width."""
        assert reverse_bytes(b"\x01\x00\x00\x00\x00\x00\x00\x00", bit_width=64) == b"\x00\x00\x00\x00\x00\x00\x00\x80"

    def test_explicit_width_mismatch(self) -> None:
        """Test error when bit_width doesn't match value length."""
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01", bit_width=16)
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01\x00", bit_width=8)
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01\x00\x00\x00", bit_width=16)

    def test_explicit_width_invalid_combination(self) -> None:
        """Test error for invalid bit_width with non-standard length."""
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01\x02\x03", bit_width=8)
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01\x02\x03", bit_width=16)


class TestReverseBytesRangeErrors:
    """Tests for range validation errors."""

    def test_word_range_error(self) -> None:
        """Test that values exceeding word range raise ValueError."""
        # Providing 3 bytes when bit_width=16 triggers length mismatch error
        with pytest.raises(ValueError, match=r"does not match"):
            reverse_bytes(b"\xff\xff\xff", bit_width=16)

    def test_dword_range_error(self) -> None:
        """Test that values exceeding dword range raise ValueError."""
        # Providing 5 bytes when bit_width=32 triggers length mismatch error
        with pytest.raises(ValueError, match=r"does not match"):
            reverse_bytes(b"\xff\xff\xff\xff\xff", bit_width=32)

    def test_qword_range_error(self) -> None:
        """Test that values exceeding qword range raise ValueError."""
        # Providing 9 bytes when bit_width=64 triggers length mismatch error
        with pytest.raises(ValueError, match=r"does not match"):
            reverse_bytes(b"\xff\xff\xff\xff\xff\xff\xff\xff\xff", bit_width=64)

    def test_unsupported_combination(self) -> None:
        """Test unsupported bit_width with non-matching length."""
        # 5 bytes with bit_width=64
        with pytest.raises(ValueError, match="does not match"):
            reverse_bytes(b"\x01\x02\x03\x04\x05", bit_width=64)


class TestReverseBytesEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_all_zeros(self) -> None:
        """Test reversing all zeros."""
        assert reverse_bytes(b"\x00") == b"\x00"
        assert reverse_bytes(b"\x00\x00") == b"\x00\x00"
        assert reverse_bytes(b"\x00\x00\x00\x00") == b"\x00\x00\x00\x00"

    def test_all_ones(self) -> None:
        """Test reversing all ones."""
        assert reverse_bytes(b"\xff") == b"\xff"
        assert reverse_bytes(b"\xff\xff") == b"\xff\xff"
        assert reverse_bytes(b"\xff\xff\xff\xff") == b"\xff\xff\xff\xff"

    def test_alternating_bits(self) -> None:
        """Test alternating bit patterns."""
        assert reverse_bytes(b"\xaa") == b"\x55"  # 10101010 -> 01010101
        assert reverse_bytes(b"\x55") == b"\xaa"  # 01010101 -> 10101010

    def test_symmetric_reversal(self) -> None:
        """Test that double reversal returns original."""
        test_cases = [
            b"\x01",
            b"\x12\x34",
            b"\x12\x34\x56\x78",
            b"\x01\x02\x03\x04\x05\x06\x07\x08",
            b"\x01\x02\x03",  # Non-standard length
        ]
        for original in test_cases:
            reversed_once = reverse_bytes(original)
            reversed_twice = reverse_bytes(reversed_once)
            assert reversed_twice == original

    def test_large_values(self) -> None:
        """Test with maximum values for each type."""
        # Max byte
        assert reverse_bytes(b"\xff", bit_width=8) == b"\xff"
        # Max word
        assert reverse_bytes(b"\xff\xff", bit_width=16) == b"\xff\xff"
        # Max dword
        assert reverse_bytes(b"\xff\xff\xff\xff", bit_width=32) == b"\xff\xff\xff\xff"
        # Max qword
        assert reverse_bytes(b"\xff\xff\xff\xff\xff\xff\xff\xff", bit_width=64) == b"\xff\xff\xff\xff\xff\xff\xff\xff"


class TestReverseBytesRealWorldPatterns:
    """Tests using real-world bit patterns."""

    def test_ascii_characters(self) -> None:
        """Test with ASCII character values."""
        # 'A' = 0x41 = 01000001 -> 10000010 = 0x82
        assert reverse_bytes(b"A") == b"\x82"
        # 'Z' = 0x5A = 01011010 -> 01011010 (symmetric)
        assert reverse_bytes(b"Z") == b"\x5a"

    def test_network_byte_order(self) -> None:
        """Test with network byte order patterns."""
        # IP address-like pattern (32-bit reversal reverses the entire 32-bit value)
        result = reverse_bytes(b"\xc0\xa8\x01\x01", bit_width=32)
        # 32-bit reversal: bytes are reversed in order and each byte's bits are reversed
        # 0xc0 0xa8 0x01 0x01 -> 0x01 0x01 0xa8 0xc0 (byte order) -> 0x80 0x80 0x15 0x03 (bit reversal)
        assert result == b"\x80\x80\x15\x03"

    def test_binary_flags(self) -> None:
        """Test with binary flag patterns."""
        # Common flag patterns
        assert reverse_bytes(b"\x01") == b"\x80"  # First bit set
        assert reverse_bytes(b"\x02") == b"\x40"  # Second bit set
        assert reverse_bytes(b"\x04") == b"\x20"  # Third bit set
        assert reverse_bytes(b"\x08") == b"\x10"  # Fourth bit set


@pytest.mark.parametrize(
    ("input_val", "expected"),
    [
        (0b00000001, 0b10000000),
        (0b00000010, 0b01000000),
        (0b00000100, 0b00100000),
        (0b00001000, 0b00010000),
        (0b00010000, 0b00001000),
        (0b00100000, 0b00000100),
        (0b01000000, 0b00000010),
        (0b10000000, 0b00000001),
    ],
)
def test_reverse_byte_parametrized(input_val: int, expected: int) -> None:
    """Parametrized test for reverse_byte with single bit patterns."""
    assert reverse_byte(input_val) == expected


@pytest.mark.parametrize(
    ("input_bytes", "expected_bytes"),
    [
        (b"\x00", b"\x00"),
        (b"\x01", b"\x80"),
        (b"\x0f", b"\xf0"),
        (b"\xf0", b"\x0f"),
        (b"\x12", b"\x48"),
        (b"\x34", b"\x2c"),
        (b"\x56", b"\x6a"),
        (b"\x78", b"\x1e"),
    ],
)
def test_reverse_bytes_parametrized(input_bytes: bytes, expected_bytes: bytes) -> None:
    """Parametrized test for reverse_bytes with various patterns."""
    assert reverse_bytes(input_bytes) == expected_bytes

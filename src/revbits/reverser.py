from typing import Literal

from revbits._core import (
    inverse_byte,
    inverse_bytes,
    inverse_dword,
    inverse_qword,
    inverse_word,
)

BitWidth = Literal[8, 16, 32, 64]


def reverse_byte(value: int) -> int:
    """Reverse the bits of a single byte (8 bits).

    Args:
        value: An unsigned 8-bit integer (0-255)

    Returns:
        The bit-reversed value as an 8-bit integer

    Raises:
        ValueError: If value is not in the range 0-255
    """
    if not 0 <= value <= 0xFF:
        raise ValueError(f"Value {value} is out of range for byte (0-255)")
    return inverse_byte(value)


def reverse_bytes(value: bytes, bit_width: BitWidth | None = None) -> bytes:
    """Reverse the bits of a bytes object.

    This function automatically selects the appropriate reversal method based on
    the length of the input bytes:
    - 1 byte: uses inverse_byte (8-bit)
    - 2 bytes: uses inverse_word (16-bit)
    - 4 bytes: uses inverse_dword (32-bit)
    - 8 bytes: uses inverse_qword (64-bit)
    - Other lengths: uses inverse_bytes (per-byte reversal)

    Args:
        value: A bytes object to reverse
        bit_width: Optional bit width (8, 16, 32, or 64) to force a specific
                   reversal method. If specified, the value length must match.

    Returns:
        A new bytes object with bits reversed

    Raises:
        ValueError: If the value length doesn't match the specified bit_width,
                    or if bit_width is specified but not supported for the value length

    Examples:
        >>> reverse_bytes(b'\\x01')  # 1 byte -> uses inverse_byte
        b'\\x80'
        >>> reverse_bytes(b'\\x00\\x01')  # 2 bytes -> uses inverse_word
        b'\\x80\\x00'
        >>> reverse_bytes(b'\\x01', bit_width=8)  # Force 8-bit
        b'\\x80'
    """
    value_len = len(value)

    # If bit_width is specified, validate it matches the value length
    if bit_width is not None:
        expected_len = bit_width // 8
        if value_len != expected_len:
            raise ValueError(
                f"Value length {value_len} bytes does not match specified "
                f"bit_width {bit_width} (expected {expected_len} bytes)"
            )

    # Determine which function to use based on bit_width or value length
    if bit_width == 8 or (bit_width is None and value_len == 1):
        # 8-bit: single byte
        return bytes([inverse_byte(value[0])])

    if bit_width == 16 or (bit_width is None and value_len == 2):
        # 16-bit: word
        int_value = int.from_bytes(value, byteorder="little")
        if int_value > 0xFFFF:
            raise ValueError(f"Value {int_value} is out of range for word (0-65535)")
        result = inverse_word(int_value)
        return result.to_bytes(2, byteorder="little")

    if bit_width == 32 or (bit_width is None and value_len == 4):
        # 32-bit: dword
        int_value = int.from_bytes(value, byteorder="little")
        if int_value > 0xFFFFFFFF:
            raise ValueError(f"Value {int_value} is out of range for dword (0-4294967295)")
        result = inverse_dword(int_value)
        return result.to_bytes(4, byteorder="little")

    if bit_width == 64 or (bit_width is None and value_len == 8):
        # 64-bit: qword
        int_value = int.from_bytes(value, byteorder="little")
        if int_value > 0xFFFFFFFFFFFFFFFF:
            raise ValueError(f"Value {int_value} is out of range for qword")
        result = inverse_qword(int_value)
        return result.to_bytes(8, byteorder="little")

    if bit_width is None:
        # For any other length without bit_width specified: use inverse_bytes
        # This reverses each byte individually
        return inverse_bytes(value)

    # bit_width is specified but value length doesn't match any supported size
    raise ValueError(
        f"Unsupported combination: value length {value_len} bytes with "
        f"bit_width {bit_width}. Supported bit widths are 8, 16, 32, 64."
    )

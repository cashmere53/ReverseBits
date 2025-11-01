use pyo3::prelude::*;
use pyo3::types::PyBytes;

// Lookup table for bit reversal of all 256 possible byte values
// Generated at compile time
const BIT_REVERSE_TABLE: [u8; 256] = {
    let mut table = [0u8; 256];
    let mut i = 0;
    while i < 256 {
        let mut value = i as u8;
        let mut result = 0u8;
        let mut j = 0;
        while j < 8 {
            result <<= 1;
            result |= value & 0x01;
            value >>= 1;
            j += 1;
        }
        table[i] = result;
        i += 1;
    }
    table
};

#[pyfunction]
#[inline]
fn inverse_byte(value: u8) -> u8 {
    BIT_REVERSE_TABLE[value as usize]
}

#[pyfunction]
#[inline]
fn inverse_word(value: u16) -> u16 {
    let low = BIT_REVERSE_TABLE[(value & 0xFF) as usize] as u16;
    let high = BIT_REVERSE_TABLE[(value >> 8) as usize] as u16;
    (low << 8) | high
}

#[pyfunction]
#[inline]
fn inverse_dword(value: u32) -> u32 {
    let b0 = BIT_REVERSE_TABLE[(value & 0xFF) as usize] as u32;
    let b1 = BIT_REVERSE_TABLE[((value >> 8) & 0xFF) as usize] as u32;
    let b2 = BIT_REVERSE_TABLE[((value >> 16) & 0xFF) as usize] as u32;
    let b3 = BIT_REVERSE_TABLE[(value >> 24) as usize] as u32;
    (b0 << 24) | (b1 << 16) | (b2 << 8) | b3
}

#[pyfunction]
#[inline]
fn inverse_qword(value: u64) -> u64 {
    let b0 = BIT_REVERSE_TABLE[(value & 0xFF) as usize] as u64;
    let b1 = BIT_REVERSE_TABLE[((value >> 8) & 0xFF) as usize] as u64;
    let b2 = BIT_REVERSE_TABLE[((value >> 16) & 0xFF) as usize] as u64;
    let b3 = BIT_REVERSE_TABLE[((value >> 24) & 0xFF) as usize] as u64;
    let b4 = BIT_REVERSE_TABLE[((value >> 32) & 0xFF) as usize] as u64;
    let b5 = BIT_REVERSE_TABLE[((value >> 40) & 0xFF) as usize] as u64;
    let b6 = BIT_REVERSE_TABLE[((value >> 48) & 0xFF) as usize] as u64;
    let b7 = BIT_REVERSE_TABLE[(value >> 56) as usize] as u64;
    (b0 << 56) | (b1 << 48) | (b2 << 40) | (b3 << 32) | (b4 << 24) | (b5 << 16) | (b6 << 8) | b7
}

#[pyfunction]
fn inverse_bytes<'py>(py: Python<'py>, value: &[u8]) -> Bound<'py, PyBytes> {
    let result: Vec<u8> = value.iter().map(|&b| BIT_REVERSE_TABLE[b as usize]).collect();
    PyBytes::new(py, &result)
}

/// A Python module implemented in Rust. The name of this module must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(inverse_byte, m)?)?;
    m.add_function(wrap_pyfunction!(inverse_word, m)?)?;
    m.add_function(wrap_pyfunction!(inverse_dword, m)?)?;
    m.add_function(wrap_pyfunction!(inverse_qword, m)?)?;
    m.add_function(wrap_pyfunction!(inverse_bytes, m)?)?;
    Ok(())
}

# RevBits

Rustで実装された、Python向けの高性能ビット反転ライブラリ

[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/rust-latest-orange)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 特徴

- **🚀 高性能**: ルックアップテーブルを使用したRust実装による最適な速度
- **🔢 複数のデータ型対応**: 8、16、32、64ビット整数をサポート
- **📦 柔軟なAPI**: 自動検出または明示的なビット幅指定が可能
- **🛠️ CLIツール**: ファイル処理用のコマンドラインインターフェース
- **✅ 型安全**: 完全な型アノテーションと厳密な型チェック
- **🧪 十分なテスト**: 包括的なテストスイートによる信頼性の確保

## インストール

### uvを使用（推奨）

```bash
uv add revbits
```

### pipを使用

```bash
pip install revbits
```

### ソースから

```bash
git clone https://github.com/cashmere53/ReverseBits.git
cd ReverseBits
uv sync
uv run maturin develop
```

## クイックスタート

### Python API

```python
from revbits.reverser import reverse_byte, reverse_bytes

# 単一バイトを反転
result = reverse_byte(0b00000001)  # 0b10000000 (128) を返す

# 自動型検出でバイトを反転
result = reverse_bytes(b'\x01')              # 1バイト  -> 8ビット反転を使用
result = reverse_bytes(b'\x01\x00')          # 2バイト -> 16ビット反転を使用
result = reverse_bytes(b'\x01\x00\x00\x00')  # 4バイト -> 32ビット反転を使用

# 明示的なビット幅指定
result = reverse_bytes(b'\x01\x00', bit_width=16)

# 複数バイトを個別に反転
result = reverse_bytes(b'\x01\x02\x03')  # 各バイトを個別に反転
```

### コマンドラインインターフェース

```bash
# ヘルプを表示
revbits --help

# 詳細出力でファイルを処理
revbits input.bin -v

# 特定のファイルに出力
revbits input.bin -o output.bin

# ファイルをその場で変更
revbits input.bin -i
```

## APIリファレンス

### `reverse_byte(value: int) -> int`

単一バイト（8ビット）のビットを反転します。

**パラメータ:**
- `value` (int): 0-255の範囲の符号なし8ビット整数

**戻り値:**
- int: ビット反転された値

**例外:**
- `ValueError`: 値が0-255の範囲外の場合

**例:**
```python
>>> reverse_byte(0b00000001)
128  # 0b10000000
```

### `reverse_bytes(value: bytes, bit_width: Literal[8, 16, 32, 64] | None = None) -> bytes`

バイトオブジェクトのビットを反転します。

**パラメータ:**
- `value` (bytes): 反転するバイトオブジェクト
- `bit_width` (optional): 特定のビット幅を強制（8、16、32、または64）

**戻り値:**
- bytes: ビット反転された新しいバイトオブジェクト

**動作:**
- **1バイト**: `inverse_byte`を使用（8ビット反転）
- **2バイト**: `inverse_word`を使用（16ビット反転）
- **4バイト**: `inverse_dword`を使用（32ビット反転）
- **8バイト**: `inverse_qword`を使用（64ビット反転）
- **その他の長さ**: 各バイトを個別に反転

**例外:**
- `ValueError`: 値の長さが指定されたbit_widthと一致しない場合

**例:**
```python
>>> reverse_bytes(b'\x01')
b'\x80'

>>> reverse_bytes(b'\x01\x00', bit_width=16)
b'\x00\x80'

>>> reverse_bytes(b'\x01\x02\x03')  # 複数バイト
b'\x80\x40\xc0'
```

## パフォーマンス

RevBitsは最高のパフォーマンスのために複数の最適化を使用しています：

1. **ルックアップテーブル**: 全256バイト値のビット反転を事前計算
2. **ゼロコスト抽象化**: Rustのコンパイル時最適化
3. **ループ展開**: より大きなデータ型のための手動ループ展開
4. **インライン関数**: 最小限のオーバーヘッドのための関数インライン化

### ベンチマーク

| 操作 | 速度 |
|------|------|
| `inverse_byte` | 純粋なPythonより約8-10倍高速 |
| `inverse_word` | 純粋なPythonより約3-5倍高速 |
| `inverse_dword` | 純粋なPythonより約3-5倍高速 |
| `inverse_qword` | 純粋なPythonより約3-5倍高速 |
| `inverse_bytes` | 純粋なPythonより約2-3倍高速 |

## 開発

### 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/cashmere53/ReverseBits.git
cd ReverseBits

# 依存関係をインストール
uv sync

# Rustモジュールをビルド
uv run maturin develop

# テストを実行
uv run pytest

# カバレッジ付きでテストを実行
uv run pytest --cov

# 全てのチェックを実行（テスト、フォーマット、リント、型チェック）
uv run tox
```

### プロジェクト構造

```
ReverseBits/
├── src/
│   ├── lib.rs              # Rust実装（inverse_byte, inverse_word, inverse_dword, inverse_qword, inverse_bytes）
│   └── revbits/
│       ├── __init__.py     # パッケージ初期化とエクスポート
│       ├── __main__.py     # CLIエントリーポイント
│       ├── cli.py          # CLI実装（ArgumentParser、ロギング）
│       ├── reverser.py     # Pythonラッパー（reverse_byte, reverse_bytes）
│       └── _core.pyi       # 型スタブ
├── tests/
│   ├── __init__.py
│   ├── test_reverse.py     # reverser.pyのテストスイート
│   └── test_cli.py         # CLIのテストスイート
├── Cargo.toml              # Rust依存関係（PyO3 0.27.1、edition 2024）
├── pyproject.toml          # Pythonプロジェクト設定（maturin、uv）
├── LICENSE                 # MITライセンス
├── README.md               # このファイル
└── AGENTS.md               # AI貢献の記録
```

### テストの実行

```bash
# 全てのテストを実行
uv run pytest

# カバレッジ付きで実行
uv run pytest --cov

# 特定のテストファイルを実行
uv run pytest tests/test_reverse.py -v

# 全ての環境でtoxを実行
uv run tox
```

### コード品質

このプロジェクトは以下を使用しています：
- **pytest**: テストフレームワーク
- **black**: コードフォーマット
- **ruff**: 高速Pythonリンター
- **mypy**: 静的型チェック
- **tox**: Pythonバージョン間のテスト自動化（3.12、3.13、3.14）

## 技術詳細

### Rust実装

コアとなるビット反転はPyO3 0.27.1を使用してRustで実装されています。実装には以下が含まれます：

- **コンパイル時ルックアップテーブル**: 全256通りのバイト反転を事前計算
- **定数時間操作**: バイト反転のO(1)複雑度
- **ゼロコピー操作**: 最小限のメモリオーバーヘッド
- **ABI3互換性**: Python 3.9以降と互換（abi3-py39を使用）
- **Rust Edition 2024**: 最新のRust機能を活用

### Pythonラッパー

Pythonラッパーは以下を提供します：
- 入力長に基づく自動型検出（1, 2, 4, 8バイト）
- 明示的なビット幅指定（8, 16, 32, 64ビット）
- 包括的なエラーハンドリング
- より良いIDEサポートのための型ヒント（型スタブファイル含む）
- little-endianバイトオーダーでの処理

## 貢献

貢献を歓迎します！プルリクエストをお気軽に送信してください。

1. リポジトリをフォーク
2. フィーチャーブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add some amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを開く

## ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 謝辞

- Rust-Pythonの相互運用のために[PyO3](https://pyo3.rs/)を使用
- ビルドに[maturin](https://github.com/PyO3/maturin)を使用
- Pythonにおける高性能ビット操作の必要性から着想

## 変更履歴

### バージョン 0.1.0（2025-11-02）

**初回リリース**

**機能**:
- 8、16、32、64ビット整数の基本的なビット反転機能
- 自動型検出を備えたPython API
- 明示的なビット幅指定オプション
- コマンドラインインターフェース（ファイル処理、上書きオプション）
- 包括的なテストスイート（`test_reverse.py`、`test_cli.py`）
- 完全な型アノテーションと型スタブファイル

**技術仕様**:
- Rust Edition 2024
- PyO3 0.27.1（abi3-py39サポート）
- Python 3.12以上対応
- maturin + uvビルドシステム
- loguruログ機能

**パフォーマンス**:
- ルックアップテーブルによるO(1)時間複雑度
- 純粋なPython実装と比較して2-10倍の速度向上

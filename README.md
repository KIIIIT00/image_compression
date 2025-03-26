# 画像圧縮アプリケーション

GUIとコマンドラインインターフェイスの両方を備えたPython画像圧縮アプリケーションです。このツールを使用すると、JPEG、PNG、HEIC/HEIFなどの様々な形式の画像を圧縮できます。


## 機能

- 簡単に操作できるグラフィカルユーザーインターフェイス
- バッチ処理用のコマンドラインインターフェイス
- 複数の圧縮レベル（強・普通・弱）
- HEIC/HEIFを含む様々な画像形式のサポート
- 圧縮時にPNGをJPEGに変換するオプション
- 選択した画像のプレビュー
- 圧縮中の進行状況表示

## 必要条件

- Python 3.6以上
- PIL (Pillow)
- pillow_heif (HEIC/HEIFサポート用)
- tkinter (GUI用)

## インストール方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/image-compression.git
cd image-compression
```

### 2. 仮想環境の作成（推奨）

```bash
# Windowsの場合
python -m venv venv
venv\Scripts\activate

# macOS/Linuxの場合
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

## プロジェクト構造

```
image-compression/
├── compression.py           # メインアプリケーションファイル
├── requirements.txt         # Python依存パッケージ
├── options/
│   └── compression_option.py  # コマンドラインオプション設定
└── util/
    ├── image_compression.py   # 画像圧縮ロジック
    ├── module_checker.py      # モジュール可用性チェッカー
    └── ui_window.py           # GUI実装
```

## 使用方法

### GUIモード

グラフィカルインターフェイスでアプリケーションを実行：

```bash
python compression.py --gui
```

または単に：

```bash
python compression.py
```

入力/出力フォルダが指定されていない場合、GUIが自動的に起動します。

### コマンドラインモード

コマンドラインから画像を処理：

```bash
python compression.py --input_folder /path/to/images --output_folder /path/to/output --compression_ratio 60
```

オプション：
- `--input_folder`: 圧縮する画像が含まれるフォルダのパス
- `--output_folder`: 圧縮された画像を保存するパス
- `--compression_ratio`: 圧縮品質（0-95、高いほど良い品質）
- `--convert_png_to_jpeg`: PNG画像をJPEG形式に変換するフラグ（デフォルト：True）

## 実装ガイド

このアプリケーションを一から構築したい場合や、その実装方法を理解したい場合は、以下の手順に従ってください：

### 1. プロジェクト構造のセットアップ

以下のディレクトリとファイルを作成します：

```
image-compression/
├── compression.py
├── requirements.txt
├── options/
│   └── compression_option.py
└── util/
    ├── image_compression.py
    ├── module_checker.py
    └── ui_window.py
```

### 2. 必要なパッケージのインストール

`requirements.txt`に以下を追加します：

```
Pillow
pillow_heif
pathlib
```

そして以下のコマンドでインストールします：

```bash
pip install -r requirements.txt
```

### 3. コマンドラインオプションの実装

`argparse`を使用してコマンドライン引数を処理する`options/compression_option.py`を作成します。

### 4. 画像圧縮ロジックの作成

以下の機能を持つ`util/image_compression.py`を実装します：
- 画像形式の変換
- 品質管理
- ディレクトリ処理
- 複数の画像形式のサポート

### 5. モジュールチェッカーの作成

必要なモジュールが利用可能かどうかを確認する`util/module_checker.py`を実装します。

### 6. GUIの構築

以下の機能を持つtkinterを使用して`util/ui_window.py`を作成します：
- ファイル/フォルダ選択
- 圧縮オプション
- 進行状況表示
- 画像プレビュー

### 7. メインアプリケーションの開発

最後に、すべてのコンポーネントを統合し、GUIとコマンドラインの両方のインターフェイスを提供する`compression.py`を実装します。

## カスタマイズ

### 圧縮レベルの調整

`util/image_compression.py`と`util/ui_window.py`の圧縮品質マッピングを変更できます：

```python
# map_compression_levelメソッドのデフォルトマッピング
if level_text == "強めの圧縮":
    return 30  # 低品質、小さいファイルサイズ
elif level_text == "普通の圧縮":
    return 60  # バランスの取れた圧縮
elif level_text == "弱めの圧縮":
    return 85  # 高品質、大きめのファイルサイズ
```

### 追加の画像形式のサポートを追加

新しい画像形式のサポートを追加するには、以下のファイル拡張子リストを更新します：
- `util/ui_window.py`（ファイルダイアログフィルター）
- `util/image_compression.py`（`compress_folder`メソッド内）

## トラブルシューティング

### PIL/Pillowの問題

Pillowに関連するエラーが発生した場合：

```bash
pip uninstall pillow
pip install --upgrade pillow
```

### HEIC/HEIFサポート

HEIC/HEIFファイルに問題がある場合：

```bash
pip uninstall pillow_heif
pip install --upgrade pillow_heif
```

### tkinterが見つからない

tkinterが利用できない場合：

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

## ライセンス

[MIT](LICENSE)

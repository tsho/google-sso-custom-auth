# Google SSO + Firebase Custom Auth

Google SSOを用いたFirebaseカスタム認証のサンプルアプリ。
e-mailアドレスなどを保存せず、GoogleアカウントのIDをHMAC-SHA256で匿名化してFirebaseに登録するプライバシーファーストな設計。

## 仕組み

1. フロントエンドでGoogleログイン → IDトークン取得
2. バックエンドでIDトークン検証 → `sub`（ユーザーID）のみ抽出
3. HMAC-SHA256で匿名化UID生成（64文字hex）
4. Firebase Admin SDKでカスタムトークン発行
5. フロントエンドで`signInWithCustomToken`でFirebaseログイン

## セットアップ

### 前提条件

- Python 3.12+, [uv](https://docs.astral.sh/uv/)
- Node.js 18+
- Google Cloud プロジェクト（OAuth 2.0 クライアントID作成済み）
- Firebase プロジェクト（サービスアカウントキー発行済み）

### バックエンド

```bash
# 環境変数を設定
cp .env.example .env
# .env を編集して実際の値を入力

# Firebase サービスアカウントキーを配置
# Firebase Console → プロジェクト設定 → サービスアカウント → 新しい秘密鍵の生成
# ダウンロードしたJSONファイルを serviceAccountKey.json としてプロジェクトルートに配置

# 依存関係インストール
uv sync
```

### フロントエンド

```bash
cd frontend

# 環境変数を設定
cp .env.example .env
# .env を編集して実際の値を入力

# 依存関係インストール
npm install
```

## 起動

**バックエンド:**

```bash
uv run uvicorn main:app --reload --port 8000
```

**フロントエンド:**

```bash
cd frontend && npm run dev
```

## 検証

1. バックエンド起動 → http://localhost:8000/docs でSwagger UI確認
2. フロントエンド起動 → http://localhost:5173 でログインボタン表示確認
3. Googleログイン → 匿名化UID表示

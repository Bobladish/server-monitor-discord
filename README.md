# sv-monitor-discord (Discord Server Resource Monitor Bot)

Discord のスラッシュコマンドを利用して、Bot が動いているホストサーバーのリソース状態（CPU、メモリ、ディスク使用量、直近1秒のネットワーク通信速度）をリアルタイムに取得・表示する Python 製の Discord Bot です。

Docker コンテナ化されており、環境変数と Docker Compose を使用して簡単にデプロイできます。

---

## 🚀 主な機能

- **`/status` スラッシュコマンド**: 
  - 実行された瞬間のサーバーリソース情報を測定し、Discord に送信します。
  - **管理者限定権限**: デフォルトで管理者（Administrator）のみが実行できるように制限されています。
  - **プライベート返信 (Ephemeral)**: コマンドを実行した本人にのみ結果が表示されるため、チャンネルの他のメンバーにサーバー情報を露出させません。

---

## 🛠️ セットアップと起動手順

### 1. Discord Bot の作成とトークンの取得
1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセスします。
2. **New Application** を作成し、Bot を追加します。
3. **Bot** タブから **Token** を生成（Reset Token）し、手元に控えておきます。
4. **Privileged Gateway Intents** はデフォルトのままで問題ありません（メッセージ本文の読み取り等は不要です）。
5. **OAuth2** -> **URL Generator** から以下のスコープを選択し、生成された URL から Bot をサーバーに招待します。
   - `bot`
   - `applications.commands` (スラッシュコマンド同期用)

### 2. 環境変数の設定
リポジトリルートにある `.env.sample` を `.env` にコピーし、取得した Discord Bot トークンを設定します。

```bash
cp .env.sample .env
```

`.env` ファイルをエディタで開き、以下のようにトークンを設定します。

```env
DISCORD_BOT_TOKEN=ここに取得したBotトークンを貼り付けます
```

### 3. Docker Compose による起動
Docker がインストールされている環境で、以下のコマンドを実行してコンテナをビルド・起動します。

```bash
docker compose up -d --build
```

起動後、Bot が Discord 上でオンラインになり、管理者権限を持つユーザーが `/status` スラッシュコマンドを使用できるようになります。


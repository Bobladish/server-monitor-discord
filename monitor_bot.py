import os
import time
import discord
from discord import app_commands
import psutil

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# 📊 呼び出された瞬間のサーバー状態を取得する関数
def get_immediate_status():
    # CPU (interval=1.0秒でその瞬間の使用率を測定)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    
    # メモリ
    memory = psutil.virtual_memory()
    mem_used_gb = memory.used / (1024 ** 3)
    mem_total_gb = memory.total / (1024 ** 3)
    
    # ディスク (ホストマウント /host があればそちらを、なければ / を監視)
    disk_path = '/host' if os.path.exists('/host') else '/'
    disk = psutil.disk_usage(disk_path)
    disk_used_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)
    
    # 通信帯域 (1秒間の送受信量を計測)
    net_before = psutil.net_io_counters()
    time.sleep(1) # 1秒待つ
    net_after = psutil.net_io_counters()
    
    # バイトからKB（またはMB）に変換
    download_speed = (net_after.bytes_recv - net_before.bytes_recv) / 1024
    upload_speed = (net_after.bytes_sent - net_before.bytes_sent) / 1024
    
    # 表示用のテキストを整形
    report = (
        "📊 **現在のサーバーリソース状態**\n"
        f"🖥️ **CPU使用率**: {cpu_percent}%\n"
        f"🧠 **メモリ使用量**: {mem_used_gb:.2f} GB / {mem_total_gb:.2f} GB ({memory.percent}%)\n"
        f"💾 **ディスク使用量**: {disk_used_gb:.2f} GB / {disk_total_gb:.2f} GB ({disk.percent}%)\n"
        "🌐 **現在のネットワーク通信速度** (直近1秒の計測):\n"
        f"   📥 ダウンロード: {download_speed:.1f} KB/s\n"
        f"   📤 アップロード: {upload_speed:.1f} KB/s"
    )
    return report

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# コマンドの実行制限（管理者だけが実行できるように設定）
@tree.command(name="status", description="サーバーの現在のリソース状態をその場で計測して表示します")
@app_commands.default_permissions(administrator=True) # 管理者権限を持つ人のみ表示可能に
async def status_command(interaction: discord.Interaction):
    # 測定に2秒ほどかかるため、先に「考え中...」のステータスを出す
    await interaction.response.defer(ephemeral=True) 
    
    # ステータスを取得
    status_msg = get_immediate_status()
    
    # 結果を送信（ephemeral=True でコマンドを打った本人にしか見えないようにする）
    await interaction.followup.send(status_msg)

if __name__ == "__main__":
    if TOKEN:
        client.run(TOKEN)
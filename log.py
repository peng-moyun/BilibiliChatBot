import psutil
import time


def list_drives():
    print("可用的盘符:")
    drives = []
    for partition in psutil.disk_partitions():
        drives.append(partition.device)
        print(partition.device)
    return drives


def log_disk_io(drive_letter):
    prev_io_counters = psutil.disk_io_counters(perdisk=True).get(drive_letter)
    if prev_io_counters is None:
        print(f"未找到盘符 {drive_letter}")
        return

    print(f"监视盘符 {drive_letter} 的读写速度...")

    while True:
        io_counters = psutil.disk_io_counters(perdisk=True).get(drive_letter)
        if io_counters is None:
            print(f"未找到盘符 {drive_letter}")
            break

        read_bytes = io_counters.read_bytes - prev_io_counters.read_bytes
        write_bytes = io_counters.write_bytes - prev_io_counters.write_bytes

        # 换算为 MB/s
        read_speed_mb = read_bytes / 1024 / 1024 / 0.1  # 每0.1秒的读速度
        write_speed_mb = write_bytes / 1024 / 1024 / 0.1  # 每0.1秒的写速度

        # 输出结果
        print(f"\r读取速度: {read_speed_mb:.2f} MB/s, 写入速度: {write_speed_mb:.2f} MB/s", end='')

        prev_io_counters = io_counters  # 更新上一个状态
        time.sleep(0.1)  # 每隔0.1秒


if __name__ == "__main__":
    drives = list_drives()  # 列出所有可用盘符
    drive_letter = input("请选择要监视的盘符（如 C: 或 D:）: ").strip()

    # 调试输出，检查用户输入和可用盘符
    print(f"用户输入的盘符: '{drive_letter}'")
    print(f"可用盘符: {drives}")

    # 确保用户输入的格式正确
    # 将用户输入的盘符添加反斜杠以匹配可用盘符的格式
    if drive_letter + "\\" in drives:
        log_disk_io(drive_letter + "\\")
    else:
        print("无效的盘符选择。")

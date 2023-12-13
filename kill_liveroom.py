import psutil

def terminate_process(process_name):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            # print(proc.info['name'])
            if process_name.lower() in proc.info['name'].lower():
                pid = proc.info['pid']
                process = psutil.Process(pid)
                process.terminate()  # 或者使用 process.kill() 来强制终止
                print(f"进程 {process_name} (PID: {pid}) 已被终止.")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 要结束的进程名称，可以是部分匹配
    process_to_terminate = ["DYToolEx.exe", "HuyaClient.exe", "kwaiLive.exe", "PotPlayer", "OBS"]  # 修改为你要结束的进程名称
    for p in process_to_terminate:
        terminate_process(p)
        # break
    # 停止推流
    from change_game import stop
    stop()


# clear_user_message.py

import user_data_manager

def main():
    try:
        uid = int(input("请输入要清除消息计数的用户UID: "))
        user_data_manager.clear_user_message_count(uid)
    except ValueError:
        print("请输入有效的UID (整数)。")

if __name__ == "__main__":
    main()

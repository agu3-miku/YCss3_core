import json
import os
import sys

# 数据文件路径（与脚本文件在同一目录）
DATA_FILE = os.path.join(os.path.dirname(__file__), "storage_data.json")

def create_empty_file_if_not_exists():
    """如果数据文件不存在，则创建一个空的 JSON 文件."""
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"创建数据文件时发生错误: {e}")
            sys.exit(1)

def load_data():
    """加载数据文件中的内容，并返回数据字典."""
    create_empty_file_if_not_exists()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("数据文件格式错误或损坏，已创建新文件。")
        create_empty_file_if_not_exists()
        return {}
    except Exception as e:
        print(f"读取数据文件时发生错误: {e}")
        return {}

def save_data(data):
    """将数据字典保存到数据文件中."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"保存数据文件时发生错误: {e}")

def add_item(room, storage, items_string):
    """添加物品的逻辑处理."""
    if not all([room, storage, items_string]):
        clear_terminal()
        print("请填写所有字段。")
        return

    items = [item.strip() for item in items_string.split(';') if item]
    data = load_data()
    existing_items = data.setdefault(room, {}).setdefault(storage, [])
    duplicates = [item for item in items if item in existing_items]

    if duplicates:
        clear_terminal()
        print(f"已存在以下物品：{', '.join(duplicates)}")
        return  # 用户选择不添加，直接返回

    existing_items.extend(items)
    save_data(data)
    clear_terminal()
    print("物品已成功添加！")

def find_item(search_term):
    """查找物品的逻辑处理."""
    if not search_term:
        clear_terminal()
        print("请输入要查找的物品。")
        return

    data = load_data()
    found_items = {
        room: {storage: items for storage, items in storages.items() if search_term in items}
        for room, storages in data.items()
    }

    if not any(found_items.values()):
        clear_terminal()
        print("未找到任何匹配的物品。")
    else:
        clear_terminal()
        for room, storages in found_items.items():
            for storage, items in storages.items():
                for item in items:
                    print(f"房间: {room}  存储地点: {storage}  物品: {item}")

def show_statistics():
    """统计信息的逻辑处理."""
    data = load_data()
    total_items = sum(len(storage_items) for storages in data.values() for storage_items in storages.values())
    total_rooms = len(data)
    clear_terminal()
    if total_rooms == 0:
        print("当前没有任何数据。")
    else:
        stats_info = f"房间总数: {total_rooms}\n物品总数: {total_items}"
        print(stats_info)

def clear_data():
    """清空数据文件中的所有数据."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4, ensure_ascii=False)
        clear_terminal()
        print("数据已成功清空！")
    except Exception as e:
        clear_terminal()
        print(f"清空数据时发生错误: {e}")

def main_menu():
    """主菜单，提供命令行交互界面."""
    while True:
        clear_terminal()
        print("\n请选择操作：")
        print("1. 添加物品")
        print("2. 查找物品")
        print("3. 查看统计信息")
        print("4. 清空数据")
        print("5. 退出")
        choice = input("请输入选项编号：")

        if choice == "1":
            clear_terminal()
            room = input("请输入房间名称：")
            storage = input("请输入存储地点：")
            items_string = input("请输入物品（用中文分号隔开）：")
            add_item(room, storage, items_string)
        elif choice == "2":
            clear_terminal()
            search_term = input("请输入要查找的物品名称：")
            find_item(search_term)
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            clear_data()
        elif choice == "5":
            clear_terminal()
            print("退出程序。")
            break
        else:
            clear_terminal()
            print("无效选项，请重新选择。")

def clear_terminal():
    """清除终端屏幕."""
    os.system('cls' if os.name == 'nt' else 'clear')

# 调用函数清除终端
clear_terminal()

# 启动主菜单
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        clear_terminal()
        print("\n程序已中断。")
    except Exception as e:
        clear_terminal()
        print(f"程序运行时发生错误: {e}")

# encoding: utf-8
"""
@author:  Ryuk
@contact: jeryuklau@gmail.com
"""

import os
import pathlib


def rename_to_gbk_compatible(root_dir):
    """
    递归遍历目录，将所有文件和文件夹名称的内容从 UTF-8 语义转换为 GBK 兼容语义。

    Args:
        root_dir (str): 要开始遍历的根目录路径。
    """
    root_path = pathlib.Path(root_dir)
    rename_count = 0

    print(f"开始遍历和重命名目录：{root_dir}\n")

    # 1. 递归遍历：使用 topdown=False (自底向上) 确保先重命名子目录中的内容，再重命名父目录
    for root, dirs, files in os.walk(root_dir, topdown=False):

        # 2. 处理文件
        for old_name in files:
            # os.walk 提供的 old_name 已经是 Python 的 Unicode (str)
            old_full_path = pathlib.Path(root) / old_name

            try:
                # 核心转换逻辑
                byte_string = old_name.encode('latin-1')
                new_name = byte_string.decode('utf-8')

                # 构造新的完整路径
                new_full_path = pathlib.Path(root) / new_name

                if old_name != new_name:
                    os.rename(old_full_path, new_full_path)
                    print(f"[文件] 成功: {old_name} -> {new_name} (路径: {root})")
                    rename_count += 1
            except Exception as e:
                print(f"[文件] 失败: 无法重命名 {old_name}。错误: {e}")

        # 3. 处理文件夹
        # 注意：由于我们使用 topdown=False，当前 root 目录下的所有子目录都在 dirs 列表中
        for i in range(len(dirs)):
            old_name = dirs[i]
            old_full_path = pathlib.Path(root) / old_name

            try:
                # 核心转换逻辑
                byte_string = old_name.encode('latin-1')
                new_name = byte_string.decode('utf-8')

                # 构造新的完整路径
                new_full_path = pathlib.Path(root) / new_name

                if old_name != new_name:
                    os.rename(old_full_path, new_full_path)
                    print(f"[文件夹] 成功: {old_name} -> {new_name} (路径: {root})")
                    rename_count += 1

                    # 重要的步骤：更新 dirs 列表，以反映文件夹名称的变化
                    # 尽管 topdown=False 不依赖此列表继续遍历，但保持其准确性是良好的实践
                    dirs[i] = new_name
            except Exception as e:
                print(f"[文件夹] 失败: 无法重命名 {old_name}。错误: {e}")

    print(f"\n--- 批量操作完成，共重命名了 {rename_count} 个文件/文件夹。---")



if __name__ == "__main__":
    # --- 使用示例 ---
    # 替换为你要处理的根目录，请使用原始字符串 r'' 来避免路径转义问题
    TARGET_ROOT = "test/"
    # 请在运行前**备份**你的数据，因为重命名操作不可逆！
    rename_to_gbk_compatible(TARGET_ROOT)
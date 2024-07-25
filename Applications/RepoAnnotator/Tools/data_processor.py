import os

class DataProcessor:

    @staticmethod
    def restructure_files(task_list, file_path_list, old_root, new_root):
        # 创建一个映射，index 到 file_path
        index_to_path = {index: path for index, path in file_path_list}
        
        # 按照 index 排序的 task_list
        sorted_task_list = sorted(task_list, key=lambda x: x[1])
        
        # 用于存储新的文件内容
        file_contents = {}
        
        for task in sorted_task_list:
            _, index = task
            old_file_path = index_to_path[index]
            new_file_path = old_file_path.replace(old_root, new_root)
            
            if new_file_path not in file_contents:
                file_contents[new_file_path] = []
            
            file_contents[new_file_path].append((index, old_file_path))
        
        # 在新根目录下重建文件架构并写入内容
        for new_file_path, contents in file_contents.items():
            # 确保目录存在
            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
            
            # 按照 index 顺序写入内容
            with open(new_file_path, 'w', encoding='utf-8') as f:
                for _, old_file_path in sorted(contents):
                    with open(old_file_path, 'r', encoding='utf-8') as old_file:
                        f.write(old_file.read())
                        f.write('\n')

    @staticmethod
    def transitor(data):
        task_list = [(item['source_code'], item['index']) for item in data if item['source_code']]
        file_path_list = [(item['index'], item['file_path']) for item in data if item['source_code']]
        return task_list, file_path_list
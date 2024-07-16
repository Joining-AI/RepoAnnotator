import ast
import os
import concurrent.futures
import time
from collections import defaultdict
from .code_analyser import CodeAnalyser

class RepoProcessor:
    def __init__(self, processor, service, threshold=4096):
        self.processor = processor
        self.service = service
        self.code_analyser = CodeAnalyser(threshold)

    # 调用模型API进行处理任务
    def task_processor(self, code, retries=3, delay=2):
        """
        Process the code and add Chinese comments.
        Retries up to `retries` times in case of failure, with `delay` seconds between retries.
        """
        prompt = f'''
        请你为我解释下面的代码，逐行中文注释，使得一个十岁小孩也能看懂，并且不许减少一行代码。

        {code}
        '''
        for attempt in range(retries):
            try:
                answer = self.service.ask_once(prompt)
                python_code = self.processor.parse_code(answer)
                return python_code
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        raise Exception("All retry attempts failed。")

    # 单元格式处理
    def process_unit(self, unit):
        try:
            new_code = self.task_processor(unit['source_code'])
            return (unit['file_path'], unit['index'], new_code)
        except Exception as e:
            print(f"Failed to process unit {unit['index']} in file {unit['file_path']}: {e}")
            return (unit['file_path'], unit['index'], None)

    # 主函数
    def process_repo_code(self, root_folder, new_root_folder, threshold=100, max_workers=50, exclude_paths=None):
        if exclude_paths is None:
            exclude_paths = []
        # 将相对路径转为绝对路径，便于后续处理
        exclude_paths = [os.path.abspath(path) for path in exclude_paths]

        code_files = []
        ext_legal_list = ['.py', '.js', '.c', '.java', '.cpp', '.php', '.rb', '.go', '.html']

        for subdir, _, files in os.walk(root_folder):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in ext_legal_list:
                    file_path = os.path.join(subdir, file)
                    # 跳过在exclude_paths中的文件或目录
                    if not any(os.path.abspath(file_path).startswith(excluded) for excluded in exclude_paths):
                        code_files.append(file_path)
        all_units = []
        for file_path in code_files:
            relative_path = os.path.relpath(file_path, root_folder)
            units = self.code_analyser.get_code_units(file_path)
            for unit in units:
                unit['file_path'] = relative_path
                all_units.append(unit)

        # 按文件路径和开始行排序所有单元，以保持顺序
        all_units.sort(key=lambda x: (x['file_path'], x['start_line']))

        if not os.path.exists(new_root_folder):
            os.makedirs(new_root_folder)

        results = []
        total_units = len(all_units)

        def print_progress(finished_units, total_units):
            print(f"Processed {finished_units}/{total_units} units ({(finished_units / total_units) * 100:.2f}%)")

        finished_units = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.process_unit, unit) for unit in all_units]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                finished_units += 1
                print_progress(finished_units, total_units)

        # 按文件路径分组结果
        grouped_results = defaultdict(list)
        for file_path, index, new_code in results:
            grouped_results[file_path].append((index, new_code))

        # 以顺序写入新文件
        for file_path, code_segments in grouped_results.items():
            # 按索引排序代码段
            code_segments.sort(key=lambda x: x[0])
            new_file_path = os.path.join(new_root_folder, file_path)
            new_dir = os.path.dirname(new_file_path)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            last_index = 0
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                for index, new_code in code_segments:
                    if index != last_index + 1:
                        print(f"Warning: Missing code segment between indices {last_index} and {index} in file {file_path}")
                    if new_code is None:
                        print(f"Warning: Code segment at index {index} in file {file_path} is None")
                    else:
                        new_file.write(new_code)
                        new_file.write("\n\n")  # 在单元之间添加额外的空行
                    last_index = index
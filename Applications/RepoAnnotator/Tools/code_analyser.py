import ast
import os
import re

class CodeAnalyser:
    def __init__(self, threshold=4096):
        self.threshold = threshold

    def get_source_segment(self, source, node):
        """获取给定AST节点的源代码片段。"""
        lines = source.splitlines()
        start_line = node.lineno - 1
        end_line = node.end_lineno
        return "\n".join(lines[start_line:end_line])

    def py_analyser(self, source_code, file_path):
        """解析Python代码并提取代码单元。"""
        tree = ast.parse(source_code)
        units = []

        import_unit = []
        last_end_line = 0

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_unit.append(self.get_source_segment(source_code, node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if import_unit:
                    units.append({
                        "index": len(units) + 1,
                        "source_code": "\n".join(import_unit),
                        "file_path": file_path,
                        "start_line": last_end_line + 1,
                        "end_line": node.lineno - 1
                    })
                    import_unit = []
                start_line = node.lineno - 1
                if last_end_line < start_line:
                    units.append({
                        "index": len(units) + 1,
                        "source_code": "\n".join(source_code.splitlines()[last_end_line:start_line]),
                        "file_path": file_path,
                        "start_line": last_end_line + 1,
                        "end_line": start_line
                    })
                units.append({
                    "index": len(units) + 1,
                    "source_code": self.get_source_segment(source_code, node),
                    "file_path": file_path,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                })
                last_end_line = node.end_lineno

        # 添加剩余的import语句
        if import_unit:
            units.append({
                "index": len(units) + 1,
                "source_code": "\n".join(import_unit),
                "file_path": file_path,
                "start_line": last_end_line + 1,
                "end_line": last_end_line + len(import_unit)
            })

        # 添加任何剩余的代码
        if last_end_line < len(source_code.splitlines()):
            units.append({
                "index": len(units) + 1,
                "source_code": "\n".join(source_code.splitlines()[last_end_line:]),
                "file_path": file_path,
                "start_line": last_end_line + 1,
                "end_line": len(source_code.splitlines())
            })

        # 合并单元以确保每个单元至少达到阈值字符长度
        return self.merge_units(units, source_code, file_path)

    def generic_analyser(self, source_code, file_path, patterns):
        """通用代码解析器，用于提取代码单元。"""
        lines = source_code.splitlines()  # 将源代码按行分割
        units = []  # 存储解析后的代码单元

        last_end_line = 0  # 记录上一个单元的结束行号

        def add_unit(start, end):
            """添加一个新的代码单元。"""
            if start < end:
                units.append({
                    "start_line": start + 1,  # 单元的起始行号
                    "end_line": end  # 单元的结束行号
                })

        # 处理关键行
        for pattern in patterns:
            for match in pattern.finditer(source_code):
                start_line = source_code.count('\n', 0, match.start())  # 关键行的起始行号
                end_line = source_code.count('\n', 0, match.end()) + 1  # 关键行的结束行号
                if last_end_line < start_line:
                    add_unit(last_end_line, start_line)  # 添加空白区域作为一个单元
                add_unit(start_line, end_line)  # 添加关键行作为一个单元
                last_end_line = end_line  # 更新上一个单元的结束行号

        if last_end_line < len(lines):
            add_unit(last_end_line, len(lines))  # 添加剩余的代码作为一个单元

        # 合并单元以确保每个单元至少达到阈值字符长度
        return self.merge_units(units, source_code, file_path)

    def merge_units(self, units, source_code, file_path):
        """合并单元以确保每个单元至少达到阈值字符长度。"""
        lines = source_code.splitlines()
        merged_units = []  # 存储合并后的代码单元
        current_unit = []  # 当前合并的单元
        current_start_line = 0  # 当前合并单元的起始行号

        for unit in units:
            if len(current_unit) == 0:
                current_start_line = unit['start_line']  # 初始化当前合并单元的起始行号
                current_unit = lines[unit['start_line'] - 1:unit['end_line']]  # 初始化当前合并单元
            else:
                current_unit.extend(lines[unit['start_line'] - 1:unit['end_line']])  # 扩展当前合并单元

            if len("\n".join(current_unit)) > self.threshold:
                merged_units.append({
                    "index": len(merged_units) + 1,  # 合并单元的索引
                    "start_line": current_start_line,  # 合并单元的起始行号
                    "end_line": unit['start_line'] - 1  # 合并单元的结束行号
                })
                current_unit = lines[unit['start_line'] - 1:unit['end_line']]  # 重置当前合并单元
                current_start_line = unit['start_line']  # 重置当前合并单元的起始行号

        if current_unit:
            merged_units.append({
                "index": len(merged_units) + 1,  # 合并单元的索引
                "start_line": current_start_line,  # 合并单元的起始行号
                "end_line": unit['end_line']  # 合并单元的结束行号
            })

        # 回到源码中获取对应的各单元代码
        final_units = []
        for merged_unit in merged_units:
            final_units.append({
                "index": merged_unit['index'],  # 单元的索引
                "source_code": "\n".join(lines[merged_unit['start_line'] - 1:merged_unit['end_line']]),  # 单元的源代码
                "file_path": file_path,  # 文件路径
                "start_line": merged_unit['start_line'],  # 单元的起始行号
                "end_line": merged_unit['end_line']  # 单元的结束行号
            })

        return final_units

    def c_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*#include\s*[<"].*?[>"]', re.MULTILINE),  # C 语言导入语句的正则表达式
            re.compile(r'^\s*#define\s+\w+\s+.*', re.MULTILINE),  # C 语言宏定义的正则表达式
            re.compile(r'^\s*typedef\s+.*', re.MULTILINE),  # C 语言类型定义的正则表达式
            re.compile(r'^\s*struct\s+\w+\s*{', re.MULTILINE),  # C 语言结构体定义的正则表达式
            re.compile(r'^\s*enum\s+\w+\s*{', re.MULTILINE),  # C 语言枚举定义的正则表达式
            re.compile(r'^\s*union\s+\w+\s*{', re.MULTILINE),  # C 语言联合体定义的正则表达式
            re.compile(r'^\s*\w+\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # C 语言函数定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def js_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*import\s+.*', re.MULTILINE),  # JavaScript 导入语句的正则表达式
            re.compile(r'^\s*export\s+.*', re.MULTILINE),  # JavaScript 导出语句的正则表达式
            re.compile(r'^\s*function\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # JavaScript 函数定义的正则表达式
            re.compile(r'^\s*class\s+\w+\s*{', re.MULTILINE),  # JavaScript 类定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def java_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*import\s+.*', re.MULTILINE),  # Java 导入语句的正则表达式
            re.compile(r'^\s*package\s+.*', re.MULTILINE),  # Java 包声明的正则表达式
            re.compile(r'^\s*public\s+class\s+\w+\s*{', re.MULTILINE),  # Java 类定义的正则表达式
            re.compile(r'^\s*public\s+interface\s+\w+\s*{', re.MULTILINE),  # Java 接口定义的正则表达式
            re.compile(r'^\s*public\s+enum\s+\w+\s*{', re.MULTILINE),  # Java 枚举定义的正则表达式
            re.compile(r'^\s*public\s+.*\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # Java 方法定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def cpp_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*#include\s*[<"].*?[>"]', re.MULTILINE),  # C++ 导入语句的正则表达式
            re.compile(r'^\s*#define\s+\w+\s+.*', re.MULTILINE),  # C++ 宏定义的正则表达式
            re.compile(r'^\s*typedef\s+.*', re.MULTILINE),  # C++ 类型定义的正则表达式
            re.compile(r'^\s*struct\s+\w+\s*{', re.MULTILINE),  # C++ 结构体定义的正则表达式
            re.compile(r'^\s*class\s+\w+\s*{', re.MULTILINE),  # C++ 类定义的正则表达式
            re.compile(r'^\s*enum\s+\w+\s*{', re.MULTILINE),  # C++ 枚举定义的正则表达式
            re.compile(r'^\s*union\s+\w+\s*{', re.MULTILINE),  # C++ 联合体定义的正则表达式
            re.compile(r'^\s*\w+\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # C++ 函数定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def php_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*<\?php', re.MULTILINE),  # PHP 开始标签的正则表达式
            re.compile(r'^\s*namespace\s+.*', re.MULTILINE),  # PHP 命名空间声明的正则表达式
            re.compile(r'^\s*use\s+.*', re.MULTILINE),  # PHP 导入语句的正则表达式
            re.compile(r'^\s*class\s+\w+\s*{', re.MULTILINE),  # PHP 类定义的正则表达式
            re.compile(r'^\s*interface\s+\w+\s*{', re.MULTILINE),  # PHP 接口定义的正则表达式
            re.compile(r'^\s*trait\s+\w+\s*{', re.MULTILINE),  # PHP 特性定义的正则表达式
            re.compile(r'^\s*function\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # PHP 函数定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def ruby_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*require\s+.*', re.MULTILINE),  # Ruby 导入语句的正则表达式
            re.compile(r'^\s*module\s+\w+', re.MULTILINE),  # Ruby 模块定义的正则表达式
            re.compile(r'^\s*class\s+\w+', re.MULTILINE),  # Ruby 类定义的正则表达式
            re.compile(r'^\s*def\s+\w+\s*\(.*?\)', re.MULTILINE),  # Ruby 方法定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def go_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*package\s+.*', re.MULTILINE),  # Go 包声明的正则表达式
            re.compile(r'^\s*import\s+\(.*\)', re.MULTILINE),  # Go 导入语句的正则表达式
            re.compile(r'^\s*type\s+\w+\s+struct\s*{', re.MULTILINE),  # Go 结构体定义的正则表达式
            re.compile(r'^\s*type\s+\w+\s+interface\s*{', re.MULTILINE),  # Go 接口定义的正则表达式
            re.compile(r'^\s*func\s+\w+\s*\(.*?\)\s*{', re.MULTILINE),  # Go 函数定义的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def html_analyser(self, source_code, file_path):
        patterns = [
            re.compile(r'^\s*<!DOCTYPE\s+html>', re.MULTILINE),  # HTML 文档类型声明的正则表达式
            re.compile(r'^\s*<html.*?>', re.MULTILINE),  # HTML html 标签的正则表达式
            re.compile(r'^\s*<head.*?>', re.MULTILINE),  # HTML head 标签的正则表达式
            re.compile(r'^\s*<body.*?>', re.MULTILINE),  # HTML body 标签的正则表达式
            re.compile(r'^\s*<script.*?>', re.MULTILINE),  # HTML script 标签的正则表达式
            re.compile(r'^\s*<style.*?>', re.MULTILINE),  # HTML style 标签的正则表达式
        ]
        return self.generic_analyser(source_code, file_path, patterns)

    def get_code_units(self, file_path):
        """获取文件的代码单元。"""
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()

        analyzers = {
            '.py': self.py_analyser,
            '.js': self.js_analyser,
            '.c': self.c_analyser,
            '.java': self.java_analyser,
            '.cpp': self.cpp_analyser,
            '.php': self.php_analyser,
            '.rb': self.ruby_analyser,
            '.go': self.go_analyser,
            '.html': self.html_analyser
        }

        file_extension = os.path.splitext(file_path)[1]
        analyser = analyzers.get(file_extension)

        if analyser:
            return analyser(source_code, file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return []

    def get_units(self, root_folder, exclude_paths=None):
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
            units = self.get_code_units(file_path)
            for unit in units:
                unit['file_path'] = relative_path
                all_units.append(unit)
                
        return all_units

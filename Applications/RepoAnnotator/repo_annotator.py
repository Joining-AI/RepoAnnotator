import os
import sys

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Packages.LLM_API import LLMLoader
from Packages.LLM_Parser import LLMParser
from Packages.Multi_Process import MultiProcessor

from Applications.RepoAnnotator.Tools import DataProcessor
from Applications.RepoAnnotator.Tools import CodeAnalyser
from Applications.RepoAnnotator.Config.code_annotator import data_template, prompt, correction, validation

class RepoAnnotator:

    @staticmethod
    def run(root_folder, exclude_list, new_root_folder, service_type='qwen', threshold=64, num_threads=50):
        # 初始化LLM API
        loader = LLMLoader(service_type=service_type)
        llm = loader.service
        parser = LLMParser()

        analyser = CodeAnalyser(threshold=threshold)
        unit_list = analyser.get_units(root_folder, exclude_paths=exclude_list)
        task_list, file_path_list = DataProcessor.transitor(unit_list)

        code_annotator = MultiProcessor(llm, parser.parse_pads, data_template, prompt, correction, validation)
        task_list = code_annotator.multitask_perform(task_list, num_threads)

        DataProcessor.restructure_files(task_list, file_path_list, root_folder, new_root_folder)

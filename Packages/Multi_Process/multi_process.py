import threading
import time
import random
from queue import Queue
from tqdm import tqdm

class MultiProcessor:

    def __init__(self, llm, parse_method, data_template, prompt_template, correction_template, validator):
        self.llm = llm
        self.parse_method = parse_method
        self.data_template = data_template
        self.prompt_template = prompt_template
        self.correction_template = correction_template
        self.validator = validator

    def generate_prompt(self, **kwargs):
        kwargs['data_template'] = self.data_template
        return self.prompt_template.format(**kwargs)

    def generate_correction_prompt(self, answer):
        return self.correction_template.format(answer=answer, data_template=self.data_template)

    def task_perform(self, **kwargs):
        try:
            prompt = self.generate_prompt(**kwargs)
            answer = self.llm.ask(prompt)
            structured_data = self.parse_method(answer)
            return structured_data
        except Exception as e:
            print(f"Error in task_perform: {str(e)}")
            return None

    def correct_data(self, answer):
        correction_prompt = self.generate_correction_prompt(answer)
        correction = self.llm.ask(correction_prompt)
        return correction

    def process_tuple(self, input_tuple):
        input_data = input_tuple[:-1]
        index = input_tuple[-1]
        attempts = 0
        base_wait_time = 1  # 初始等待时间

        while attempts < 3:
            try:
                input_dict = {f'input_{i+1}': input_data[i] for i in range(len(input_data))}
                structured_data = self.task_perform(**input_dict)
                if self.validator(structured_data):
                    return (structured_data, index)
                corrected_answer = self.correct_data(structured_data)
                if corrected_answer and self.validator(corrected_answer):
                    return (corrected_answer, index)
                break
            except Exception as e:
                if 'Throttling.RateQuota' in str(e):
                    wait_time = base_wait_time * (2 ** attempts) + random.uniform(0, 1)
                    print(f"Rate limit exceeded. Retrying in {wait_time:.2f} seconds. Attempt {attempts + 1}/3")
                    time.sleep(wait_time)
                    attempts += 1
                else:
                    print(f"An error occurred: {str(e)}. Attempt {attempts + 1}/3")
                    attempts += 1

        return (None, index)

    def multitask_perform(self, tuple_list, num_threads):
        results = [None] * len(tuple_list)
        queue = Queue()

        for idx, input_tuple in enumerate(tuple_list):
            queue.put((input_tuple, idx))

        def worker(pbar):
            while not queue.empty():
                input_tuple, idx = queue.get()
                result = None
                thread = threading.Thread(target=lambda q, arg1: q.put(self.process_tuple(arg1)), args=(queue, input_tuple))
                thread.start()
                thread.join(timeout=100)  # 设置单线程100s超时
                if thread.is_alive():
                    print(f"Thread processing {input_tuple} timed out.")
                    thread.join()
                else:
                    result = queue.get()
                results[idx] = result
                queue.task_done()
                pbar.update(1)

        with tqdm(total=len(tuple_list)) as pbar:
            threads = []
            for _ in range(min(num_threads, len(tuple_list))):
                thread = threading.Thread(target=worker, args=(pbar,))
                threads.append(thread)
                thread.start()

            queue.join()

            for thread in threads:
                thread.join()

        return results

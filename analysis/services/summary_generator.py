from django.db.backends.utils import logger
from g4f.client import Client


class SummaryGenerator:
    def __init__(self, tasks, prompt):
        self._tasks = tasks
        self._prompt = prompt
        self._request_text = f"""\n\nMain purpose of creating this request is to help user to understand his tasks. 
                                {" User personal purpose is described by him as " + self._tasks[0].project.user.description if self._tasks[0].project.user.description else "No description provided"};\n\n
                                TASKS:\n\n"""
        self._structure_tasks()
        self._prompt += self._request_text

    def _structure_tasks(self):
        for task in self._tasks:
            structured_task = {
                "name": task.name,
                "description": task.description if task.description else 'No description',
                "comments": '\n'.join(task.comments.values_list('text', flat=True)) if task.comments.values_list('text',
                                                                                                                 flat=True) else 'No comments',
                "start_datetime": task.start_datetime,
                "due_datetime": task.due_datetime,
                "complete_percentage": task.progress.percentage,
                "progress_updated": task.progress.updated_datetime,
                "status": task.is_completed,
            }
            self._request_text += (f"Task: {structured_task['name']}\n"
                                   f"Description: {structured_task['description']}\n"
                                   f"Status: {structured_task['status']}\nComplete percentage: {structured_task['complete_percentage']}\n"
                                   f"Start date and time:  {structured_task['start_datetime']}\n"
                                   f"Due date and time: {structured_task['due_datetime']}\n"
                                   f"Updated date and time: {structured_task['progress_updated']}\n"
                                   f"Comments: {structured_task['comments']}\n\n")

    def generate_summary(self):
        client = Client()

        models = ("deepseek-r1-turbo", "deepseek-r1", "qvq-72b",
                  "qwq-32b-arliai", "qwq-32b-preview", "qwq-32b", "qwen-3-0.6b", "qwen-3-1.7b", "qwen-3-4b",
                  "qwen-3-14b")
        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": self._prompt}],
                    web_search=False,
                )
                logger.info(f"Model: {model}")
                message = response.choices[0].message.content
                if "</think>" in message:
                    message = message.split("</think>")[1]
                return message
            except Exception as e:
                logger.warning(f"Error with model {model}, error: {e}")
                continue

from g4f.client import Client


def structure_tasks(tasks):
    structured_tasks = []
    request_in_string = f'Main purpose of creating this request is to help user to understand his tasks. {" User personal purpose is described by him as " + tasks[0].user.description if tasks[0].user.description else "No description provided"};\n\n'
    request_in_string += 'TASKS:\n\n'
    for task in tasks:
        structured_task = {
            "name": task.name,
            "description": task.description if task.description else 'No description',
            "comments": '\n'.join(task.comments.values_list('text', flat=True)) if task.comments.values_list('text', flat=True) else 'No comments',
            "start_time": task.start_time,
            "start_date": task.start_date,
            "due_time": task.due_time,
            "due_date": task.due_date,
            "status": "Completed" if task.is_completed else "In Progress",
            "complete_percentage": task.complete_percentage,
            "completed_datetime":  task.complete_datetime if task.is_completed else "Task is not complete"
        }
        structured_tasks.append(structured_task)
    for task in structured_tasks:
        request_in_string += f"Task: {task['name']}\nDescription: {task['description']}\nStatus: {task['status']}\nComplete percentage: {task['complete_percentage']}\nStart date and time:  {task['start_date']} {task['start_time']}\nDue date and time: {task['due_date']} {task['due_time']}\nComplete date and time: {task['completed_datetime']}\nComments: {task['comments']}\n\n"
    return request_in_string


def generate_analysis(content):
    client = Client()
    main_prompt = """
    You are a professional productivity analyst and self-organization mentor. Analyze a list of tasks including titles, descriptions, completion statuses, and comments. Based on this, generate a motivational and structured summary. Do not analyze each task individually — instead, provide an overall assessment focused on praise and suggestions for improving self-organization.
    
    Structure the output as follows:
    [1. Overall Productivity and Dynamics] — general evaluation of activity, volume, and quality of execution.
    [2. Strengths and Successes] — what worked well and what skills were demonstrated.
    [3. Areas for Growth] — what can be optimized going forward, patterns, and recommendations.
    [4. Recommendations for Self-Organization] — techniques, tools, and practical tips.
    [5. Motivational Conclusion] — praise, positive feedback, and encouragement.
    
    Tone — professional, inspiring, and friendly. The goal is to motivate, highlight progress, and offer useful advice for improving personal productivity.
    \n\n\n"""

    models = ("deepseek-r1-turbo", "deepseek-r1", "qvq-72b",
              "qwq-32b-arliai", "qwq-32b-preview", "qwq-32b", "qwen-3-0.6b", "qwen-3-1.7b", "qwen-3-4b", "qwen-3-14b")
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": main_prompt + content}],
                web_search=False
            )
            print(f"Model: {model}")
            message = response.choices[0].message.content
            if "</think>" in message:
                message = message.split("</think>")[1]
            return message
        except:
            print(f"Error with model {model}")
            continue

from analysis.management.commands._base_make_summary import BaseMakeSummaryCommand


class Command(BaseMakeSummaryCommand):
    def __init__(self):
        prompt = """
    You are a professional productivity analyst and self-organization mentor. Analyze a list of tasks including titles, descriptions, completion statuses, and comments. Based on this, generate a motivational and structured summary. Do not analyze each task individually — instead, provide an overall assessment focused on praise and suggestions for improving self-organization.

    Structure the output as follows:
    [1. Day tasks] — general evaluation of activity, volume, and quality of execution.
    [2. Day progress] — what worked well and what skills were demonstrated.
    [3. Day shortcoming] — what could be better.
    [4. Summary] — praise, positive feedback, and encouragement.

    Tone — professional, inspiring, and friendly. The goal is to motivate, highlight progress, and offer useful advice for improving personal productivity.
    \n\n\n"""
        days = 1
        super().__init__(prompt, days)

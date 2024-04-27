from google.oauth2.service_account import Credentials
import gspread
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


class Client:
    def __init__(self,
                 spreadsheet_url,
                 json_path="env/auth.json"):

        credentials = Credentials.from_service_account_file(
            json_path,
            scopes=scopes,
        )

        gc = gspread.authorize(credentials)

        self.sheet = gc.open_by_url(spreadsheet_url).sheet1

    def get_q_and_a(self):
        values = self.sheet.get_all_values()

        questions = []
        answers = []
        instructios = []
        for records in values:
            questions.append(records[0])
            instructios.append("")
            if len(records) > 1:
                answers.append(records[1])
            else:
                answers.append("")

        self.questions = questions
        self.answers = answers
        self.instructios = instructios
        self.values = values
        return questions, answers

    def get_unanswered_question(self):
        self.get_q_and_a()

        for id, (q, a, inst) in enumerate(zip(self.questions, self.answers, self.instructios)):
            if a == "":
                return id+1, q, inst

        return -1, "", ""

    def answer(self, row_id, answer1, answer2, metainfo="meta"):
        self.sheet.update(f'B{row_id}', [[answer1]])
        self.sheet.update(f'C{row_id}', [[answer2]])
        self.sheet.update(f'E{row_id}', [[metainfo]])

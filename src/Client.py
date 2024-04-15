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
        values=self.sheet.get_all_values()

        questions=[]
        answers=[]
        for records in values:
            questions.append(records[0])
            if len(records)>1:
                answers.append(records[1])
            else:
                answers.append("")

        self.questions=questions
        self.answers=answers
        return questions,answers

    def get_unanswered_question(self):
        for id,(q,a) in enumerate(zip(self.questions,self.answers)):
            if a=="":
                break

        return id+1,q
    
    def answer(self,row_id,answer):
        self.sheet.update(f'B{row_id}', [[answer]])
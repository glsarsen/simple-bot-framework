from datetime import datetime

import gspread

from simplebot.user import User


class google_sheets_writer:
    def __init__(self):
        gc = gspread.service_account(filename="proud-coral-353408-7f43e6396c24.json")
        self.spreadsheet = gc.open_by_key(
            "1JEv29lEp3nXdE6l5gONynn5EvuUTD14kRXPUyynnJdA"
        )

    def save_user_to_gsheets(self, user: User):
        worksheet = self.spreadsheet.get_worksheet(0)
        user_cell = worksheet.find(user.viber_id, in_column=1)
        if user_cell:
            worksheet.update(
                f"A{user_cell.row}:I{user_cell.row}",
                [
                    [
                        user.viber_id,
                        user.login,
                        user.phone,
                        user.name,
                        user.google_login,
                        user.google_password,
                        user.linkedin_login,
                        user.linkedin_password,
                        user.discord_login,
                    ]
                ],
            )
        else:
            worksheet.append_row(
                values=[
                    user.viber_id,
                    user.login,
                    user.phone,
                    user.name,
                    user.google_login,
                    user.google_password,
                    user.linkedin_login,
                    user.linkedin_password,
                    user.discord_login,
                ]
            )

    def save_feedback_to_gsheets(self, user: User, feedback: str):
        worksheet = self.spreadsheet.get_worksheet(1)
        format = "%Y-%m-%d %H:%M:%S"
        worksheet.append_row(
            values=[
                datetime.today().strftime(format),
                user.name,
                "",  # TODO: add user step
                feedback,
            ]
        )

from googleapiclient.discovery import build
from sheets_auth.sheets_autorization import autentication
from googleapiclient.errors import HttpError
from datos import datos
from vars import vars
import vars.spreadsheets_reqs as srqsts
import sys


class Services:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.service = build("sheets", "v4", credentials=autentication())

    def get_spreadsheet(self):
        spreadsheet_dict = self.service.spreadsheets()\
            .get(spreadsheetId=self.spreadsheet_id).execute()
        datos.spreadsheet_dict = spreadsheet_dict
        return spreadsheet_dict

    def set_sheets_id_dict(self):
        sheets = datos.spreadsheet_dict["sheets"]
        for sheet in sheets:
            datos.sheets_id[sheet["properties"]["title"]] = sheet["properties"]["sheetId"]

    def check_sheet_confs(self):
        sheets = datos.spreadsheet_dict["sheets"]
        sheets_names = []
        for sheet in sheets:
            sheets_names.append(sheet["properties"]["title"])
        if "CONFIGURACION JOBS" in sheets_names:
            self.get_confs_sheet()
            return True
        else:
            print("\n- Debe existir una hoja con nombre:\n" +\
                "CONFIGURACION JOBS")
            input("- Esperando la hoja...\n(Enter para volver a intentarlo)\n")
            set_spreadsheet()
            self.check_sheet_confs()

    def set_columns(self):
        for sheet in self.get_spreadsheet()["sheets"]:
            if sheet["properties"]["title"] == "CONFIGURACION JOBS":
                srqsts.reqs.append(srqsts.format_columns(sheet["properties"]["sheetId"]))
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=srqsts.body_reqs(srqsts.reqs)
        ).execute()
        srqsts.reqs = []

    def get_confs_sheet(self):
        res = self.service.spreadsheets().values().get(
            spreadsheetId = self.spreadsheet_id,
            range = "CONFIGURACION JOBS!A2:A"
        ).execute()
        if "values" not in res.keys():
            print("No hay jobs indicados en la hoja")
            sys.exit()
        else:
            datos.jobs_in_sheet = res["values"] # Se tienen que dividir en 50
            datos.total_jobs = len(res["values"])

    def insert_data(self, i_row, pre_data):
        data = pre_data[1:]
        res = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId = self.spreadsheet_id,
            body=srqsts.insert_data(data, i_row) ## data tiene que ser una lista de listas
                                                 ## cada sublista debe tener un valor para la celda
        ).execute()
        return res


def set_spreadsheet():
    vars.SPREADSHEET_ID = input("- Ingrese el spreadsheetID:\n")
    try:
        sheets = Services(vars.SPREADSHEET_ID)
        sheets.get_spreadsheet()
        sheets.set_sheets_id_dict()
        return sheets
    except HttpError as err:
        if err.resp["status"] == "404":
            print("- No se encontro el spreadsheet")
        return set_spreadsheet()
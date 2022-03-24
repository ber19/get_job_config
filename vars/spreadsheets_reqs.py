###############
reqs = []
def body_reqs(reqs):
    return {
        "requests": reqs
    }
################
def format_columns(sheet_id):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 1,
                "endColumnIndex": 33
            },
            "cell": {
                "userEnteredFormat":{
                    "backgroundColor":{
                        "red": 0.0,
                        "green": 0.0,
                        "blue": 0.0
                    },
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                        "foregroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                        },
                        "fontSize": 8,
                        "bold": True
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor, textFormat, horizontalAlignment)"
        }
    }

def insert_data(data, i_row):
    return {
        "value_input_option": "USER_ENTERED",
        "data": [
            {
                "range": "CONFIGURACION JOBS!B{}".format(
                    i_row + 2 # Por el comienzo en 1 y las columnas en la hoja
                ),
                "majorDimension": "COLUMNS",
                "values": 
                    data    ## tiene que se una lista de listas, cada sublista
                            ## debe tener un valor para la celda
            }
        ]
    }
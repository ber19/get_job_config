from os import stat
from datos import datos


def get_data():
    for jobname, list_of_str in datos.datos_jobs.items():
        total_data = list_of_str[:29] # son los datos que siempre estaran
                                        # no se toma en cuenta al 29
                                        # len(total_data)  -> 28
        if list_of_str:
            for i in range(0,29):  # Para limpiar los saltos de linea
                total_data[i] = total_data[i].replace("\n", "")

            count = 29  # RECURSOS -> Recurso cuantitativo y cantidad
                        # llevara el indice para recorrer la lista

            recursos = [] 
            for str in list_of_str[count:]: # toma en cuenta al count (29 en esta linea)
                count += 1
                if "QuantCantidad" in str:
                    continue
                if "CondicionTipoEfecto" in str:
                    break
                else:
                    recursos.append(str)
            recs = []
            if len(recursos) == 0:
                pass
            else:
                for i in range(len(recursos)):
                    if recursos[i].isnumeric():
                        recs.append((recursos[i-1],recursos[i]))
            total_data.append(recs)  ## Al total_data

            conditions = []
            for str in list_of_str[count:]:
                count += 1
                if "CondicionTipoEfecto" in str:
                    continue
                if "OK" in str and "NOTOK" in str:
                    break
                else:
                    conditions.append(str)
            conds = []
            if len(conditions) == 0:
                pass
            else:
                for i in range(len(conditions)):
                    if conditions[i] == "INCOND":
                        conds.append(("INCOND", conditions[i-1]))
                    if conditions[i].strip() == "-":
                        conds.append(("OUTCOND", "-", conditions[i-2]))
                    if conditions[i].strip() == "+":
                        conds.append(("OUTCOND", "+", conditions[i-2]))
            total_data.append(conds)  ## Al total_data

            alerts = []
            for str in list_of_str[count:]:
                count += 1
                if "OK" in str and "NOTOK" in str:
                    continue
                if "Envia MAIL" in str:
                    alerts.append(str)
            alrts = []
            if len(alerts) == 0:
                pass
            else:
                for i in range(len(alerts)):
                    if i == 0:
                        alrts.append(("OK", alerts[i]))
                    elif i == 1:
                        alrts.append(("NOTOK", alerts[i]))
                    else:
                        alrts.append(("", alerts[i])) # Por si son alertas de 
                                                    # otro tipo que no conozco
            total_data.append(alrts)   ## Al total_data
        else: pass

        datos.datos_jobs[jobname] = total_data

def str_to_list(val):
    if isinstance(val, str):
        return [val]
    if isinstance(val, list):
        if val and not isinstance(val[0], str):
            res = ""
            for i_tup in range(len(val)):   ## Indice de tupla en la lista
                if val[i_tup] == val[-1]:  ## Si es la ultima tupla en la lista
                    for i in range(len(val[i_tup])):   ## Indice de string en la tupla
                        if val[i_tup][i].isnumeric():
                            res += "{}, {}".format(val[i_tup][i-1], val[i_tup][i])
                        if "-TO-" in val[i_tup][i] and len(val[i_tup]) == 3:
                            res += "{}, {}, {}".format(val[i_tup][i-2], val[i_tup][i-1], val[i_tup][i])
                        if "-TO-" in val[i_tup][i] and len(val[i_tup]) == 2:
                            res += "{}, {}".format(val[i_tup][i-1], val[i_tup][i])
                        if "_TR" in val[i_tup][i] and len(val[i_tup]) == 3:
                            res += "{}, {}, {}".format(val[i_tup][i-2], val[i_tup][i-1], val[i_tup][i])
                        if "_TR" in val[i_tup][i] and len(val[i_tup]) == 2:
                            res += "{}, {}".format(val[i_tup][i-1], val[i_tup][i])
                        if " MAIL a " in val[i_tup][i]:
                            res += "{}, {}".format(val[i_tup][i-1], val[i_tup][i])
                if val[i_tup] != val[-1]:  ## Si no es la ultima tupla en la lista
                    for i in range(len(val[i_tup])):
                        if val[i_tup][i].isnumeric():
                            res += "{}, {}\n".format(val[i_tup][i-1], val[i_tup][i])
                        if "-TO-" in val[i_tup][i] and len(val[i_tup]) == 3:
                            res += "{}, {}, {}\n".format(val[i_tup][i-2], val[i_tup][i-1], val[i_tup][i])
                        if "-TO-" in val[i_tup][i] and len(val[i_tup]) == 2:
                            res += "{}, {}\n".format(val[i_tup][i-1], val[i_tup][i])
                        if "_TR" in val[i_tup][i] and len(val[i_tup]) == 3:
                            res += "{}, {}, {}\n".format(val[i_tup][i-2], val[i_tup][i-1], val[i_tup][i])
                        if "_TR" in val[i_tup][i] and len(val[i_tup]) == 2:
                            res += "{}, {}\n".format(val[i_tup][i-1], val[i_tup][i])
                        if " MAIL a " in val[i_tup][i]:
                            res += "{}, {}\n".format(val[i_tup][i-1], val[i_tup][i])
            return [res]
        else: return val
def insert_conf(sheets, start, end): 
    for i in range(start, end):
        job_str = list(datos.datos_jobs.keys())[i-start]
        data_s = datos.datos_jobs[job_str]  ## Se trabaja con datos_jobs por la compatibilidad
                                            ## con el api de las spreadsheets (lista de strings)
        if data_s:
            sheets.insert_data(i, list(map(str_to_list, data_s))) ## El list() es una lista de listas de un solo string
        else: continue




spreadsheet_dict = None
sheets_id = {}
jobs_in_sheet = None ## Lista de listas de un solo string ("el valor")
                     ## si no hay valor indicado en la celda, es una lista de la lista principal, vacia

datos_jobs = {} ## Cada key es un jobname(str), cada value son los datos de la consulta (lista de strings y listas)
                ## values pueden ser listas vacias

dfs_confs = {}  # Cada key es un jobname(str), cada value son los datos de la consulta (pandas Serie)

total_jobs = 0
conteo = 0
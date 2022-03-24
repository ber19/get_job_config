import pandas as pd
import datos.datos as datos
import vars.vars as vars

def set_dfs_c():
    for job, data in datos.datos_jobs.items(): 
        if data:
            datos.dfs_confs[job] = pd.DataFrame( ## Cada value es un pandas DataFrame
                [data],
                columns = vars.COLUMNS[0]
            )
        else:
            datos.dfs_confs[job] = pd.DataFrame(
                [[]]
            )
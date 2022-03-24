from ops.clean_scrap import clean_mei, clean_drag, clean_scoped
import traceback
from ops.sheets_services import set_spreadsheet
from vars import vars
from datos import datos
from scraping.scheduling_scraping import main_data as main_get_data
from ops.data_ops import get_data, insert_conf
from ops.set_dfs import set_dfs_c

def main():
    try:
        clean_mei()
        clean_drag()
        try:
            clean_scoped()
        except PermissionError as err:
            pass
        sheets = set_spreadsheet()
        # sheets.set_columns()  ## Mejor proteger las columnas desde el drive
        sheets.get_confs_sheet()
        if datos.total_jobs % 50 != 0 and datos.total_jobs > 50:
            residuo = datos.total_jobs % 50
            for i in range(50, datos.total_jobs+1, 50):                
                main_get_data(datos.jobs_in_sheet[datos.conteo:i])
                get_data()
                set_dfs_c()
                insert_conf(
                    sheets,
                    datos.conteo,
                    i
                )
                datos.conteo = i
                datos.datos_jobs = {}
            main_get_data(datos.jobs_in_sheet[datos.conteo:datos.conteo+residuo])
            get_data()
            set_dfs_c()
            insert_conf(
                sheets,
                datos.conteo,
                datos.conteo+residuo
            )
        elif datos.total_jobs % 50 == 0 and datos.total_jobs > 50:
            for i in range(50, datos.total_jobs+1, 50):
                main_get_data(datos.jobs_in_sheet[datos.conteo:i])
                get_data()
                set_dfs_c()
                insert_conf(
                    sheets,
                    datos.conteo,
                    i
                )
                datos.conteo = i
                datos.datos_jobs = {}
        else:
            main_get_data(datos.jobs_in_sheet)
            get_data()
            set_dfs_c()
            insert_conf(
                sheets,
                datos.conteo,
                len(datos.jobs_in_sheet)
            )
    except Exception as err:
        if vars.selenium_driver:
            vars.selenium_driver.quit()
        print("- Error inesperado.\n- Info:\n", err,
        "\n- Cerrando ...")
        traceback.print_exc() ## Comentar en producción
    except KeyboardInterrupt:
        if vars.selenium_driver:
            vars.selenium_driver.quit()
        print("- Ejecución interrumpida")

if __name__ == "__main__":
    main()
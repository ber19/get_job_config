

PATH_DRIVER = "C:\\Users\\mi11878\\chromedriver.exe"

URL_CONFIGURACION = "http://150.100.216.64:8080/scheduling/planificaciones"

VALUE_INPUT_OPTION = "USER_ENTERED"

COLUMNS = [[
    "No.","JOBNAME", "FOLDER", "USERDAILY", "APPLICATION", "SUB-APPLICATION", "DESCRIPTION",
    "TASKTYPE", "SCRIPT", "PATH", "COMMAND", "HOST", "RUN AS", "CYCLIC", "KEEP ACTIVE",
    "DAYSCAL", "DAYS", "WEEKSCAL", "WEEKSDAYS", "AUTOR", "TIMEFROM", "TIMETO", "ACTIVEFROM", "ACTIVETILL",
    "JOBTYPE", "TIMEZONE", "CONFCAL", "APX/DAAS JOB", "APX/DAAS BODY", "RECURSOS", "CONDITIONS", "STEPS"
]]
## RECURSOS tiene una subtabla con Recurso Quant y Cantidad
## CONDITIONS tiene una subtabla con Condicion Tipo y Efecto
## STEPS tiene dos subtablas NOTOK y OK 


selenium_driver = None
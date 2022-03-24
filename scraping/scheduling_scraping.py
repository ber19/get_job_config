from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from vars import vars
from datos import datos


def main_data(jobs_in_sheet):
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--headless")
        options.add_argument("--window-size=1280x720")
        vars.selenium_driver = webdriver.Chrome(executable_path=vars.PATH_DRIVER, options=options)
        vars.selenium_driver.get(vars.URL_CONFIGURACION)
        for i in range(len(jobs_in_sheet)):
            if jobs_in_sheet[i]:   ## Si la celda no esta vacia         
                job = jobs_in_sheet[i][0] # string
            else:
                job = ""
            datos.datos_jobs[job] = config(job, vars.selenium_driver)
            vars.selenium_driver.refresh()
        vars.selenium_driver.quit()
        vars.selenium_driver = None
    except WebDriverException:
        print("- Se cerro el proceo del navegador")


def config(job, driver):
    data = []
    if job == "": return data
    jobname = driver.find_element_by_id("jobname")
    jobname.clear()
    jobname.send_keys(job)
    submit = driver.find_element_by_id("Consultar")
    submit.click()
    driver.implicitly_wait(3)
    if driver.find_elements_by_xpath("//div[text()='No hay registros']"):
        return data
    driver.implicitly_wait(177)
    if driver.find_elements_by_xpath("//table[@id='tblEjec']/tbody/tr"):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", attrs={"id":"tblEjec"})
        for row in table.find_all("tr")[1:]:
            data.append([value.getText() for value in row.find_all("td")])
        # return data
        for vals_list in data:
            if len(vals_list) >= 28 and vals_list[3] != "EVENTUAL":
                return vals_list
        
        
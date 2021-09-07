import requests
from bs4 import BeautifulSoup
import json

class FloorSheetClass():
    def floorsheet():
        page = requests.get("https://merolagani.com/Floorsheet.aspx")
        soup = BeautifulSoup(page.text,'lxml')

        table = soup.find('table',class_="table table-bordered table-striped table-hover sortable")

        headers = [heading.text.replace("\n" ,"") for heading in table.find_all('th')]

        tbody = soup.find("tbody")
        table_row = [row for row in tbody.find_all("tr")]

        result=[{headers[index]:cell.text.replace("\n","") for index, cell in enumerate(row.find_all("td"))} for row in table_row]

        # for dump json
        resultJson = json.dumps(result)
        return resultJson
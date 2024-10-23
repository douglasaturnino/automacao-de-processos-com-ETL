import json
import sqlite3
import pandas as pd
from glob import glob
from lxml import etree
from datetime import datetime
import os

PATH = os.getcwd() + "/var/logs/rundeck/PROD/job"


def get_logs() -> pd.DataFrame:
    projects = glob(PATH + "/*")

    df = pd.DataFrame()
    for project_path in projects:
        projects_id = project_path.split("/")[-1]

        projects_json_logs_paths = glob(project_path + "/logs/*.json")
        projects_xml_logs_paths = glob(project_path + "/logs/*.xml")

        dfjson = pd.concat(
            [
                pd.DataFrame.from_dict(json.load(open(path)), orient="index").T
                for path in projects_json_logs_paths
            ]
        )

        dfjson.reset_index(drop=True, inplace=True)
        dfjson["projectID"] = projects_id

        xmls = []
        for path in projects_xml_logs_paths:
            elements = list(etree.parse(path).getroot().find("execution"))
            xmls.append({element.tag: element.text for element in elements})

        dfxml = pd.DataFrame(xmls).rename(columns={"execIdForLogStore": "executionId"})
        dfxml.reset_index(drop=True, inplace=True)
        dfxml["executionId"] = dfxml["executionId"].str.strip().astype(int)

        df = pd.concat(
            [df, dfjson.merge(dfxml, on=["executionId"], how="inner")], axis=0
        )

    df.reset_index(drop=True, inplace=True)
    df["extractionDate"] = datetime.now()

    return df


if __name__ == "__main__":
    df = get_logs()

    conexao = sqlite3.connect("imdb_data.db")

    df.drop(columns=["nodes", "steps", "targetNodes", "allNodes"], axis=1).to_sql(
        "logs", con=conexao
    )

    conexao.close()

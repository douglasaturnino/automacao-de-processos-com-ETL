# IMPORTS
import logging
import os
import sqlite3

from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader
from src.view import ViewCreator
from src.config.config import config

# Configuração do logging
log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Adicione um manipulador de arquivo ao logger
log_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "script_logs.log"
)
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

if __name__ == "__main__":
    extractor = DataExtractor()
    extractor.extract()

    transformer = DataTransformer()
    transformer.transform()

    with sqlite3.connect(config.BANCO_DADOS) as conexao:
        loader = DataLoader(conexao)
        loader.load()

        view_creator = ViewCreator(conexao)
        view_creator.create_views()

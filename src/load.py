import logging
import os

import pandas as pd

from src.config.config import config


class DataLoader:
    def __init__(self, conexao):
        self.conexao = conexao
        self.diretorio_tratados = os.path.join(config.DIRETORIO_DADOS, "tratados")

    def load(self):
        arquivos = os.listdir(self.diretorio_tratados)

        for arquivo in arquivos:
            self.load_file(arquivo)

        logging.info("Todos os arquivos foram salvos no banco de dados.")

    def load_file(self, arquivo):
        caminho_arquivo = os.path.join(self.diretorio_tratados, arquivo)

        if os.path.isfile(caminho_arquivo) and arquivo.endswith(".tsv"):
            df = pd.read_csv(caminho_arquivo, sep="\t", low_memory=False)
            nome_tabela = self.format_table_name(arquivo)

            df.to_sql(nome_tabela, self.conexao, index=False, if_exists="replace")
            logging.info(
                f"Arquivo {arquivo} salvo como tabela {nome_tabela} no banco de dados."
            )
            os.remove(caminho_arquivo)

    @staticmethod
    def format_table_name(arquivo):
        return os.path.splitext(arquivo)[0].replace(".", "_").replace("-", "_")

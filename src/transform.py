import logging
import os

import pandas as pd

from src.config.config import config


class DataTransformer:
    def __init__(
        self,
        arquivos: list = config.ARQUIVOS,
        diretorio_dados: str = config.DIRETORIO_DADOS,
    ):
        self.arquivos = arquivos
        self.diretorio_dados = diretorio_dados
        self.diretorio_tratados = os.path.join(self.diretorio_dados, "tratados")

    def transform(self, chunksize=1_000_000):
        os.makedirs(self.diretorio_tratados, exist_ok=True)

        for arquivo in self.arquivos:
            self.process_file(arquivo, chunksize)

        logging.info(
            "Todos os arquivos foram tratados e salvos no diretório 'tratados'."
        )

    def process_file(self, arquivo, chunksize):
        caminho_arquivo = os.path.join(self.diretorio_dados, arquivo)

        if os.path.isfile(caminho_arquivo) and arquivo.endswith(".gz"):
            logging.debug(f"Lendo e tratando o arquivo {arquivo}...")
            chunks = pd.read_csv(
                caminho_arquivo,
                sep="\t",
                compression="gzip",
                low_memory=False,
                chunksize=chunksize,
            )

            for chunk in chunks:
                chunk.replace({"\\N": None}, inplace=True)
                caminho_destino = os.path.join(self.diretorio_tratados, arquivo[:-3])
                chunk.to_csv(
                    caminho_destino,
                    sep="\t",
                    mode="a",
                    index=False,
                    header=not os.path.exists(caminho_destino),
                )

            logging.debug(
                f"Tratamento concluído para {arquivo}. Arquivo tratado salvo em {caminho_destino}"
            )
            os.remove(caminho_arquivo)

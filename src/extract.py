import logging
import os
import shutil

import requests

from src.config.config import config


class DataExtractor:
    def __init__(
        self,
        base_url: str = config.BASE_URL,
        arquivos: list = config.ARQUIVOS,
        destino_diretorio: str = config.DESTINO_DIRETORIO,
    ):
        self.base_url = base_url
        self.arquivos = arquivos
        self.destino_diretorio = destino_diretorio

    def extract(self):
        logging.info("Inicio do processo de ETL")
        os.makedirs(self.destino_diretorio, exist_ok=True)

        for arquivo in self.arquivos:
            self.download_file(arquivo)

        logging.info("Download concluído.")

    def download_file(self, arquivo):
        url = os.path.join(self.base_url, arquivo)
        caminho_destino = os.path.join(self.destino_diretorio, arquivo)

        if not os.path.exists(caminho_destino):
            logging.info(f"Baixando {arquivo}...")
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                with open(caminho_destino, "wb") as f:
                    shutil.copyfileobj(response.raw, f)
                logging.info(f"{arquivo} baixado com sucesso!")
            else:
                logging.error(
                    f"Falha ao baixar {arquivo}. Código de status: {response.status_code}"
                )
        else:
            logging.info(f"{arquivo} já existe. Pulando o download.")


if __name__ == "__main__":
    extractor = DataExtractor()
    extractor.extract()

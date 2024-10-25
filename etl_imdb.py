# IMPORTS
import logging
import os
import sqlite3

from src.extract import DataExtractor
from src.transform import DataTransformer
from src.load import DataLoader
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

BANCO_DADOS = "imdb_data.db"
DESTINO_DIRETORIO = "data"
BASE_URL = "https://datasets.imdbws.com/"
ARQUIVOS = [
    "name.basics.tsv.gz",
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.crew.tsv.gz",
    "title.episode.tsv.gz",
    "title.principals.tsv.gz",
    "title.ratings.tsv.gz",
]


def load(conexao) -> None:
    # CARGA DOS DADOS
    diretorio_tratados = os.path.join("data", "tratados")

    arquivos = os.listdir(diretorio_tratados)

    for arquivo in arquivos:
        caminho_arquivo = os.path.join(diretorio_tratados, arquivo)

        if os.path.isfile(caminho_arquivo) and arquivo.endswith(".tsv"):
            df = pd.read_csv(caminho_arquivo, sep="\t", low_memory=False)

            nome_tabela = os.path.splitext(arquivo)[0]
            nome_tabela = nome_tabela.replace(".", "_").replace("-", "_")

            df.to_sql(nome_tabela, conexao, index=False, if_exists="replace")

            logging.info(
                f"Arquivo {arquivo} salvo como tabela {nome_tabela} no banco de dados."
            )

            # Remova o arquivo tratado após a carga no banco de dados
            os.remove(caminho_arquivo)

    logging.info("Todos os arquivos foram salvos no banco de dados.")


def create_views(conexao) -> None:
    # CRIAÇÃO DAS TABELAS ANALÍTICAS
    analitico_titulos = """
    CREATE TABLE IF NOT EXISTS analitico_titulos AS

    WITH 
    participantes AS (
        SELECT
            tconst,
            COUNT(DISTINCT nconst) as qtParticipantes
        
        FROM title_principals
        
        GROUP BY 1
    )

    SELECT
        tb.tconst,
        tb.titleType,
        tb.originalTitle,
        tb.startYear,
        tb.endYear,
        tb.genres,
        tr.averageRating,
        tr.numVotes,
        tp.qtParticipantes

    FROM title_basics tb 

    LEFT JOIN title_ratings tr
        ON tr.tconst = tb.tconst

    LEFT JOIN participantes tp
        ON tp.tconst = tb.tconst
    """

    analitico_participantes = """
    CREATE TABLE IF NOT EXISTS analitico_participantes AS

    SELECT
        tp.nconst,
        tp.tconst,
        tp.ordering,
        tp.category,
        tb.genres

    FROM title_principals tp

    LEFT JOIN title_basics tb
        ON tb.tconst = tp.tconst
    """

    queries = [
        "DROP TABLE IF EXISTS analitico_titulos",
        "DROP TABLE IF EXISTS analitico_participantes",
        analitico_titulos,
        analitico_participantes,
    ]

    logging.info("Salvando tabelas anlíticas no banco de dados.")

    for query in queries:
        conexao.execute(query)

    logging.info("Tabelas analíticas criadas com sucesso.")

    logging.info("Fim do processo de ETL")


if __name__ == "__main__":
    extractor = DataExtractor()
    extractor.extract()

    transformer = DataTransformer()
    transformer.transform()

    with sqlite3.connect(config.BANCO_DADOS) as conexao:
        loader = DataLoader(conexao)
        loader.load()

    create_views(conexao=conexao)

    conexao.close()

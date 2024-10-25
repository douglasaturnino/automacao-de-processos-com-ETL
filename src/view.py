import logging


class ViewCreator:
    def __init__(self, conexao):
        self.conexao = conexao

    def create_views(self):
        queries = self.get_view_creation_queries()
        logging.info("Salvando tabelas analíticas no banco de dados.")

        for query in queries:
            self.conexao.execute(query)

        logging.info("Tabelas analíticas criadas com sucesso.")
        logging.info("Fim do processo de ETL")

    @staticmethod
    def get_view_creation_queries():
        return [
            "DROP TABLE IF EXISTS analitico_titulos",
            "DROP TABLE IF EXISTS analitico_participantes",
            """
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
            LEFT JOIN title_ratings tr ON tr.tconst = tb.tconst
            LEFT JOIN participantes tp ON tp.tconst = tb.tconst
            """,
            """
            CREATE TABLE IF NOT EXISTS analitico_participantes AS
            SELECT
                tp.nconst,
                tp.tconst,
                tp.ordering,
                tp.category,
                tb.genres
            FROM title_principals tp
            LEFT JOIN title_basics tb ON tb.tconst = tp.tconst
            """,
        ]

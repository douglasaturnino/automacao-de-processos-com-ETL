# O contexto

Neste projeto, trabalharemos em uma empresa de mídia e esta empresa está montando um novo squad de produto. O objetivo deste squad é começar a trabalhar com campanhas de marketing baseadas em lançamentos de filmes e para isso precisaremos entender alguns comportamentos de consumo dos usuários deste tipo de mídia e as tendências de mercado. Uma das sugestões passadas pelo time de produto foi a exploração dos dados do IMDb.

# 1 problema de Negócio

## 1.1 O que é o IMDb

O IMDb (Internet Move Database) é uma das maiores base de dados online sobre cinema e tudo o que envolve a indústria do entretenimento. Além de reunir informações sobre artistas e produções, o site também permite que usuários criem listas e avaliem seus filmes favoritos.

## 1.2 Como funcionam as notas do IMDb

Qualquer usuário registrado no Internet Movie Database pode avaliar filmes, séries, documentários, e diversos outros tipos de produções audiovisuais em uma escala de 1 a 10, representada por estrelas. Os votos individuais são agregados e resumidos em uma nota única, exibida com destaque na página principal do título. Os usuários podem editar suas notas quantas vezes quiserem, mas a avaliação é única para cada perfil, ou seja, ao editar uma nota, a  antiga é sobrescrita. 

A “nota IMDb” exibida na página é calculada com base em todas as avaliações de todos os usuários O IMDb utiliza vários filtros para determinar o “peso” de determinadas avaliações na nota final, com o objetivo de diminuir ou eliminar o impacto de votações em massa combinadas para afetar a classificação de uma obra.

# 2 Premissas de negócio

O objetivo aqui será listar os principais desafios encontrados na [documentação](https://developer.imdb.com/non-commercial-datasets/) e os principais insights que tivemos a partir da observação feita.

 - A base de dados é atualizada diariamente, portanto é possível criar a recorrência de atualização dos dados;

 - Os arquivos são disponibilizados de forma compactada (.gz), portanto será necessário criar um processo de descompactação;

  - Os dados estão disponíveis de forma denormalizada e por isso será necessário realizar o cruzamento de dados entre os datasets para chegarmos na nossa base anaítica;

  - As tabelas possuem chaves que possibilitam o cruzamento entre si;

As variaveis do dataset original são:

### title.akas.tsv.gz
| Variavel | Definição|
----------- | ---------
|titleId (string) | Um identificador alfanumérico exclusivo do título
|ordering (integer) | Um número para identificar exclusivamente as linhas para um determinado titleId|
|title (string) | O título localizado|
|region (string) | A região para esta versão do título|
|language (string) | O idioma do título|
|types (array) | Conjunto enumerado de atributos para este título alternativo. Um ou mais dos |seguintes: "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". Novos valores podem ser adicionados no futuro sem aviso
|attributes (array) | Termos adicionais para descrever este título alternativo, não enumerados|
|isOriginalTitle (boolean) | 0: título não original; 1: título original|

### title.basics.tsv.gz
| Variavel | Definição|
----------- | ---------
|tconst (string) | Identificador alfanumérico exclusivo do título|
|titleType (string) | O tipo/formato do título (por exemplo, movie, short, tvseries, tvepisode, video, etc.)|
|primaryTitle (string) | O título mais popular / o título usado pelos cineastas em materiais promocionais no momento do lançamento|
|originalTitle (string) | Título original, no idioma original|
|isAdult (boolean) | 0: título não adulto; 1: título adulto|
|startYear (YYYY) | Representa o ano de lançamento de um título. No caso de séries de TV, é o ano de início da série|
|endYear (YYYY) | Ano final da série de TV. '\N' para todos os outros tipos de títulos|
|runtimeMinutes | Tempo de execução principal do título, em minutos|
|genres (string array) | Inclui até três gêneros associados ao título|

### title.crew.tsv.gz
| Variavel | Definição|
----------- | ---------
|tconst (string) | Identificador alfanumérico exclusivo do título|
|directors (array of nconsts) | Diretor(es) do título fornecido|
|writers (array of nconsts) | Escritor(es) do título fornecido|

### title.episode.tsv.gz
| Variavel | Definição|
----------- | ---------
|tconst (string) | Identificador alfanumérico do episódio|
|parentTconst (string) | Identificador alfanumérico da série de TV pai|
|seasonNumber (integer) | Número da temporada à qual o episódio pertence|
|episodeNumber (integer) | Número do episódio do tconst na série de TV|

### title.principals.tsv.gz
| Variavel | Definição|
----------- | ---------
|tconst (string) | Identificador alfanumérico exclusivo do título|
|ordering (inteiro) | Um número para identificar exclusivamente as linhas para um determinado titleId|
|nconst (string) | Identificador alfanumérico exclusivo do nome/pessoa|
|category (string) | A categoria do trabalho em que a pessoa estava|
|job (string) | O cargo específico, se aplicável, caso contrário '\N'|
|characters (string) | O nome do personagem interpretado, se aplicável, caso contrário '\N'|

### title.ratings.tsv.gz
| Variavel | Definição|
----------- | ---------
|tconst (string) | Identificador alfanumérico exclusivo do título|
|averageRating | Média ponderada de todas as avaliações individuais dos usuários|
|numVotes | Número de votos que o título recebeu|

### nome.básico.tsv.gz
| Variavel | Definição|
----------- | ---------
|nconst (string) | Identificador alfanumérico exclusivo do nome/pessoa|
|primaryName (string) | Nome pelo qual a pessoa é mais frequentemente creditada|
|birthYear | No formato YYYY|
|deathYear | No formato YYYY se aplicável, caso contrário '\N'|
|primaryProfession (array of strings) | As 3 principais profissões da pessoa|
|knownForTitles (array of tconsts) | Títulos pelos quais a pessoa é conhecida|

# 3 Planejamento da solução
## 3.1 Produto final

O que será entregue efetivamente?
 - Um ETL das fonde do IMDb para um banco de dados utilizando o rundeck.
 - Um dashboard com as analises dos filmes e dos participantes

## 3.2 Ferramentas

Quais ferramentas serão usadas no processo?

- Python
- Visual Studio code
- Git, GitHub
- ETL
- Rundeck

# 4 Modo de uso

Existem duas formas de utilizar a aplicação: pelo run.sh e pelo arquivo etl_imdb.py. Vamos explicar como rodar o projeto das duas formas mais abaixo. Este projeto foi desenvolvido com o Python 3.10, então, se você estiver utilizando outra versão, pode ocorrer alguns erros não esperados.

## Utilizando o run.sh

O script run.sh pode ser utilizado por sistemas que têm como base o Unix. Esse arquivo simplesmente navega até o caminho onde está o run.sh, ativa o ambiente virtual e executa o arquivo etl_imdb.py. Ele foi criado para ser usado no Rundeck. Para usar, basta ter um ambiente virtual na pasta do projeto e rodar o comando:

```bash
bash run.sh
```

## Utilizando o etl_imdb.py

O script etl_imdb.py é onde o projeto começa. Para utilizá-lo, você deve ativar o seu ambiente virtual de sua preferência. Vamos usar o venv como exemplo:

```bash
source .venv/bin/activat
```

Em seguida, podemos rodar o arquivo etl_imdb.py:

```bash
python etl_imdb.py
```
# 5. Resultados para o negócio

De acordo com os critérios definidos, foi feito o processo de ETL do projeto. Como resultado para o negócio foram criados:

 - Um dashboard que pode ser acessado aqui;
 - A Automação do projeto para um bando de dados.

# 6 Próximos passos
 
 - O projeto atualmente está em um bando de dados local uma possivel mudança pode ser feita para que o banco de dados fique acessivel remotamente.

 - Assim como o banco de dados o Rundeck tambem está local e pode ser colocado para ser acessado de forma online.
import nbformat as nbf
import os

def update_notebook(file_path):
    # Load the notebook
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Define new cells to insert
    new_cells = []

    # 1. Title and Intro
    nb.cells.insert(0, nbf.v4.new_markdown_cell(
        "# EDA e Tratamento de Dados de Emissões de CO2\n\n"
        "Este notebook realiza a Análise Exploratória de Dados (EDA) e o tratamento final da base para modelagem, "
        "incluindo limpeza, engenharia de atributos e padronização."
    ))

    # Identify cell indices for headers
    # Note: Indices shift after each insert. We'll find them dynamically or use offsets.
    
    current_index = 0
    
    # 2. Imports (originally cell 1, now 2 after title)
    nb.cells.insert(1, nbf.v4.new_markdown_cell(
        "## 1. Importações e Configurações\n\n"
        "Configuramos o ambiente com bibliotecas de visualização e carregamos os caminhos do projeto."
    ))
    
    # 3. Carregamento (originally cell 2, now 4)
    nb.cells.insert(3, nbf.v4.new_markdown_cell(
        "## 2. Carregamento dos Dados Consolidados\n\n"
        "Lemos a base de dados consolidada no passo anterior."
    ))
    
    # 4. Inspeção (after intro, imports, code1, carregamento, code2 -> now 6)
    nb.cells.insert(5, nbf.v4.new_markdown_cell(
        "## 3. Inspeção Inicial e Sanity Checks\n\n"
        "Verificamos a estrutura dos dados, tipos de colunas e presença de valores nulos ou duplicados."
    ))
    
    # Let's find more specific markers for the remaining sections
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'transmission' in source and 'extract' in source:
                # 5. Tratamento Transmissão
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 4. Tratamento da Variável de Transmissão\n\n"
                    "Extraímos o número de marchas e simplificamos as categorias de transmissão."
                ))
                cell.source = "# Extração de marchas e simplificação de categorias\n" + cell.source
                break

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'fuel_type' in source and 'map' in source:
                # 6. Tratamento Combustível
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 5. Tratamento da Variável de Combustível\n\n"
                    "Mapeamos os códigos de combustível para nomes legíveis e padronizados."
                ))
                cell.source = "# Mapeamento de tipos de combustível\n" + cell.source
                break

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'drop' in source and 'combined_mpg' in source:
                # 7. Limpeza
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 6. Limpeza e Seleção de Colunas\n\n"
                    "Removemos colunas redundantes ou que não contribuem para a modelagem."
                ))
                cell.source = "# Remoção de variáveis redundantes\n" + cell.source
                break

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'value_counts' in source and 'make' in source:
                # 8. Análise Exploratória
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 7. Análise Exploratória Inicial\n\n"
                    "Exploramos as distribuições das variáveis categóricas remanescentes."
                ))
                break

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'pd.cut' in source and 'cylinders' in source:
                # 9. Eng de Atributos
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 8. Agrupamento e Engenharia de Atributos\n\n"
                    "Criamos classes para variáveis numéricas para facilitar o aprendizado do modelo."
                ))
                cell.source = "# Criação de classes para cilindros\n" + cell.source
                break

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = "".join(cell.source)
            if 'to_parquet' in source and 'DADOS_TRATADOS' in source:
                # 10. Salvamento
                nb.cells.insert(i, nbf.v4.new_markdown_cell(
                    "## 9. Salvamento da Base Tratada\n\n"
                    "Exportamos o dataset final processado para ser utilizado na etapa de modelagem."
                ))
                cell.source = "# Exportação do dataset tratado\n" + cell.source
                break

    # Save the modified notebook
    with open(file_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook {file_path} updated successfully.")

if __name__ == "__main__":
    path = "/home/evlos/myprojects/Ciencias_Dados_Impressionador/Project_CO2_emissions/notebooks/02-fb-eda.ipynb"
    update_notebook(path)

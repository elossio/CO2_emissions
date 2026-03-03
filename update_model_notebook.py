import nbformat as nbf
import os
import re

def update_model_notebook(file_path):
    # Load the notebook
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # 1. CLEANUP: Remove all previously added markdown headers and clean code comments
    # Our headers start with '#' or '## ' and have specific text.
    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Skip the headers we added
            if (cell.source.startswith('# Modelagem') or 
                re.match(r'^## \d\. ', cell.source)):
                continue
        if cell.cell_type == 'code':
            # Remove the specific comments we added
            lines = cell.source.split('\n')
            filtered_lines = []
            for line in lines:
                if line.strip() in [
                    '# Importações e configurações de caminhos',
                    '# Função para organizar os coeficientes do modelo',
                    '# Carregamento da base e separação de features/alvo',
                    '# Configuração do ColumnTransformer para pré-processamento',
                    '# Integração do pipeline com o regressor e transformação do alvo',
                    '# Execução do Grid Search com Validação Cruzada',
                    '# Verificação dos melhores hiperparâmetros encontrados',
                    '# Extração e visualização dos coeficientes do modelo final'
                ]:
                    continue
                filtered_lines.append(line)
            cell.source = '\n'.join(filtered_lines).strip()
        new_cells.append(cell)
    
    nb.cells = new_cells

    # 2. INSERTION: Build the final list with headers
    final_cells = []
    
    # Title
    final_cells.append(nbf.v4.new_markdown_cell(
        "# Modelagem Preditiva de Emissões de CO2\n\n"
        "Este notebook foca na construção e otimização de um modelo de regressão para prever emissões de CO2, "
        "utilizando pipelines de pré-processamento sofisticados e busca de hiperparâmetros."
    ))

    # Markers and headers
    sections = [
        {
            "header": "## 1. Importações e Parâmetros\n\nCarregamos as bibliotecas necessárias, com foco em scikit-learn para preprocessing e modelagem.",
            "marker": "import pandas as pd",
            "comment": "# Importações e configurações de caminhos"
        },
        {
            "header": "## 2. Funções Utilitárias\n\nDefinimos funções para facilitar a análise dos resultados do modelo.",
            "marker": "def dataframe_coeficientes",
            "comment": "# Função para organizar os coeficientes do modelo"
        },
        {
            "header": "## 3. Carregamento dos Dados\n\nLemos a base tratada e separamos as variáveis explicativas (X) do alvo (y).",
            "marker": "pd.read_parquet(DADOS_TRATADOS)",
            "comment": "# Carregamento da base e separação de features/alvo"
        },
        {
            "header": "## 4. Preparação do Pipeline de Preprocessamento\n\nConfiguramos diferentes transformadores para cada tipo de variável (categórica, numérica, classes).",
            "marker": "preprocessamento = ColumnTransformer",
            "comment": "# Configuração do ColumnTransformer para pré-processamento"
        },
        {
            "header": "## 5. Definição do Modelo com Regressão de Alvo\n\nUtilizamos o `TransformedTargetRegressor` para aplicar uma transformação (ex: Quantile) no alvo para normalizá-lo.",
            "marker": "TransformedTargetRegressor(",
            "comment": "# Integração do pipeline com o regressor e transformação do alvo"
        },
        {
            "header": "## 6. Otimização de Hiperparâmetros (Grid Search)\n\nRealizamos uma busca exaustiva para encontrar o melhor parâmetro de regularização do modelo Ridge.",
            "marker": "grid_search = GridSearchCV",
            "comment": "# Execução do Grid Search com Validação Cruzada"
        },
        {
            "header": "## 7. Análise dos Melhores Resultados\n\nInspecionamos os parâmetros e scores resultantes da melhor rodada.",
            "marker": "grid_search.best_params_",
            "comment": "# Verificação dos melhores hiperparâmetros encontrados"
        },
        {
            "header": "## 8. Análise de Coeficientes e Importância\n\nAnalisamos os pesos atribuídos pelo modelo a cada variável para entender quais mais impactam a emissão.",
            "marker": "coefs = dataframe_coeficientes(",
            "comment": "# Extração e visualização dos coeficientes do modelo final"
        }
    ]

    used_sections = set()
    
    for cell in nb.cells:
        # Check if this cell matches any section marker
        for i, section in enumerate(sections):
            if i not in used_sections and cell.cell_type == 'code' and section["marker"] in cell.source:
                final_cells.append(nbf.v4.new_markdown_cell(section["header"]))
                cell.source = section["comment"] + "\n" + cell.source
                used_sections.add(i)
                break
        final_cells.append(cell)

    nb.cells = final_cells

    # Save the modified notebook
    with open(file_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook {file_path} updated successfully.")

if __name__ == "__main__":
    path = "/home/evlos/myprojects/Ciencias_Dados_Impressionador/Project_CO2_emissions/notebooks/03-fb-modelos.ipynb"
    update_model_notebook(path)

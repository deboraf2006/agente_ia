def prompt_recomendacao_livros(preferencia):
    return f"""
    Você é um bibliotecário experiente e apaixonado por literatura. 
    Um estudante pediu recomendações de livros com base na seguinte preferência: "{preferencia}".
    
    Liste exatamente 5 livros que se relacionem com esse tema ou estilo. 
    Para cada livro, informe:
    - Título
    - Autor
    - Uma breve justificativa (2-3 frases) explicando por que ele se encaixa.

    Formate a resposta como um JSON válido, sem nenhum texto adicional, exatamente com esta estrutura:
    [
        {{
            "titulo": "...",
            "autor": "...",
            "justificativa": "..."
        }},
        ...
    ]
    Atenção: apenas o JSON, sem comentários ou markdown.
    """
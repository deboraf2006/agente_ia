import json
from flask import Blueprint, render_template, request, jsonify
from app.gemini_client import obter_resposta_do_gemini
from app.prompts import prompt_recomendacao_livros

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/recomendacao', methods=['POST'])
def recomendacao():
    dados = request.get_json()
    entrada = dados.get('entrada', '').strip()

    if not entrada:
        return jsonify({'erro': 'Informe um tema ou livro.'}), 400

    try:
        prompt = prompt_recomendacao_livros(entrada)
        resposta_bruta = obter_resposta_do_gemini(prompt)

        # O Gemini às vezes envolve o JSON em crases triplas
        if '```' in resposta_bruta:
            inicio = resposta_bruta.find('[')
            fim = resposta_bruta.rfind(']') + 1
            resposta_json = resposta_bruta[inicio:fim]
        else:
            resposta_json = resposta_bruta

        livros = json.loads(resposta_json)
        return jsonify({'recomendacoes': livros})

    except json.JSONDecodeError:
        # Caso o parsing falhe, devolvemos o texto bruto
        return jsonify({'recomendacoes_texto': resposta_bruta})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
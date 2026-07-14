document.getElementById('btn-recomendar').addEventListener('click', async () => {
    const entrada = document.getElementById('entrada').value.trim();
    const resultadoDiv = document.getElementById('resultado');

    if (!entrada) {
        resultadoDiv.innerHTML = '<p class="erro">Digite algo.</p>';
        return;
    }

    resultadoDiv.innerHTML = '<p>Buscando recomendações...</p>';

    try {
        const response = await fetch('/api/recomendacao', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entrada })
        });
        const data = await response.json();

        if (data.erro) {
            resultadoDiv.innerHTML = `<p class="erro">Erro: ${data.erro}</p>`;
            return;
        }

        if (data.recomendacoes) {
            let html = '<h2>Livros recomendados:</h2>';
            data.recomendacoes.forEach(livro => {
                html += `
                    <div class="livro">
                        <h3>${livro.titulo}</h3>
                        <p><strong>Autor:</strong> ${livro.autor}</p>
                        <p>${livro.justificativa}</p>
                    </div>
                `;
            });
            resultadoDiv.innerHTML = html;
        } else if (data.recomendacoes_texto) {
            // Fallback para texto bruto
            resultadoDiv.innerHTML = `<pre>${data.recomendacoes_texto}</pre>`;
        }
    } catch (err) {
        resultadoDiv.innerHTML = '<p class="erro">Falha na requisição.</p>';
        console.error(err);
    }
});
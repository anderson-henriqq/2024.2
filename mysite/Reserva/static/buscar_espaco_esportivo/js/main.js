 // Função para aplicar a seleção no select
 function aplicarSelecao() {
    const ufSelect = document.getElementById('uf');
    const ufSelecionada = localStorage.getItem('uf_selecionada');  // Recupera o valor da UF salva

    if (ufSelecionada) {
        ufSelect.value = ufSelecionada;  // Aplica a seleção salva
    }
}

// Função para salvar a seleção ao mudar
function salvarSelecao() {
    const ufSelect = document.getElementById('uf');
    localStorage.setItem('uf_selecionada', ufSelect.value);  // Salva a seleção no localStorage
}

// Aplica a seleção ao carregar a página
window.onload = aplicarSelecao;

document.getElementById('uf').addEventListener('change', salvarSelecao);
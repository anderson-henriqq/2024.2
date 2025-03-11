let selectedDia = null;
let selectedDiaEscrito = null; 
let selectedHorario = null;

// Pega o modal
let modal = document.getElementById("myModal");

// Pega o botão de fechar (X)
let closeModal = document.getElementsByClassName("close")[0];

document.getElementById('botao_Reservar').addEventListener('click', function() {
if (selectedHorario !== null) {
    // Construir a URL com o valor de selectedHorario
    let url = `setAgenda/${selectedHorario}`;

    // Redirecionar para a URL
    window.location.href = url;
} else {
    alert('Selecione um horário antes de reservar.');
}
});

function toggleBackgroundDay(element) {
    // Seleciona todos os blocos (ou elementos similares) e remove a classe "active" de todos
    const blocos = document.querySelectorAll(".bloco");  // Aqui você pode alterar para o seletor correto caso não seja .bloco
    blocos.forEach(function(bloco) {
        bloco.classList.remove("active");
        selectedDia = null;
        selectedDiaEscrito = null; 
    });

    // Adiciona a classe "active" apenas no item que foi clicado
    element.classList.add("active");

    selectedDia = element.getAttribute("data-dia");
    
}

function toggleBackgroundSchedules(element) {
    // Seleciona todos os blocos (ou elementos similares) e remove a classe "active" de todos
    const blocos = document.querySelectorAll(".bloco_horario");  // Aqui você pode alterar para o seletor correto caso não seja .bloco
    blocos.forEach(function(bloco) {
        bloco.classList.remove("active");
        selectedHorario = null;
    });

    // Adiciona a classe "active" apenas no item que foi clicado
    element.classList.add("active");

    selectedHorario = element.getAttribute("data-id");

    checkOpenModal();
}

function checkOpenModal() {
    if (selectedDia !== null && selectedHorario !== null) {
        openModal(selectedDia, selectedHorario); // Passa o valor do data-dia e do bloco para abrir o modal
    }   
}

function openModal(dia, id_horario) {
    // Faz a requisição para obter as informações do horário
    fetch(`/getInfoHorario/${id_horario}`)
        .then(response => response.json())
        .then(data => {
            // Preenche os dados no modal
            document.getElementById("nome_recurso_modal").textContent = `${data.recurso}`;
            document.getElementById("modal-dia").textContent = `${data.data}`;
            document.getElementById("modal-horario").textContent = `${data.horario}`;
            document.getElementById("modal-bloco").textContent = `${data.localizacao}`;
            document.getElementById("modal-preco").textContent = `${data.preco}`;
        })
        .catch(error => console.error('Erro ao obter horário:', error));

    // Exibe o modal
    modal.style.display = "block";
}

// Quando o usuário clica no botão de fechar (X), fecha o modal
closeModal.onclick = function() {
    modal.style.display = "none";
    const blocos = document.querySelectorAll(".bloco_horario");  // Aqui você pode alterar para o seletor correto caso não seja .bloco
    blocos.forEach(function(bloco) {
        bloco.classList.remove("active");
        selectedHorario = null;
    });

}

// Quando o usuário clica em qualquer lugar fora do modal, ele também fecha
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
        const blocos = document.querySelectorAll(".bloco_horario");  // Aqui você pode alterar para o seletor correto caso não seja .bloco
        blocos.forEach(function(bloco) {
            bloco.classList.remove("active");
            selectedHorario = null;
        });
    }
}




document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todas as datas no calendário
    document.querySelectorAll(".bloco").forEach(function (bloco) {
        bloco.addEventListener("click", function () {
            let diaSelecionado = this.getAttribute("data-dia");  // Pega a data do atributo personalizado
            let recursoId = "{{ recurso }}";  // ID do recurso vindo do Django

            // Fazer a requisição AJAX para obter os horários da data selecionada
            fetch(`/horarios/${recursoId}/${diaSelecionado}/`)
                .then(response => response.json())
                .then(data => {
                    let horariosContainer = document.getElementById("horarios-container");
                    horariosContainer.innerHTML = ""; // Limpar horários anteriores

            // Criar os novos horários dinamicamente
                    data.horarios.forEach(horario => {
                        let div = document.createElement("div");
                        div.className = "bloco_horario";
                        div.setAttribute("data-id", horario.id);
                        div.onclick = function() { toggleBackgroundSchedules(this); }; // Adiciona a função de clique
                        div.innerHTML =`<div class="conteudo_horario">
                                            <div class="hora">
                                                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <path d="M9.9915 1.66665C5.3915 1.66665 1.6665 5.39998 1.6665 9.99998C1.6665 14.6 5.3915 18.3333 9.9915 18.3333C14.5998 18.3333 18.3332 14.6 18.3332 9.99998C18.3332 5.39998 14.5998 1.66665 9.9915 1.66665ZM9.99984 16.6666C6.3165 16.6666 3.33317 13.6833 3.33317 9.99998C3.33317 6.31664 6.3165 3.33331 9.99984 3.33331C13.6832 3.33331 16.6665 6.31664 16.6665 9.99998C16.6665 13.6833 13.6832 16.6666 9.99984 16.6666Z" fill="#A1CF00"/>
                                                    <path d="M10.4165 5.83331H9.1665V10.8333L13.5415 13.4583L14.1665 12.4333L10.4165 10.2083V5.83331Z" fill="#A1CF00"/>
                                                </svg>
                                                <span class="tempo">${horario.h_inicial}  -  ${horario.h_final}</span>
                                            </div>
                                            <div class="preco">
                                                <span>R$ ${horario.preco} <sup>/h</sup></span>
                                            </div>
                                        </div>`
                        horariosContainer.appendChild(div);


                        });
                    })
            .catch(error => console.error("Erro ao buscar horários:", error));
        });
    });
});
// Obtém os elementos do modal e do botão
var modal = document.querySelector(".modal-avaliar-recurso");
var btn_avaliar = document.querySelector(".btn-avaliar");
var btn_close = document.querySelector(".close");

// Abre o modal quando o botão é clicado
btn_avaliar.onclick = function() {
  modal.style.display = "block";
}

// Fecha o modal quando o "x" é clicado
btn_close.onclick = function() {
  modal.style.display = "none";
}

// Fecha o modal quando clica fora dele
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Estrelas do rating
// const rating = document.querySelector('.rating');

// rating.addEventListener('click', (event) => {
//   if (event.target.tagName === 'svg') {
//     const clickedLabel = event.target.parentNode;
//     const clickedRadio = document.getElementById(clickedLabel.htmlFor);
//     const radioButtons = rating.querySelectorAll('input[type="radio"]');

//     for (const radio of radioButtons) {
//       if (radio.value <= clickedRadio.value) {
//         radio.checked = true;
//       }
//     }
//   }
// });
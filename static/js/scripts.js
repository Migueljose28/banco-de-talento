let valor = 0;
//parseInt(document.getElementById("valor").value);

const url = 'static/pdf/curriculo-100.pdf';  // Caminho para o PDF
 // Variável inicial
 

 // Funções para alterar o valor
function atualizarValor() {
     document.getElementById('displayValor').textContent = valor;
      // Carregar o PDF com pdf.js
 pdfjsLib.getDocument(url).promise.then(function(pdf) {
 


 pdf.getPage(valor).then(function(page) {
     var canvas = document.getElementById('pdf-canvas');
     var context = canvas.getContext('2d');


     // Definir a escala para a exibição
     var scale = 1.5; 
     var viewport = page.getViewport({ scale: scale });

     canvas.height = viewport.height;
     canvas.width = viewport.width;

     // Renderizar a página do PDF
     page.render({
         canvasContext: context,
         viewport: viewport
     });
 });
});
 }

 document.getElementById("valor").addEventListener("input", function() {
    valor = parseInt(this.value);  // Atualiza a variável 'valor' com o valor do textarea
    document.getElementById("displayValor").innerText = valor;  // Exibe o valor atualizado
 });
 
 // Função para diminuir
 document.getElementById('decrementar').onclick = function() {
     valor -= 1;
     atualizarValor();
 };

 // Função para aumentar
 document.getElementById('incrementar').onclick = function() {
     valor += 1;
     atualizarValor();
 };

 document.getElementById('commit').onclick = function(){
     atualizarValor();
 }

 
// Bloquear o clique direito no canvas
document.getElementById('pdf-canvas').addEventListener('contextmenu', function(event) {
 event.preventDefault();  // Impede a ação padrão (abrir o menu de contexto)
 return false;
});

document.addEventListener("keydown", function(event) {
    if (event.ctrlKey && event.key === "p") {
      event.preventDefault(); // Impede a ação padrão
      alert("A impressão desta página foi desativada!");
    }
  });
  
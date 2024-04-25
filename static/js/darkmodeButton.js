// Função para alternar entre os modos light e dark
function switchMode() {
  // Alternar entre os modos light e dark
  if ($("body").hasClass("dark")) {
      $("body").removeClass("dark");
      $("#sunIcon").css("display", "block");
      $("#moonIcon").css("display", "none");
      // Salvar a escolha do modo no armazenamento local
      localStorage.setItem("mode", "light");
  } else {
      $("body").addClass("dark");
      $("#sunIcon").css("display", "none");
      $("#moonIcon").css("display", "block");
      // Salvar a escolha do modo no armazenamento local
      localStorage.setItem("mode", "dark");
  }
}

// Quando o documento estiver pronto
$(document).ready(function() {
  // Recuperar a escolha do modo do armazenamento local, se existir
  var mode = localStorage.getItem("mode");
  if (mode === "dark") {
      // Se o modo for dark, aplicar a classe dark ao corpo do documento
      $("body").addClass("dark");
      $("#sunIcon").css("display", "none");
      $("#moonIcon").css("display", "block");
  } else {
      // Se o modo for light (ou se não houver escolha salva), manter o padrão
      $("body").removeClass("dark");
      $("#sunIcon").css("display", "block");
      $("#moonIcon").css("display", "none");
  }

  // Vincular o evento de clique do botão à função switchMode
  $("#switchButton").on("click", switchMode);
});

$(document).ready(function(){
    $('#navbar-toggler').click(function(){
        $('#navbar-links').toggleClass('show');
    });

    // Adiciona esta linha para remover a classe 'show' por padrão
    $('#navbar-links').removeClass('show');
});

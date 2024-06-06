var cep=document.getElementById('cep');
var rua=document.getElementById('rua');
var msg=document.getElementById('msg');
var cidade=document.getElementById('cidade');
var bairro=document.getElementById('bairro');
var botao=document.getElementById('form');

botao.addEventListener('submit',(event)=>{
    event.preventDefault();
    var cnpj=document.getElementById('cnpj');
    if (cnpj == '') return false;
    if (cnpj.length != 14){
       alert("Por favor, digite um CNPJ válido");
        return false
      }

    // Elimina CNPJs inválidos conhecidos
    if (cnpj == "00000000000000" || cnpj == "11111111111111" || cnpj == "22222222222222" || cnpj == "33333333333333" || cnpj == "44444444444444" || cnpj == "55555555555555" || cnpj == "66666666666666" || cnpj == "77777777777777" || cnpj == "88888888888888" || cnpj == "99999999999999") {
        return false;
    }

    // Valida dígitos verificadores
    var tamanho = cnpj.length - 2;
    var numeros = cnpj.substring(0, tamanho);
    var digitos = cnpj.substring(tamanho);
    var soma = 0;
    var pos = tamanho - 7;

    for (var i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    var resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0)) return false;

    tamanho = tamanho + 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (var i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) pos = 9;
    }

    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1)) return false;

    return true;
});


botao.addEventListener('submit', (event)=>{
  event.preventDefault();

  if (cep.value===""){
    alert('teste');
    return;
  }else {
    var ver=cep.value;
    fetch(`https://cdn.apicep.com/file/apicep/${ver}.json`)
  .then(function(response) {
    return response.json(); 
  })
  .then(function(data) {
    var cidadeTela=data.city;
    var ruaTela=data.address;
    var bairroTela=data.district;
    if (bairroTela ==='Ibura'){
      cidade.innerHTML=cidadeTela;
      rua.innerHTML=ruaTela;
      bairro.innerHTML=bairroTela;
      console.log(cidadeTela);
      msg.innerHTML='';
      console.log(data);
    }else{
      msg.innerHTML="ops só atendemos o bairro do ibura";
      cidade.innerHTML='';
      rua.innerHTML='';
      bairro.innerHTML='';
    }
    
  })
  .catch(function(error) {
    console.error('Erro ao buscar dados da API:', error);
  });
return;
  }
});

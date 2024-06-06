var cep=document.getElementById('cep');
var rua=document.getElementById('rua');
var msg=document.getElementById('msg');
var cidade=document.getElementById('cidade');
var bairro=document.getElementById('bairro');
var botao=document.getElementById('form');
var cpf=document.getElementById('cpf');

var cep=document.getElementById('cep');
var rua=document.getElementById('rua');
var msg=document.getElementById('msg');
var cidade=document.getElementById('cidade');
var bairro=document.getElementById('bairro');
var botao=document.getElementById('form');


 
 
var form=document.getElementById('cadastro');
form.addEventListener('submit', (event)=>{
 
event.preventDefault();
if (cep.value===""){
  console.log(cep);
    alert('CEP inválido');
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
      alert("Por favor, digite um CEP válido");
      msg.innerHTML="ops só atendemos o bairro do ibura";
      cidade.innerHTML='';
      rua.innerHTML='';
      bairro.innerHTML='';
    }
    
  })
  .catch(function(error) {
    console.error('Erro ao buscar dados da API:', error);
    return false;
  });

 var dados=cpf.value
 if (dados === '' || dados.length !== 11 || dados === '00000000000') {
    cpf.classList.add("incorreto");
    alert("Por favor, digite um CPF válido");
    return false;
}

// Cálculo do primeiro dígito verificador
let soma = 0;
for (let i = 1; i <= 9; i++) {
    soma += parseInt(dados.substring(i - 1, i)) * (11 - i);
}
let resto = (soma * 10) % 11;
if (resto === 10 || resto === 11) {
    resto = 0;
}
if (resto !== parseInt(dados.substring(9, 10))) {
    cpf.classList.add("incorreto");
    alert("Por favor, digite um CPF válido");
    return;
}

// Cálculo do segundo dígito verificador
soma = 0;
for (let i = 1; i <= 10; i++) {
    soma += parseInt(dados.substring(i - 1, i)) * (12 - i);
}
resto = (soma * 10) % 11;
if (resto === 10 || resto === 11) {
    resto = 0;
}
resto === parseInt(dados.substring(10, 11));
if (resto !== parseInt(dados.substring(10, 11))){
    cpf.classList.add("incorreto");
    alert("Por favor, digite um CPF válido");
    return;
}else{
    
    // form.submit();
    return;
}
  }});
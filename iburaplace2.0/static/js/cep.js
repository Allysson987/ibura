var cep=document.getElementById('cep');
var rua=document.getElementById('rua');
var msg=document.getElementById('msg');
var cidade=document.getElementById('cidade');
var bairro=document.getElementById('bairro');
var botao=document.getElementById('form');
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

 
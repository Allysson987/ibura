var cpf=document.getElementById('cpf');

console.log('tste');
var form=document.getElementById('login');
form.addEventListener('submit', (event)=>{
 event.preventDefault();
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
    
    form.submit();
    return;
}

});
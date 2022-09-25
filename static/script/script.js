const verificados = document.getElementById('btn-verificados')
const botaoPesquisar = document.getElementById('btn-pesquisar')


let verificadosCheck = verificados.value
MostrarVerificados = () => {

    if(verificadosCheck == 'on'){
        verificadosCheck = 'off'
        verificados.value = verificadosCheck
        console.log(verificados.value)

    } else {
        verificadosCheck = 'on'
        verificados.value = verificadosCheck
        console.log(verificados.value)
    }
}



Pesquisar = () => {
    if(botaoPesquisar.value == 'off'){
        botaoPesquisar.value = 'on'
    } else {
        botaoPesquisar.value = 'off'
    }
}
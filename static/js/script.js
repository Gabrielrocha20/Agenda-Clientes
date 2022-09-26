const verificados       = document.getElementById('btn-verificados')
const botaoPesquisar    = document.getElementById('btn-pesquisar')
const alteraDados       = document.getElementById('alteraDados')
const btn_sair          = document.getElementById('btn_sair')
const registraFiltro    = document.getElementById('registraFiltro')
const btnRegistraFiltro = document.getElementById('btnRegistraFiltro')
const btn_confirma      = document.getElementById('btn-confirma')

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
        botaoPesquisar.value = `on ${verificados.value}`
    } else {
        botaoPesquisar.value = 'off'
    }
}

function AlterarDados(){
    let container = document.getElementById('container')
    let background = document.getElementById('background')

    if(alteraDados.style.display == 'flex'){
        alteraDados.style.display = 'none'
        container.style.filter = 'blur(0px)'
        background.style.display = 'none'

    } else {
        alteraDados.style.display = 'flex'
        container.style.filter = 'blur(5px)'
        background.style.display = 'block'
    }
}

function BotaoSair(){
    if(btn_sair.value == 'off'){
        btn_sair.value = 'on'
        console.log(btn_sair.value)
    } else {
        btn_sair.value = 'off'
        console.log(btn_sair.value)
    }
}

function RegistraFiltro(){
    let container = document.getElementById('container')
    let background = document.getElementById('background')

    if(registraFiltro.style.display == 'flex'){
        registraFiltro.style.display = 'none'
        container.style.filter = 'blur(0px)'
        background.style.display = 'none'

    } else {
        registraFiltro.style.display = 'flex'
        container.style.filter = 'blur(5px)'
        background.style.display = 'block'
    }
}


function btnConfirma(){
    if(btn_confirma.value == 'off'){
        btn_confirma.value = 'on'
        console.log(btn_confirma.value)
    } else {
        btn_confirma.value = 'off'
        console.log(btn_confirma.value)
    }
}
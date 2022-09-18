# Workshop_rasa

Projeto Hello
19 Setembro 2022


## Exercicio 1:
Crie um chatbot que permita ao aluno verificar situações de risco (ex: as notas encontram-se separadas por mais do que dois valores):
        1) Realizar ações básicas;
        2) Conectar-se com o módulo de Education Intelligence;
        3) Conectar-se com módulos externos (código python): Análise de sentimentos;
        4) Conectar-se a API cliente (simulador e-schooling);
        

#### Actions server
>rasa run actions


#### Rasa 
>rasa run --enable-api --cors="*" 


#### Servidor cliente (simulador E-schooling)
> python -m http.server 
Aceder ao file bot.html

#### Simulador Education Intelligence (servidor json-server)
>npx json-server --watch notas.json


## Exercicio 2:

Crie um chatbot que ajude os aluno a preencher um formulário para contacto com os docente:
	
    1) Cumprimentar o aluno;
    2) Questionar qual o professor que deseja contactar;
    3) Solicitar um e-mail para o professor entrar em contacto; 
    4) Informar o aluno que o professor já foi informado;
    5) Despedir-se;

>rasa train
>rasa shell

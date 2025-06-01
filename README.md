# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/images/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Alert-DOS

## 👨‍👩 Grupo

Grupo de número <b>4</b> formado pelos integrantes mencionados abaixo.

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/cirohenrique/">Ciro Henrique</a> ( <i>RM559040</i> )
- <a href="https://www.linkedin.com/in/marcofranzoi/">Marco Franzoi</a> ( <i>RM559468</i> )
- <a href="https://www.linkedin.com/in/rodrigo-mazuco-16749b37/">Rodrigo Mazuco</a> ( <i>RM559712</i> )

## 👩‍🏫 Professores:

### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

## 📜 Descrição

<b>Referência</b>: https://on.fiap.com.br/mod/assign/view.php?id=491867&c=13085

### Problema

Nos últimos anos, o Brasil enfrentou tragédias causadas por deslizamentos em encostas, provocados pelo solo excessivamente encharcado. Sabemos que é muito difícil evitar esses acidentes, pois a natureza é incontrolável e, devido às ações humanas, esses eventos estão se tornando cada vez mais imprevisíveis.

As informações abaixo foram levantadas a partir do site https://disasterscharter.org.

#### São Sebastião, fevereiro 2023

Não precisamos voltar muito no tempo para nos lembrarmos dos eventos ocorridos na cidade de São Sebastião, litoral do estado de São Paulo, em fevereiro de 2023. Por conta da quantidade excessiva de chuvas — acumulando, em um único dia, a quantidade total esperada para todo o mês —, a cidade foi afetada por diversos alagamentos e deslizamentos nas encostas da região. Infelizmente, 64 moradores da Vila Sahy, bairro mais afetado pelos deslizamentos, perderam a vida, pois não tiveram tempo suficiente para abandonar a região em segurança.

As imagens abaixo, retiradas do site https://disasterscharter.org/activations/landslide-in-brazil-activation-803-, mostram como essas regiões foram afetadas com os deslizamentos.

![São Sebastião - Barra Sahy](https://github.com/RM559712/fase7_global_solution/blob/main/assets/images/SaoSebastiao_BarraSahy-1.png)
![São Sebastião - Barra Sahy](https://github.com/RM559712/fase7_global_solution/blob/main/assets/images/SaoSebastiao_BarraSahy-2.png)
![São Sebastião - Barra Sahy](https://github.com/RM559712/fase7_global_solution/blob/main/assets/images/SaoSebastiao_BarraSahy-3.png)

#### Recife, junho de 2022

Pouco menos de um ano antes dos eventos mencionados, um bairro da Região Metropolitana do Recife, chamado Jardim Monte Verde — localizado na divisa entre Recife e Jaboatão dos Guararapes —, também registrou, em um único dia, um volume de chuvas que superou a média histórica mensal para o período, provocando diversos alagamentos e deslizamentos. Sendo a região mais atingida, o episódio causou 44 mortes e deixou várias famílias desabrigadas.

As imagens abaixo, retiradas do site https://disasterscharter.org/activations/landslide-in-brazil-activation-758-, mostram como essas regiões foram afetadas com os deslizamentos.

![Recife - Jaboatão dos Guararapes](https://github.com/RM559712/fase7_global_solution/blob/main/assets/images/Recife_JaboataoDosGuararaoes-1.png)
![Recife - Jardim Monte Verde](https://github.com/RM559712/fase7_global_solution/blob/main/assets/images/Recife_JardimMonteVerde-1.png)

#### Outros relatos

Infelizmente, muitos outros episódios causaram tragédias em diversas regiões do Brasil, como em Angra dos Reis, no estado do Rio de Janeiro, em abril de 2022.

Por se tratarem de regiões sujeitas a esse tipo de evento, será que, se essas famílias tivessem acesso a um sistema capaz de alertá-las sempre que a área estivesse se aproximando do seu limite e correndo risco de deslizamentos, elas poderiam ter sido salvas? A resposta é: sim, acreditamos que isso seria possível. Para tanto, um sistema simples e de baixo custo seria suficiente para ajudar não apenas a salvar todas essas vidas — o ponto principal da questão —, mas também para auxiliar as equipes de resgate e contenção a tomarem decisões que, talvez, evitassem os danos materiais causados à região.

### Projeto

Este projeto foi desenvolvido utilizando itens de baixo custo, como sensores de umidade do solo com potenciômetro, além de um sistema simples de alertas comunitários voltado à atuação em áreas de risco.

A proposta é permitir que regiões localizadas em áreas vulneráveis sejam cadastradas no sistema com base em coordenadas de latitude e longitude, definindo também um percentual máximo de umidade do solo considerado seguro. Por meio de sensores e leituras frequentes, torna-se possível monitorar o aumento progressivo da umidade nessas regiões. Caso, em determinado momento, o sistema identifique que o limite configurado foi ultrapassado pelas leituras do sensor, um alerta de segurança será enviado imediatamente a uma equipe responsável por auxiliar na evacuação da área.

### Sistema

Algumas informações sobre os módulos do sistema:

- <strong>Módulo "Localizações"</strong>: Permite o cadastro das áreas que deverão ser monitoradas, como encostas, serras, morros ou qualquer outro tipo de terreno. A partir dos parâmetros de latitude e longitude, é possível gerenciar a região e fornecer informações que agilizem a tomada de decisões. Além disso, com a definição de um percentual máximo de umidade do solo, podem ser estabelecidas regras para a prevenção de deslizamentos ou outros acidentes geológicos.
- <strong>Módulo "Sensores"</strong>: Permite que sejam cadastrados diferentes sensores com seus códigos de série e associados ao tipo "Sensor de Umidade do solo".
- <strong>Módulo "Medições"</strong>: Permite o cadastro de medições utilizando como parâmetros o ID da localização onde a medição foi realizada (conforme cadastro no módulo "Localizações"), o ID do sensor utilizado (conforme cadastro no módulo "Sensores") e o valor da medição. Ao final do processo, caso o valor registrado ultrapasse o percentual máximo de umidade do solo definido para a região, um alerta será enviado imediatamente, com o objetivo de auxiliar na tomada de decisões. Esse módulo atua em paralelo com o serviço utilizado pelo sensor (API), responsável pelo armazenamento dos registros conforme a frequência de medição configurada.
- <strong>Módulo "Gráficos"</strong>: Permite a visualização de gráficos das medições cadastradas por localização;

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

1. <b>assets</b>: Diretório para armazenamento de arquivos complementares da estrutura do sistema.
    - Diretório "images": Diretório para armazenamento de imagens.

2. <b>config</b>: Diretório para armazenamento de arquivos em formato <i>json</i> contendo configurações.

3. <b>document</b>: Diretório para armazenamento de documentos relacionados ao sistema.

4. <b>scripts</b>: Diretório para armazenamento de scripts.

5. <b>src</b>: Diretório para armazenamento de código fonte do sistema.

6. <b>tests</b>: Diretório para armazenamento de resultados de testes.
	- Diretório "images": Diretório para armazenamento de imagens relacionadas aos testes efetuados.

7. <b>README.md</b>: Documentação do projeto em formato markdown.

<i><strong>Importante</strong>: A estrutura de pastas foi mantida neste formato para atender ao padrão de entrega dos projetos.</i>

## 🔧 Como executar o código

Como se trata de uma versão em formato <i>prompt</i>, para execução das funcionalidades, os seguintes passos devem ser seguidos:

1. Utilizando algum editor de código compatível com a linguagem de programação Python (<i>VsCode, PyCharm, etc.</i>), acesse o diretório "./src/prompt".
2. Neste diretório, basta abrir o arquivo "main.py" e executá-lo.

Alguns módulos do sistema podem ser executados em formato <i>web</i> utilizando Streamlit conforme descritos em [Descrição](https://github.com/RM559712/fase4_cap1?tab=readme-ov-file#-descri%C3%A7%C3%A3o). Para acessá-los, os seguintes passos devem ser seguidos:

1. Utilizando algum editor de código compatível com a linguagem de programação Python (<i>VsCode, PyCharm, etc.</i>), acesse o diretório "./src/web/modules/{nome_do_modulo}".
2. Neste diretório, basta identificar o arquivo desejado e executar o comando `streamlit run {nome_do_arquivo}.py`.

Para essa versão não são solicitados parâmetros para acesso como por exemplo <i>username</i>, <i>password</i>, <i>token access</i>, etc.

## 🗃 Histórico de lançamentos

* 1.0.0 - 06/06/2025

## 📋 Licença

Desenvolvido pelo Grupo 4 para o projeto da fase 7 (<i>Global Solution - 2º Semestre</i>) da <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a>. Está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
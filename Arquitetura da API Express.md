\# Para criar o projeto node.js aceitando de forma rápida, sem precisar configurar passo a passo.

**npm init -y**

\#Para instalar o express

**npm install express**

\#Para instalar o TypeScript e suas tipagens

**npm install -D typescript @types/express @types/node tsx**

\# Já com este comando nos criamos o arquivo de configuração do TypeScript.

npx tsc --init



src/

&#x20;┣ 📂 controllers/

&#x20;┃ ┗ 📜 movieController.ts

&#x20;┣ 📂 services/

&#x20;┃ ┗ 📜 movieService.ts

&#x20;┣ 📂 routes/

&#x20;┃ ┗ 📜 movieRoutes.ts

&#x20;┗ 📜 server.ts



1º - Criação do server.ts

\#Importação do express

import express from 'express';



\#Criação do servidor

const app = express();

\#Possibilita ler as requisições em formato JSON

app.use(express.json());



\#Define a porta que estará rodando o servidor

const PORT = 3000;

app.listen(PORT, () => {

&#x20;   console.log(`🚀 Servidor Express rodando na porta ${PORT}`);

}); 



2º - Criação do Service




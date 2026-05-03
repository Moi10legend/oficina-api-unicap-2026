\# Para criar o projeto node.js aceitando de forma rápida, sem precisar configurar passo a passo.

**npm init -y**

\#Para instalar o express

**npm install express**

\#Para instalar o TypeScript e suas tipagens

**npm install -D typescript @types/express @types/node tsx**

1º Criação do tsconfig (Configuração no arquivo tsconfig.txt)

src/

&#x20;┣ 📂 controllers/

&#x20;┃ ┗ 📜 movieController.ts

&#x20;┣ 📂 services/

&#x20;┃ ┗ 📜 movieService.ts

&#x20;┣ 📂 routes/

&#x20;┃ ┗ 📜 movieRoutes.ts

&#x20;┗ 📜 server.ts



3º - Criação do server.ts

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



4º - Criação do Service com um array representando o banco de dados.
5º - Criação do Controller
6º - Crição do Routes
7º - Teste das rotas no Insomnia

8º - Instalação do Prisma
npm install -D prisma @types/better-sqlite3
npm install @prisma/client @prisma/adapter-better-sqlite3 dotenv
\#Criação da pasta prisma, prisma.config.ts e .env
npx prisma init --datasource-provider sqlite

9º importação do env em "import { defineConfig, env } from "prisma/config";" no arquivo config do prisma

10º modelagem da tabela de filmes
\# Para criação do banco e tabela de filmes
npx prisma migrate dev --name init

11º Geração do Prisma Client
npx prisma generate

12º Refatoração do Service para persistir os dados no banco.
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export const movieService = {
  getAllMovies: async () => {
    // Sai o array, entra o Prisma
    return await prisma.movie.findMany();
  },
  createMovie: async (title: string, year: number) => {
    // Sai o push no array, entra o Prisma
    return await prisma.movie.create({
      data: { title, year }
    });
  }
};

13º Criar os filmes "O Agente Secreto" e "O Auto da Compadecida" no Insomnia
Capa do Agente Secreto: https://upload.wikimedia.org/wikipedia/pt/6/60/O_Agente_Secreto_%28Cartaz_brasileiro%29.jpg
Capa do Auto da Compadecida: https://upload.wikimedia.org/wikipedia/pt/thumb/b/bf/O_auto_da_compadecida.jpg/250px-O_auto_da_compadecida.jpg

14º Subir o front-end e mostrar o filmes aparecendo. Adicionar Bacurau:
ano: 2019
capa: https://upload.wikimedia.org/wikipedia/pt/6/67/Bacurau_%28filme%29.jpeg

\# Para refazer o banco de dados a partir de migrações já existentes:
npx prisma migrate dev
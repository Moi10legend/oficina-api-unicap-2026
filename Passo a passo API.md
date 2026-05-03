\# Para criar o projeto node.js aceitando de forma rápida, sem precisar configurar passo a passo.  

**npm init -y**  

\#Para instalar o express  

**npm install express**  

\#Para instalar o TypeScript e suas tipagens  

**npm install -D typescript @types/express @types/node tsx**  

1º Criação do tsconfig (Configuração no arquivo tsconfig.txt)  
```Typescript
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "rootDir": "",
    "esModuleInterop": true,
    "strict": true,
    "ignoreDeprecations": "6.0",
  },
  "include": ["src/**/*"],
}
```

src/

&#x20;┣ 📂 controllers/

&#x20;┃ ┗ 📜 movieController.ts

&#x20;┣ 📂 services/

&#x20;┃ ┗ 📜 movieService.ts

&#x20;┣ 📂 routes/

&#x20;┃ ┗ 📜 movieRoutes.ts

&#x20;┗ 📜 server.ts



3º - Criação do server.ts

```Typescript
import express from 'express';

const app = express();

app.use(express.json());

app.get('/', (req, res) => {
    message: `🚀 Servidor rodando em http://localhost:${PORT}`
});

const PORT = 3000;

app.listen(PORT, () => {

&#x20;   console.log(`🚀 Servidor Express rodando na porta ${PORT}`);
}); 
```
4º - Criação do Service com um array representando o banco de dados.  
```typescript
let movies = [{id:1, title:"O Auto da Compadecida", year:2000, cover_url:"hhttps://upload.wikimedia.org/wikipedia/pt/thumb/b/bf/O_auto_da_compadecida.jpg/250px-O_auto_da_compadecida.jpg"}]

export class MovieServices{
    async getAllMovies(){
        return movies;
    }
    async createMovie(title:string, year:number, cover:string){
        // const newMovie = {id: movies.length + 1, title: title, year: year, cover: cover};
        // movies.push(newMovie);
        return await prisma.movie.create({
            data: {title, year, cover}
        });
    }
    async deleteMovie(id: number){
        movies.forEach((movie) => {
            if(movie.id == id){
                movies.splice(movies.indexOf(movie), 1)
            }
        })
    }
}
```

5º - Criação do Controller  
```typescript
import type {Request, Response} from 'express';
import { MovieServices } from '../services/movieServices.js';

const movieServices = new MovieServices();

export class MoviesController{
    async list(req: Request, res: Response){
        const movies = await movieServices.getAllMovies();
        res.json(movies);
    }

    async create(req: Request, res: Response){
        const {title, year, cover} = req.body;
        const newMovie = await movieServices.createMovie(title, year, cover);
        res.status(201).json(newMovie);
    }

    async delete(req: Request, res: Response){
        const id = Number(req.params.id);
        movieServices.deleteMovie(id);
        res.status(200).json({ message: 'Filme deletado com sucesso!' });
    }
}
```

6º - Crição do Routes  
```typescript
import type {Request, Response} from 'express';
import { MovieServices } from '../services/movieServices.js';

const movieServices = new MovieServices();

export class MoviesController{
    async list(req: Request, res: Response){
        const movies = await movieServices.getAllMovies();
        res.json(movies);
    }

    async create(req: Request, res: Response){
        const {title, year, cover} = req.body;
        const newMovie = await movieServices.createMovie(title, year, cover);
        res.status(201).json(newMovie);
    }

    async delete(req: Request, res: Response){
        const id = Number(req.params.id);
        movieServices.deleteMovie(id);
        res.status(200).json({ message: 'Filme deletado com sucesso!' });
    }
}
```

7º - Importação do router no server.ts e Teste das rotas no Insomnia  
```typescript
import router from './routes/movieRoutes.js';

app.use(router);
```

8º - Instalação do Prisma  
```bash
npm install -D prisma @types/better-sqlite3
npm install @prisma/client @prisma/adapter-better-sqlite3 dotenv
\#Criação da pasta prisma, prisma.config.ts e .env
npx prisma init --datasource-provider sqlite
```

9º importação do env em "import { defineConfig, env } from "prisma/config";" no arquivo config do prisma e criação da tabela movie

```prisma
model Movie{
  id Int @id @default(autoincrement())
  title String
  year Int
  cover String
}
```

10º modelagem da tabela de filmes  
\# Para criação do banco e tabela de filmes  
npx prisma migrate dev --name init

11º Geração do Prisma Client  
npx prisma generate

12º Refatoração do Service para persistir os dados no banco.  
Arquivo prismaClient.ts:  
```Typescript
import "dotenv/config";
import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3";
import { PrismaClient } from "../generated/client";

const connectionString = `${process.env.DATABASE_URL}`;

const adapter = new PrismaBetterSqlite3({ url: connectionString });
const prisma = new PrismaClient({ adapter });

export { prisma };
```

Arquivo movieService.ts:
```Typescript
import { prisma } from "../database/prismaClient"
export class MovieServices{
    async getAllMovies(){
        return await prisma.movie.findMany();
    }

    async createMovie(title:string, year:number, cover:string){
        return await prisma.movie.create({
            data: {title, year, cover}
        });
    }

    async deleteMovie(id: number){
        return await prisma.movie.delete({
            where: {
                id: id,
            }
        })
    }
};
```

13º Criar os filmes "O Agente Secreto" e "O Auto da Compadecida" no Insomnia  
Filme O Agente Secreto: 
```json
{
    "title": "O Agente Secreto",
    "year": 2025,
    "cover_url": "https://upload.wikimedia.org/wikipedia/pt/6/60/O_Agente_Secreto_%28Cartaz_brasileiro%29.jpg"
}
```
Filme O Auto da Compadecida:
```json
{
    "title": "O Auto da Compadecida",
    "year": 2000,
    "cover_url": "hhttps://upload.wikimedia.org/wikipedia/pt/thumb/b/bf/O_auto_da_compadecida.jpg/250px-O_auto_da_compadecida.jpg"
}
```

14º Subir o front-end e mostrar o filmes aparecendo. Adicionar Bacurau:
```json
{
    "title": "Bacurau",
    "year": 2019,
    "cover_url": "https://upload.wikimedia.org/wikipedia/pt/6/67/Bacurau_%28filme%29.jpeg"
}
```
\# Para refazer o banco de dados a partir de migrações já existentes:
npx prisma migrate dev

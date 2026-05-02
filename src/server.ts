import express from 'express';
import cors from 'cors'
import router from './routes/movieRoutes.js'

const app = express();
app.use(express.json());

app.use(cors())
app.use(router);

app.get('/', (req, res) => {
  res.json({ message: '🚀 Servidor rodando em http://localhost:${PORT}' });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor Express rodando em http://localhost:${PORT}`)
})


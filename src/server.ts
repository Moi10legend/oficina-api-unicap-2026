import express from 'express';

const app = express();
app.use(express.json());

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor Express rodando na porta ${PORT}`)
})

app.get('/', (req, res) => {
  res.json({ message: 'Arena 26 API is running' });
});
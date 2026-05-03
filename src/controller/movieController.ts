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
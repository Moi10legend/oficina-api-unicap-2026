import {Router} from 'express';
import { MoviesController } from '../controller/movieController.js';

const router = Router();
const moviesController = new MoviesController();

router.get('/movies', moviesController.list);
router.post('/movie', moviesController.create);
router.delete('/movie/:id', moviesController.delete)

export default router;
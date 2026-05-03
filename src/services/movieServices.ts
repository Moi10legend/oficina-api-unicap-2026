import { prisma } from "../database/prismaClient"

// let movies = [
//     {id: 1, 
//      title:"O Auto da Compadecida", 
//      year:2000, 
//      cover:"https://pt.wikipedia.org/wiki/O_Auto_da_Compadecida_%28filme%29"}
//     ];

export class MovieServices{
    async getAllMovies(){
        // return movies;
        return await prisma.movie.findMany();
    }

    async createMovie(title:string, year:number, cover:string){
        // const newMovie = {id: movies.length + 1, title: title, year: year, cover: cover};
        // movies.push(newMovie);
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
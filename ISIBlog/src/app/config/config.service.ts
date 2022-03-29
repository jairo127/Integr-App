import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommentBean, comments } from 'src/beans/comment';

class CommentHttp {
    auteur: string;
    titre: string;
    contenu: string;
    constructor(auteur: string, titre: string, contenu: string) {
        this.auteur = auteur;
        this.titre = titre;
        this.contenu = contenu;
    }
}

@Injectable()
export class ConfigService {

    constructor(private http: HttpClient) { }

    clearComments() {
        while (comments.length > 0) {
            comments.pop();
        }
    }

    insertComment(comment: CommentBean): Observable<any> {
        const header = {'Content-Type': 'application/json'};
        const body = JSON.stringify(new CommentHttp(comment.auteur, comment.titre, comment.contenu))
        return this.http.post("http://localhost:5000/", body, { headers: header });
    }

    getComments() {
        return this.http.get<CommentBean[]>("http://localhost:5000/").subscribe(data => {
            this.clearComments();
            data.forEach(item => {
                comments.push(new CommentBean(item.id, item.auteur, item.titre, item.contenu, item.dateCreation));
            });
        });
    }

    deleteComment(id: number): Observable<any> {
        return this.http.delete("http://localhost:5000/"+id);
    }
}
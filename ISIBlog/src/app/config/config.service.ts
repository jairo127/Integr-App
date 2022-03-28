import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CommentBean } from 'src/beans/comment';

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

    insertComment(comment: CommentBean): Observable<any> {
        const header = {'Content-Type': 'application/json'};
        const body = JSON.stringify(new CommentHttp(comment.auteur, comment.titre, comment.contenu))
        return this.http.post("http://localhost:5000/", body, { headers: header });
    }

    getComments(): Observable<any> {
        return this.http.get("http://localhost:5000/");
    }
}
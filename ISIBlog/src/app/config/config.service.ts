import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommentBean } from 'src/beans/comment';

@Injectable()
export class ConfigService {
    constructor(private http: HttpClient) { }

    insertComment(comment: CommentBean) {
        let body = {
            auteur: comment.auteur,
            titre: comment.titre
        }
        this.http.post<any>("localhost:5000", body).subscribe();
    }
}
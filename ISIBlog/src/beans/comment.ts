export class CommentBean {
    public id: number;
    public auteur: string;
    public titre: string;
    public contenu: string;
    public dateCreation: string;

    constructor(id: number, auteur: string, titre: string, contenu: string, dateCreation: string) {
        this.id = id;
        this.auteur = auteur;
        this.titre = titre;
        this.contenu = contenu;
        this.dateCreation = dateCreation;
    }
}

export var comments: CommentBean[] = new Array<CommentBean>();
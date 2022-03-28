export class CommentBean {
    public id: number;
    public auteur: string;
    public titre: string;
    public contenu: string;
    public dateCreation: Date;

    constructor(id: number, auteur: string, titre: string, contenu: string, dateCreation: Date) {
        this.id = id;
        this.auteur = auteur;
        this.titre = titre;
        this.contenu = contenu;
        this.dateCreation = dateCreation;
    }
}
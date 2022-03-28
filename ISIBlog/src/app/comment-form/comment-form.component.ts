import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../config/config.service';
import { CommentBean } from './../../beans/comment';

@Component({
  selector: 'app-comment-form',
  templateUrl: './comment-form.component.html',
  styleUrls: ['./comment-form.component.scss'],
  providers: [ConfigService]
})
export class CommentFormComponent implements OnInit {

  displayForm: boolean;

  comment: CommentBean;

  constructor(private config: ConfigService) { }

  ngOnInit(): void {
    this.displayForm = false;
    this.comment = new CommentBean(0, "", "", "", null);
  }

  sendComment() {
    this.config.insertComment(this.comment).subscribe(data => {
      this.displayForm = false;
    });
  }

}

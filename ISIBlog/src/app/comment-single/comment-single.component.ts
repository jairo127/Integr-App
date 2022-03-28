import { Component, Input, OnInit } from '@angular/core';
import { CommentBean } from 'src/beans/comment';
import { ConfigService } from '../config/config.service';

@Component({
  selector: 'app-comment-single',
  templateUrl: './comment-single.component.html',
  styleUrls: ['./comment-single.component.scss'],
  providers: [ConfigService]
})
export class CommentSingleComponent implements OnInit {

  @Input() comment: CommentBean;

  constructor(private config: ConfigService) { }

  ngOnInit(): void {
  }

  deleteComment() {
    this.config.deleteComment(this.comment.id).subscribe(data => {
      this.config.getComments();
    });
  }

}

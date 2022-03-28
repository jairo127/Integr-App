import { Component, OnInit } from '@angular/core';
import { ConfigService } from '../config/config.service';
import { CommentBean, comments } from 'src/beans/comment';

@Component({
  selector: 'app-comment-list',
  templateUrl: './comment-list.component.html',
  styleUrls: ['./comment-list.component.scss'],
  providers: [ConfigService]
})
export class CommentListComponent implements OnInit {

  constructor(private config: ConfigService) { }

  ngOnInit(): void {
    this.config.getComments();
  }

  comments(): CommentBean[] {
    return comments;
  }

}

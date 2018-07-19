import { Data } from '../../models/Data';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.scss']
})
export class DataComponent implements OnInit {

  @Input()
  public data: Data;
  
  constructor() { }

  ngOnInit() {
  }

}

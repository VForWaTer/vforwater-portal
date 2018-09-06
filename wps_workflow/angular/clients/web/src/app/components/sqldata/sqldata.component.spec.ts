import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SQLDataComponent } from './sqldata.component';

describe('SQLDataComponent', () => {
  let component: SQLDataComponent;
  let fixture: ComponentFixture<SQLDataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SQLDataComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SQLDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

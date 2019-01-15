import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ResultDialogComponent } from './result-dialog.component';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material';

xdescribe('ResultDialogComponent', () => {
  let component: ResultDialogComponent;
  let fixture: ComponentFixture<ResultDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        ResultDialogComponent,
        FormsModule,
        MatFormFieldModule,
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ResultDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProcessDialogComponent } from './process-dialog.component';

xdescribe('ProcessDialogComponent', () => {
  let component: ProcessDialogComponent;
  let fixture: ComponentFixture<ProcessDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ProcessDialogComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProcessDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

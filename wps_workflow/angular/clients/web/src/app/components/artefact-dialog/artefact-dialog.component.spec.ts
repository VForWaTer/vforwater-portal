import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArtefactDialogComponent } from './artefact-dialog.component';
import { MatFormFieldModule, MatDialogModule, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { FormsModule } from '@angular/forms';

xdescribe('ArtefactDialogComponent', () => {
  let component: ArtefactDialogComponent;
  let fixture: ComponentFixture<ArtefactDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ArtefactDialogComponent],
      imports: [
        MatFormFieldModule,
        MatDialogModule,
        FormsModule
      ],
      providers: [
        { provide: MatDialogRef, useValue: {} },
        { provide: MAT_DIALOG_DATA, useValue: {} }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArtefactDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

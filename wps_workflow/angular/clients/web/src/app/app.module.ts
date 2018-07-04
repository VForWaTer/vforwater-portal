import {
  MatIconModule, MatInputModule, MatButtonModule, MatCheckboxModule, MatToolbarModule, MatTabsModule,
  MatFormFieldModule, MatCardModule, MatListModule, MatTooltipModule, MatChipsModule, MatDialogModule,
  MatExpansionModule, MatOptionModule, MatSelectModule, MatMenuModule, MatSnackBarModule, MatProgressSpinnerModule
} from '@angular/material';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { FlexLayoutModule } from '@angular/flex-layout';
import { NgModule, LOCALE_ID } from '@angular/core';
import { EditorPageComponent } from 'app/pages/editor-page/editor-page.component';
import { WorkflowsPageComponent } from 'app/pages/workflows-page/workflows-page.component';
import { AppComponent } from 'app/components/app/app.component';
import { ProcessListComponent } from 'app/components/process-list/process-list.component';
import { ProcessDialogComponent } from 'app/components/process-dialog/process-dialog.component';
import { TaskComponent } from 'app/components/task/task.component';
import { EditorComponent } from 'app/components/editor/editor.component';
import { ProcessComponent } from 'app/components/process/process.component';
import { HttpClientModule } from '@angular/common/http';
import { ProcessService } from 'app/services/process.service';
import { WorkflowService } from 'app/services/workflow.service';
import { WpsService } from 'app/services/wps.service';
import { SettingsPageComponent } from 'app/pages/settings-page/settings-page.component';
import { ArtefactDialogComponent } from 'app/components/artefact-dialog/artefact-dialog.component';
import { FormsModule } from '@angular/forms';
import { ResultDialogComponent } from 'app/components/result-dialog/result-dialog.component';
import { LoginPageComponent } from 'app/pages/login-page/login-page.component';
import { UserService } from 'app/services/user.service';



const routes = [
  { path: '', component: EditorPageComponent },
  { path: 'editor', component: EditorPageComponent },
  { path: 'editor/:id', component: EditorPageComponent },
  { path: 'workflows', component: WorkflowsPageComponent },
  { path: 'settings', component: SettingsPageComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'logout', component: LoginPageComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    EditorPageComponent,
    WorkflowsPageComponent,
    SettingsPageComponent,
    LoginPageComponent,
    ProcessListComponent,
    ProcessComponent,
    ProcessDialogComponent,
    ArtefactDialogComponent,
    ResultDialogComponent,
    EditorComponent,
    TaskComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    FlexLayoutModule,
    MatButtonModule,
    MatCheckboxModule,
    MatToolbarModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatCardModule,
    MatListModule,
    MatTooltipModule,
    MatChipsModule,
    MatDialogModule,
    MatExpansionModule,
    MatOptionModule,
    MatSelectModule,
    MatMenuModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    FormsModule
  ],
  entryComponents: [
    ProcessDialogComponent,
    ArtefactDialogComponent,
    ResultDialogComponent
  ],
  providers: [
    ProcessService,
    WorkflowService,
    WpsService,
    UserService,
    { provide: LOCALE_ID, useValue: 'en' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

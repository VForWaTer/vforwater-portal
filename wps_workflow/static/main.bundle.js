webpackJsonp(["main"],{

/***/ "../../../../../src/$$_lazy_route_resource lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_animations__ = __webpack_require__("../../../platform-browser/esm5/animations.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_platform_browser__ = __webpack_require__("../../../platform-browser/esm5/platform-browser.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_flex_layout__ = __webpack_require__("../../../flex-layout/esm5/flex-layout.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_app_pages_editor_page_editor_page_component__ = __webpack_require__("../../../../../src/app/pages/editor-page/editor-page.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7_app_pages_workflows_page_workflows_page_component__ = __webpack_require__("../../../../../src/app/pages/workflows-page/workflows-page.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_app_components_app_app_component__ = __webpack_require__("../../../../../src/app/components/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9_app_components_process_list_process_list_component__ = __webpack_require__("../../../../../src/app/components/process-list/process-list.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10_app_components_process_dialog_process_dialog_component__ = __webpack_require__("../../../../../src/app/components/process-dialog/process-dialog.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11_app_components_task_task_component__ = __webpack_require__("../../../../../src/app/components/task/task.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12_app_components_editor_editor_component__ = __webpack_require__("../../../../../src/app/components/editor/editor.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13_app_components_process_process_component__ = __webpack_require__("../../../../../src/app/components/process/process.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_16_app_services_workflow_service__ = __webpack_require__("../../../../../src/app/services/workflow.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_17_app_services_wps_service__ = __webpack_require__("../../../../../src/app/services/wps.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_18_app_pages_settings_page_settings_page_component__ = __webpack_require__("../../../../../src/app/pages/settings-page/settings-page.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_19_app_components_artefact_dialog_artefact_dialog_component__ = __webpack_require__("../../../../../src/app/components/artefact-dialog/artefact-dialog.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_20__angular_forms__ = __webpack_require__("../../../forms/esm5/forms.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_21_app_components_result_dialog_result_dialog_component__ = __webpack_require__("../../../../../src/app/components/result-dialog/result-dialog.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_22_app_pages_login_page_login_page_component__ = __webpack_require__("../../../../../src/app/pages/login-page/login-page.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_23_app_services_user_service__ = __webpack_require__("../../../../../src/app/services/user.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
























var routes = [
    { path: '', component: __WEBPACK_IMPORTED_MODULE_6_app_pages_editor_page_editor_page_component__["a" /* EditorPageComponent */] },
    { path: 'editor', component: __WEBPACK_IMPORTED_MODULE_6_app_pages_editor_page_editor_page_component__["a" /* EditorPageComponent */] },
    { path: 'editor/:id', component: __WEBPACK_IMPORTED_MODULE_6_app_pages_editor_page_editor_page_component__["a" /* EditorPageComponent */] },
    { path: 'workflows', component: __WEBPACK_IMPORTED_MODULE_7_app_pages_workflows_page_workflows_page_component__["a" /* WorkflowsPageComponent */] },
    { path: 'settings', component: __WEBPACK_IMPORTED_MODULE_18_app_pages_settings_page_settings_page_component__["a" /* SettingsPageComponent */] },
    { path: 'login', component: __WEBPACK_IMPORTED_MODULE_22_app_pages_login_page_login_page_component__["a" /* LoginPageComponent */] },
    { path: 'logout', component: __WEBPACK_IMPORTED_MODULE_22_app_pages_login_page_login_page_component__["a" /* LoginPageComponent */] },
];
var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_5__angular_core__["K" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_8_app_components_app_app_component__["a" /* AppComponent */],
                __WEBPACK_IMPORTED_MODULE_6_app_pages_editor_page_editor_page_component__["a" /* EditorPageComponent */],
                __WEBPACK_IMPORTED_MODULE_7_app_pages_workflows_page_workflows_page_component__["a" /* WorkflowsPageComponent */],
                __WEBPACK_IMPORTED_MODULE_18_app_pages_settings_page_settings_page_component__["a" /* SettingsPageComponent */],
                __WEBPACK_IMPORTED_MODULE_22_app_pages_login_page_login_page_component__["a" /* LoginPageComponent */],
                __WEBPACK_IMPORTED_MODULE_9_app_components_process_list_process_list_component__["a" /* ProcessListComponent */],
                __WEBPACK_IMPORTED_MODULE_13_app_components_process_process_component__["a" /* ProcessComponent */],
                __WEBPACK_IMPORTED_MODULE_10_app_components_process_dialog_process_dialog_component__["a" /* ProcessDialogComponent */],
                __WEBPACK_IMPORTED_MODULE_19_app_components_artefact_dialog_artefact_dialog_component__["a" /* ArtefactDialogComponent */],
                __WEBPACK_IMPORTED_MODULE_21_app_components_result_dialog_result_dialog_component__["a" /* ResultDialogComponent */],
                __WEBPACK_IMPORTED_MODULE_12_app_components_editor_editor_component__["a" /* EditorComponent */],
                __WEBPACK_IMPORTED_MODULE_11_app_components_task_task_component__["a" /* TaskComponent */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_2__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_animations__["a" /* BrowserAnimationsModule */],
                __WEBPACK_IMPORTED_MODULE_3__angular_router__["d" /* RouterModule */].forRoot(routes),
                __WEBPACK_IMPORTED_MODULE_14__angular_common_http__["b" /* HttpClientModule */],
                __WEBPACK_IMPORTED_MODULE_4__angular_flex_layout__["a" /* FlexLayoutModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["b" /* MatButtonModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["d" /* MatCheckboxModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["v" /* MatToolbarModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["u" /* MatTabsModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["j" /* MatFormFieldModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["l" /* MatInputModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["k" /* MatIconModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["c" /* MatCardModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["m" /* MatListModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["w" /* MatTooltipModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["e" /* MatChipsModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["g" /* MatDialogModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["i" /* MatExpansionModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["p" /* MatOptionModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["r" /* MatSelectModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["n" /* MatMenuModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["t" /* MatSnackBarModule */],
                __WEBPACK_IMPORTED_MODULE_0__angular_material__["q" /* MatProgressSpinnerModule */],
                __WEBPACK_IMPORTED_MODULE_20__angular_forms__["c" /* FormsModule */]
            ],
            entryComponents: [
                __WEBPACK_IMPORTED_MODULE_10_app_components_process_dialog_process_dialog_component__["a" /* ProcessDialogComponent */],
                __WEBPACK_IMPORTED_MODULE_19_app_components_artefact_dialog_artefact_dialog_component__["a" /* ArtefactDialogComponent */],
                __WEBPACK_IMPORTED_MODULE_21_app_components_result_dialog_result_dialog_component__["a" /* ResultDialogComponent */]
            ],
            providers: [
                __WEBPACK_IMPORTED_MODULE_15_app_services_process_service__["a" /* ProcessService */],
                __WEBPACK_IMPORTED_MODULE_16_app_services_workflow_service__["a" /* WorkflowService */],
                __WEBPACK_IMPORTED_MODULE_17_app_services_wps_service__["a" /* WpsService */],
                __WEBPACK_IMPORTED_MODULE_23_app_services_user_service__["a" /* UserService */],
                { provide: __WEBPACK_IMPORTED_MODULE_5__angular_core__["I" /* LOCALE_ID */], useValue: 'en' }
            ],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_8_app_components_app_app_component__["a" /* AppComponent */]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "../../../../../src/app/components/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "<mat-toolbar color=\"primary\" class=\"navbar\">\n    <img class=\"logo\" src=\"static/assets/img/logo.png\" alt=\"logo\">\n\n    <nav *ngIf=\"showNav\" class=\"tab-nav\">\n        <a routerLink=\"editor\" style=\"text-transform:uppercase;\" mat-button i18n=\"@@editor_header\">Editor</a>\n        <a routerLink=\"workflows\" style=\"text-transform:uppercase;\" mat-button i18n=\"@@workflows_header\">Workflows</a>\n        <a routerLink=\"settings\" style=\"text-transform:uppercase;\" mat-button i18n=\"@@settings_header\">Settings</a>\n    </nav>\n</mat-toolbar>\n<div class=\"content\">\n    <router-outlet></router-outlet>\n</div>"

/***/ }),

/***/ "../../../../../src/app/components/app/app.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".content {\n  margin-top: 48px;\n  height: calc(100vh - 48px); }\n\n.navbar {\n  max-height: 48px;\n  border-bottom: 2px solid #00796B;\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  z-index: 2; }\n\n.tab-nav {\n  width: calc(90% - 116px);\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-pack: center;\n      -ms-flex-pack: center;\n          justify-content: center;\n  color: rgba(255, 255, 255, 0.87); }\n\n.logo {\n  height: 34px;\n  cursor: pointer; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_services_user_service__ = __webpack_require__("../../../../../src/app/services/user.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



/**
 * App Component.
 *
 * @export
 * @class AppComponent
 */
var AppComponent = (function () {
    /**
     * Creates an instance of AppComponent.
     *
     * @param {Router} router
     * @param {UserService} userService
     * @memberof AppComponent
     */
    function AppComponent(router, userService) {
        var _this = this;
        this.router = router;
        this.userService = userService;
        this.showNav = true;
        userService.get()
            .subscribe(function (user) {
            if (user['error']) {
                _this.router.navigate(['/login']);
            }
        }, function (err) { return _this.router.navigate(['/login']); });
        // Hide navigation bar when user is on /login
        this.router.events.subscribe(function (route) {
            if (route instanceof __WEBPACK_IMPORTED_MODULE_1__angular_router__["b" /* NavigationEnd */]) {
                if (route.url === '/login') {
                    _this.showNav = false;
                }
                else {
                    _this.showNav = true;
                }
            }
        });
    }
    AppComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-root',
            template: __webpack_require__("../../../../../src/app/components/app/app.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/app/app.component.scss")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_router__["c" /* Router */], __WEBPACK_IMPORTED_MODULE_2_app_services_user_service__["a" /* UserService */]])
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/artefact-dialog/artefact-dialog.component.html":
/***/ (function(module, exports) {

module.exports = "<h2 mat-dialog-title> {{ parameter.title }}</h2>\n\n<div class=\"badges\" *ngIf=\"parameter\">\n  <span class=\"badge\">{{ parameter.role }}</span>\n  <span *ngIf=\"getTypeInfo(parameter.type); let info\" class=\"badge\" [style.color]=\"info[1]\" [style.borderColor]=\"info[1]\">{{ info[0] }}</span>\n</div>\n\n<mat-dialog-content *ngIf=\"parameter\" class=\"content\">\n  <!-- INPUT -->\n  <div *ngIf=\"parameter.role === 'input'\" class=\"type-container\" [ngSwitch]=\"parameter.type\">\n    <p class=\"abstract\" *ngIf=\"parameter.abstract\">{{ parameter.abstract }}</p>\n\n    <div [style.display]=\"editMode ? 'block' : 'none'\">\n      <!-- Literal Input -->\n      <ng-container *ngSwitchCase=\"0\">\n        <mat-form-field class=\"data-field\">\n          <input type=\"text\" matInput [(ngModel)]=\"data.value\" placeholder=\"Input Value\">\n          <mat-hint>Format: {{ data.format | uppercase }}</mat-hint>\n        </mat-form-field>\n      </ng-container>\n\n      <!-- Compley Input -->\n      <ng-container *ngSwitchCase=\"1\">\n        <mat-form-field class=\"data-field\">\n          <textarea matInput [(ngModel)]=\"data.value\" placeholder=\"Input Data\" matTextareaAutosize matAutosizeMinRows=\"5\"></textarea>\n        </mat-form-field>\n      </ng-container>\n\n      <!-- Bounding Box Input -->\n      <ng-container *ngSwitchCase=\"2\">\n        <mat-form-field class=\"data-field-small\">\n          <input matInput [(ngModel)]=\"data.ux\" placeholder=\"UpperCorner X\" type=\"number\">\n        </mat-form-field>\n        <mat-form-field class=\"data-field-small\">\n          <input matInput [(ngModel)]=\"data.uy\" placeholder=\"UpperCorner Y\" type=\"number\">\n        </mat-form-field>\n        <mat-form-field class=\"data-field-small\">\n          <input matInput [(ngModel)]=\"data.lx\" placeholder=\"LowerCorner X\" type=\"number\">\n        </mat-form-field>\n        <mat-form-field class=\"data-field-small\">\n          <input matInput [(ngModel)]=\"data.ly\" placeholder=\"LowerCorner Y\" type=\"number\">\n        </mat-form-field>\n      </ng-container>\n    </div>\n  </div>\n\n  <!-- OUTPUT -->\n  <div *ngIf=\"parameter.role === 'output'\" class=\"type-container\">\n\n    <pre class=\"output\">{{ this.data.value }}</pre>\n  </div>\n\n</mat-dialog-content>\n\n<mat-dialog-actions fxLayout=\"row\" fxLayoutAlign=\"end\">\n  <button mat-button mat-dialog-close i18n=\"@@close\">Close</button>\n\n  <ng-container *ngIf=\"parameter.role === 'input'\">\n    <button *ngIf=\"deletable\" mat-button (click)=\"remove()\" i18n=\"@@delete\" color=\"warn\">DELETE</button>\n    <button mat-raised-button (click)=\"save()\" i18n=\"@@save\" color=\"primary\" [disabled]=\"!valid\">SAVE</button>\n  </ng-container>\n</mat-dialog-actions>"

/***/ }),

/***/ "../../../../../src/app/components/artefact-dialog/artefact-dialog.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  display: block;\n  position: relative; }\n\n.content {\n  width: 40vw; }\n\n.badges {\n  position: absolute;\n  top: 3px;\n  right: 3px; }\n\n.badge {\n  float: right;\n  padding: 3px 5px;\n  border: solid 1px #385160;\n  border-radius: 3px;\n  font-size: 13px;\n  text-transform: uppercase;\n  margin: 3px; }\n\n.abstract {\n  color: #595959; }\n\n.data-field {\n  width: calc(100% - 16px);\n  background: #F9F9F9;\n  border-radius: 3px;\n  padding: 8px; }\n\n.type-container {\n  margin: 3px 0 21px 0; }\n\n.subtitle {\n  line-height: 40px;\n  font-weight: bold;\n  color: #595959; }\n\n.data-field-small {\n  width: calc(50% - 21px);\n  background: #F9F9F9;\n  border-radius: 3px;\n  padding: 8px;\n  margin: 2px 0; }\n\n.output {\n  width: calc(100% - 16px);\n  background: #F9F9F9;\n  border-radius: 3px;\n  padding: 8px;\n  overflow: scroll; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/artefact-dialog/artefact-dialog.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ArtefactDialogComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__ = __webpack_require__("../../../../../src/app/models/ProcessParameter.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};




/**
 * Artefact Dialog Component.
 *
 * @export
 * @class ArtefactDialogComponent
 * @implements {OnInit}
 */
var ArtefactDialogComponent = (function () {
    /**
     * Creates an instance of ArtefactDialogComponent.
     *
     * @param {ArtefactDialogData} data
     * @param {MatDialogRef<ArtefactDialogComponent>} dialog
     * @memberof ArtefactDialogComponent
     */
    function ArtefactDialogComponent(data, dialog) {
        var _this = this;
        this.dialog = dialog;
        this.selectedFormat = 'markdown';
        this.data = {};
        this.editMode = true;
        this.deletable = false;
        this.task = data.task;
        this.parameter = data.parameter;
        if (!this.parameter || !this.task) {
            return;
        }
        // Get all artefacts of this tasks
        var artefacts = this.parameter.role === 'input'
            ? this.task.task.input_artefacts
            : this.task.task.output_artefacts;
        var artefact = artefacts.find(function (a) { return a.parameter_id === _this.parameter.id; });
        // Check if parameter has artefact
        if (artefact) {
            this.data['value'] = artefact.data;
            if (artefact.role === 'input') {
                this.data['format'] = this.parameter.format || 'string';
                if (this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX) {
                    var coords = artefact.data.split(';')
                        .map(function (value) { return value.split('=')[1]; })
                        .map(function (value) { return value.split(' '); });
                    this.data.ux = coords[0][0];
                    this.data.uy = coords[0][1];
                    this.data.lx = coords[1][0];
                    this.data.ly = coords[1][1];
                }
            }
            if (artefact.role === 'output') {
                this.data['format'] = artefact.format || 'string';
            }
        }
        else {
            this.data['format'] = this.parameter.format || 'string';
        }
        if (this.data.value) {
            this.deletable = true;
        }
    }
    /**
     * Component setup.
     *
     * @memberof ArtefactDialogComponent
     */
    ArtefactDialogComponent.prototype.ngOnInit = function () {
    };
    Object.defineProperty(ArtefactDialogComponent.prototype, "valid", {
        /**
         * Checks whether the user artefact data input is valid.
         *
         * @readonly
         * @type {boolean}
         * @memberof ArtefactDialogComponent
         */
        get: function () {
            if (this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].LITERAL) {
                // Check Literal Data
                if (!this.data.value || this.data.value.length === 0) {
                    return false;
                }
                switch (this.data.format) {
                    case 'string': return true;
                    case 'float': return !isNaN(this.data.value);
                    case 'integer': return /^-?[0-9]+$/.test(this.data.value);
                    default: return true; /* Match any type */
                }
            }
            else if (this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX) {
                // Check Compley Data
            }
            else if (this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX) {
                // Check Bounding Box Data
                // All fields must exist
                if (this.data.ux === undefined
                    || this.data.uy === undefined
                    || this.data.lx === undefined
                    || this.data.lx === undefined) {
                    return false;
                }
            }
            else {
                console.log("Error: Process Type Not Found " + this.parameter.type);
            }
            return true;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Returns name and color of artefact type.
     *
     * @param {number} type Type id
     * @returns {[string, string]} Name, Color pair
     * @memberof ArtefactDialogComponent
     */
    ArtefactDialogComponent.prototype.getTypeInfo = function (type) {
        return [__WEBPACK_IMPORTED_MODULE_3_app_services_process_service__["a" /* ProcessService */].getTypeName(type), __WEBPACK_IMPORTED_MODULE_3_app_services_process_service__["a" /* ProcessService */].getTypeColor(type)];
    };
    /**
     * Is used to change input of the different input types
     * as every input type requires different fields,
     * we have to differ between them
     *
     * @memberof ArtefactDialogComponent
     */
    ArtefactDialogComponent.prototype.clickEditButton = function () {
        var el = this.codeComponent.nativeElement;
        if (this.editMode) {
            el.className = '';
            el.innerHTML = '';
            var format = this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX
                ? this.selectedFormat
                : 'markdown';
            el.classList.add(format);
            var data = this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX
                ? "UpperCorner=" + this.data.ux + " " + this.data.uy + ";LowerCorner=" + this.data.lx + " " + this.data.ly
                : this.data.value;
            if (data) {
                el.appendChild(document.createTextNode(data));
            }
        }
        this.editMode = !this.editMode;
    };
    /**
     * Saves the artefacts modified input.
     *
     * @returns {void}
     * @memberof ArtefactDialogComponent
     */
    ArtefactDialogComponent.prototype.save = function () {
        if (!this.data) {
            return;
        }
        var out = {
            value: this.parameter.type === __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX
                ? "UpperCorner=" + this.data.ux + " " + this.data.uy + ";LowerCorner=" + this.data.lx + " " + this.data.ly
                : this.data.value,
            format: this.selectedFormat === 'markdown' ? 'plain' : this.selectedFormat
        };
        if (out.value && out.value.length > 0) {
            this.task.addArtefact(this.parameter, out);
        }
        this.dialog.close();
    };
    /**
     * Removes artefact from task.
     *
     * @memberof ArtefactDialogComponent
     */
    ArtefactDialogComponent.prototype.remove = function () {
        this.task.removeArtefact(this.parameter);
        this.dialog.close();
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('code'),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */])
    ], ArtefactDialogComponent.prototype, "codeComponent", void 0);
    ArtefactDialogComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-artefact-dialog',
            template: __webpack_require__("../../../../../src/app/components/artefact-dialog/artefact-dialog.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/artefact-dialog/artefact-dialog.component.scss")],
        }),
        __param(0, Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Inject */])(__WEBPACK_IMPORTED_MODULE_1__angular_material__["a" /* MAT_DIALOG_DATA */])),
        __metadata("design:paramtypes", [Object, __WEBPACK_IMPORTED_MODULE_1__angular_material__["h" /* MatDialogRef */]])
    ], ArtefactDialogComponent);
    return ArtefactDialogComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/editor/editor.component.html":
/***/ (function(module, exports) {

module.exports = "<ng-container>\n    <div #background class=\"background\" (dragover)=\"dragOver($event)\" (drop)=\"drop($event)\">\n\n        <ng-container *ngIf=\"processes && workflow\">\n\n            <svg viewBox=\"0 0 2000 2000\">\n                <svg:path *ngIf=\"movement.edge\" [attr.d]=\"getSvgEdge(movement.edge, true)\" stroke=\"#888888\" stroke-width=\"2\" fill=\"none\"\n                />\n                <svg:path *ngFor=\"let edge of edges\" [attr.d]=\"getSvgEdge(edge)\" stroke=\"#888888\" stroke-width=\"2\" fill=\"none\" class=\"edge\"\n                />\n                <svg:path *ngFor=\"let edge of edges\" [attr.d]=\"getSvgEdge(edge)\" fill=\"none\" stroke=\"#888888\" stroke-width=\"20\" stroke-opacity=\"0\"\n                    class=\"edge-big\" (mousedown)=\"clickEdge(edge)\" />\n            </svg>\n\n            <app-task @fade #AppTask *ngFor=\"let task of workflow.tasks; let i = index\" class=\"task\" [style.left.px]=\"task.x\" [style.top.px]=\"task.y\"\n                [process]=\"findProcess(task.process_id)\" [task]=\"task\" (mousedown)=\"dragStart(i, $event)\" (parameterDrag)=\"parameterDrag($event, AppTask)\"\n                (parameterDrop)=\"parameterDrop($event, AppTask)\" (taskRemove)=\"remove(task.id)\" [running]=\"running\" (changeArtefact)=\"changeArtefact($event)\"></app-task>\n        </ng-container>\n    </div>\n</ng-container>"

/***/ }),

/***/ "../../../../../src/app/components/editor/editor.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  display: block;\n  overflow: scroll;\n  -ms-overflow-style: none; }\n\n:host::-webkit-scrollbar {\n  display: none; }\n\n.background {\n  background-image: url(\"/static/assets/img/editor_bg.png\");\n  height: 2000px;\n  width: 2000px;\n  position: relative; }\n\n.task {\n  position: absolute; }\n\n.edge-big:hover {\n  cursor: -webkit-grab;\n  cursor: grab;\n  stroke: #b10000; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/editor/editor.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EditorComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_app_models_Task__ = __webpack_require__("../../../../../src/app/models/Task.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_components_task_task_component__ = __webpack_require__("../../../../../src/app/components/task/task.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_animations__ = __webpack_require__("../../../animations/esm5/animations.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




/**
 * Editor Component.
 *
 * @export
 * @class EditorComponent
 * @implements {OnInit}
 * @implements {AfterContentInit}
 */
var EditorComponent = (function () {
    /**
     * Creates an instance of EditorComponent.
     *
     * @param {ElementRef} el
     * @param {NgZone} zone
     * @param {ChangeDetectorRef} cd
     * @memberof EditorComponent
     */
    function EditorComponent(el, zone, cd) {
        this.el = el;
        this.zone = zone;
        this.cd = cd;
        this.movement = {};
        this.snapshots = [];
        this.workflowChanged = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.running = false;
    }
    /**
     * Component setup.
     *
     * @memberof EditorComponent
     */
    EditorComponent.prototype.ngOnInit = function () {
        // Create initial workflow if no workflow is provided
        if (!this.workflow) {
            this.empty();
        }
    };
    /**
     * Is Called after all child components are ready.
     *
     * @memberof EditorComponent
     */
    EditorComponent.prototype.ngAfterContentInit = function () {
        var _this = this;
        this.workflowChanged.emit(this.workflow);
        this.scrollToMiddle();
        setTimeout(function () { return _this.detectChanges(); }, 100);
        setTimeout(function () { return _this.detectChanges(); }, 1000);
    };
    /**
     * Empties snapshots
     *
     * @memberof EditorComponent
     */
    EditorComponent.prototype.empty = function () {
        this.snapshots = [];
        this.movement = {};
    };
    /**
     * Is called when an edge is clicked.
     *
     * @param edges the workflows edges
     */
    EditorComponent.prototype.clickEdge = function (edges) {
        // Delete edge
        if (this.running) {
            return;
        }
        var id = edges[4];
        var index = this.workflow.edges.findIndex(function (edge) { return edge.id === id; });
        if (index !== -1) {
            this.snapshot();
            this.workflow.edges.splice(index, 1);
            this.workflowChanged.emit(this.workflow);
        }
    };
    /**
     * Move canvas to the middle.
     *
     * @memberof EditorComponent
     */
    EditorComponent.prototype.scrollToMiddle = function () {
        var native = this.el.nativeElement;
        native.scrollTo(500, 500);
    };
    /**
     * Changes an artefact.
     *
     * @param event the event that triggers the call
     */
    EditorComponent.prototype.changeArtefact = function (event) {
        this.snapshot();
        var task = event[0].task;
        task = this.workflow.tasks.find(function (t) { return t.id === task.id; });
        var parameter = event[0].parameter;
        if (event[1] === null) {
            // Remove Artefact
            var index = task.input_artefacts.findIndex(function (artefact) { return artefact.parameter_id === parameter.id; });
            if (index < 0) {
                return;
            }
            task.input_artefacts.splice(index, 1);
        }
        else {
            var changed = false;
            for (var _i = 0, _a = task.input_artefacts; _i < _a.length; _i++) {
                var entry = _a[_i];
                if (entry.parameter_id === event[0].parameter.id) {
                    entry.data = event[1].value;
                    entry.updated_at = (new Date).getTime();
                    changed = true;
                }
            }
            if (!changed) {
                // Add artefact
                var data = event[1];
                if (parameter.role === 'input') {
                    task.input_artefacts = task.input_artefacts || [];
                    task.input_artefacts.push({
                        parameter_id: parameter.id,
                        task_id: task.id,
                        workflow_id: this.workflow.id,
                        role: parameter.role,
                        format: data.format,
                        data: data.value,
                        created_at: (new Date).getTime(),
                        updated_at: (new Date).getTime(),
                    });
                }
            }
            for (var _b = 0, _c = task.input_artefacts; _b < _c.length; _b++) {
                var currentInputArtefact = _c[_b];
                var _loop_1 = function (currentEdge) {
                    if (currentEdge.to_task_id === currentInputArtefact.task_id && currentInputArtefact.parameter_id === currentEdge.input_id) {
                        this_1.workflow.edges = this_1.workflow.edges.filter(function (e) { return e !== currentEdge; });
                    }
                };
                var this_1 = this;
                for (var _d = 0, _e = this.workflow.edges; _d < _e.length; _d++) {
                    var currentEdge = _e[_d];
                    _loop_1(currentEdge);
                }
            }
        }
        this.workflowChanged.emit(this.workflow);
    };
    /**
     * Returns edge as svg string.
     *
     * @param edge the edge
     * @param mouse the mouse
     */
    EditorComponent.prototype.getSvgEdge = function (edge, mouse) {
        if (mouse === void 0) { mouse = false; }
        var delta = Math.abs(edge[1] - edge[3]);
        if (mouse === true && this.movement.parameter !== undefined) {
            delta *= this.movement.parameter.role === 'input' ? -1 : 1;
        }
        return "M " + edge[0] + " " + edge[1] + " C " + edge[0] + " " + (edge[1] + delta) + ", " + edge[2] + " " + (edge[3] - delta) + ", " + edge[2] + " " + edge[3];
    };
    Object.defineProperty(EditorComponent.prototype, "edges", {
        /**
         * Returns edge coordinates for use in SVG.
         *
         * @readonly
         * @type {[number, number, number, number, number][]}
         * @memberof EditorComponent
         */
        get: function () {
            if (!this.taskComponents) {
                return [];
            }
            if (!this.workflow.edges) {
                this.workflow.edges = [];
            }
            var out = [];
            var n = this.el.nativeElement;
            var r = n.getBoundingClientRect();
            var _loop_2 = function (edge) {
                var aComponent = this_2.taskComponents
                    .find(function (component) { return component.task.id === edge.from_task_id; });
                var bComponent = this_2.taskComponents
                    .find(function (component) { return component.task.id === edge.to_task_id; });
                if (!aComponent || !bComponent) {
                    return { value: void 0 };
                }
                var a = aComponent.getParameterPosition('output', edge.output_id);
                var b = bComponent.getParameterPosition('input', edge.input_id);
                if (a === null || b === null) {
                    return { value: void 0 };
                }
                out.push([
                    a[0] - r.left + n.scrollLeft,
                    a[1] - r.top + n.scrollTop,
                    b[0] - r.left + n.scrollLeft,
                    b[1] - r.top + n.scrollTop,
                    edge.id
                ]);
            };
            var this_2 = this;
            for (var _i = 0, _a = this.workflow.edges; _i < _a.length; _i++) {
                var edge = _a[_i];
                var state_1 = _loop_2(edge);
                if (typeof state_1 === "object")
                    return state_1.value;
            }
            return out;
        },
        enumerable: true,
        configurable: true
    });
    /**
     * Adds the process at the given coordinates.
     *
     * @param process the process to add
     * @param x x coordinate in the editor
     * @param y y coordinate in the editor
     */
    EditorComponent.prototype.add = function (process, x, y) {
        this.snapshot();
        var timestamp = (new Date()).getTime();
        // create task
        var task = {
            id: -Math.round(Math.random() * 10000),
            x: x,
            y: y,
            state: __WEBPACK_IMPORTED_MODULE_1_app_models_Task__["a" /* TaskState */].NONE,
            process_id: process.id,
            input_artefacts: [],
            output_artefacts: [],
            created_at: timestamp,
            updated_at: timestamp,
        };
        // add task to current workflow
        this.workflow.tasks.push(task);
        this.workflowChanged.emit(this.workflow);
        this.detectChanges();
    };
    /**
     * Called when changes detected
     *
     * @private
     * @memberof EditorComponent
     */
    EditorComponent.prototype.detectChanges = function () {
        if (!this.cd['destroyed']) {
            this.cd.detectChanges();
        }
    };
    /**
     * Removes a task from the editor.
     *
     * @param task_id the id of the task
     */
    EditorComponent.prototype.remove = function (task_id) {
        if (this.running) {
            return;
        }
        this.snapshot();
        var index = this.workflow.tasks.findIndex(function (task) { return task.id === task_id; });
        this.workflow.tasks.splice(index, 1);
        this.workflow.edges = this.workflow.edges.filter(function (edge) { return edge.from_task_id !== task_id && edge.to_task_id !== task_id; });
        this.detectChanges();
        this.workflowChanged.emit(this.workflow);
    };
    /**
     * Finds the process with the given id.
     *
     * @param id the id of the process
     */
    EditorComponent.prototype.findProcess = function (id) {
        return this.processes.find(function (process) { return process.id === id; });
    };
    /**
     * Triggered when the user starts to drag an edge from
     * a parameter to somewhere else.
     *
     * @param index the parameter index
     * @param event the user clicks on a parameter node
     */
    EditorComponent.prototype.dragStart = function (index, event) {
        if (event.button !== 0 || this.running) {
            return;
        }
        // store index of moved task
        // no move on input/output parameter
        if (!event.target.classList.contains('nomove')) {
            var x = event.offsetX;
            var y = event.offsetY;
            if (event.target.localName !== 'app-task') {
                x += 16;
                y += 16;
            }
            this.movement = { index: index, x: x, y: y, before: JSON.stringify(this.workflow) };
        }
        else {
            this.movement.index = undefined;
        }
    };
    /**
     * Triggerd when the user moves his mouse.
     *
     * @param {MouseEvent} event Mouse event
     * @memberof EditorComponent
     */
    EditorComponent.prototype.mouseDown = function (event) {
        var _this = this;
        this.zone.runOutsideAngular(function () {
            document.addEventListener('mousemove', _this.mouseMove.bind(_this));
        });
    };
    /**
     * Triggered when the user moves the cursor to
     * from a parameter node to somewhere creating an edge.
     *
     * @param event the user moves the mouse
     */
    EditorComponent.prototype.mouseMove = function (event) {
        // return if no task / parameter is selected
        if (this.movement.index === undefined && this.movement.edge === undefined) {
            return true;
        }
        // get movement data
        var n = this.el.nativeElement;
        var r = n.getBoundingClientRect();
        var _a = this.movement, index = _a.index, x = _a.x, y = _a.y;
        if (this.movement.edge === undefined) {
            // Task movement
            // calcualte new position
            this.workflow.tasks[index].x = event.pageX + n.scrollLeft - r.left - x;
            this.workflow.tasks[index].y = event.pageY + n.scrollTop - r.top - y - 20;
        }
        else {
            // Parameter line drawing
            this.movement.edge[0] = n.scrollLeft - r.left + x;
            this.movement.edge[1] = n.scrollTop - r.top + y;
            this.movement.edge[2] = event.pageX + n.scrollLeft - r.left;
            this.movement.edge[3] = event.pageY + n.scrollTop - r.top;
        }
        this.detectChanges();
    };
    /**
     * Triggered when the user releases the mouse button
     * when he drags an edge from one parameter node to
     * another.
     *
     * @param event the user releases the mouse button
     */
    EditorComponent.prototype.dragEnd = function (event) {
        if (this.movement.before !== undefined) {
            this.snapshot(JSON.parse(this.movement.before));
        }
        // reset movement data
        this.movement = {};
        // reset cursor
        document.body.style.cursor = 'default';
        document.removeEventListener('mousemove', this.mouseMove);
    };
    /**
     * Returns allways false.
     * An indicator for browsers.
     *
     * @param event drag over event
     */
    EditorComponent.prototype.dragOver = function (event) {
        // this needs to return false validate dropping area
        return false;
    };
    /**
     * Process is dropped.
     *
     * @param event user drops element
     */
    EditorComponent.prototype.drop = function (event) {
        // get process data from drag and drop event
        try {
            var process = JSON.parse(event.dataTransfer.getData('json'));
            this.add(process, event.offsetX - 100, event.offsetY - 50);
        }
        catch (e) {
        }
    };
    /**
     * Drags a parameter.
     *
     * @param parameter the parameter
     * @param task the task
     */
    EditorComponent.prototype.parameterDrag = function (parameter, task) {
        if (this.running) {
            return;
        }
        var _a = task.getParameterPosition(parameter.role, parameter.id), x = _a[0], y = _a[1];
        this.movement = {
            edge: [0, 0, 0, 0],
            task: task.task,
            parameter: parameter,
            x: x, y: y
        };
        // Set cursor
        document.body.style.cursor = 'pointer';
    };
    /**
     * Drops a parameter.
     *
     * @param parameter the parameter
     * @param task the task
     */
    EditorComponent.prototype.parameterDrop = function (parameter, task) {
        if (this.running || !this.movement.parameter || parameter.role === this.movement.parameter.role) {
            return;
        }
        // Check same type
        if (this.movement.parameter.type !== parameter.type) {
            return;
        }
        if (this.movement.edge) {
            this.snapshot();
            var input_id = parameter.role === 'input' ? parameter.id : this.movement.parameter.id;
            var output_id = parameter.role === 'output' ? parameter.id : this.movement.parameter.id;
            var from_task_id = parameter.role === 'output' ? task.task.id : this.movement.task.id;
            var to_task_id = parameter.role === 'input' ? task.task.id : this.movement.task.id;
            this.workflow.edges.push({ id: -Math.round(Math.random() * 10000), from_task_id: from_task_id, to_task_id: to_task_id, input_id: input_id, output_id: output_id });
            this.workflowChanged.emit(this.workflow);
        }
    };
    /**
     * Creates a new snapshot.
     *
     * @param workflow the workflow
     */
    EditorComponent.prototype.snapshot = function (workflow) {
        if (workflow) {
            this.snapshots.push(workflow);
        }
        else {
            this.snapshots.push(JSON.parse(JSON.stringify(this.workflow)));
        }
    };
    /**
     * Loads last workflow and thus reverts change.
     *
     * @returns {void}
     * @memberof EditorComponent
     */
    EditorComponent.prototype.undo = function () {
        if (this.running) {
            return;
        }
        var snapshot = this.snapshots.pop();
        if (snapshot !== undefined) {
            this.workflow = snapshot;
        }
        this.detectChanges();
        this.workflowChanged.emit(this.workflow);
    };
    /**
     * Is supposed to return true if there is the
     * last snapshot and the workflow is not running
     * else returns false.
     *
     * @returns {boolean} Can undo
     * @memberof EditorComponent
     */
    EditorComponent.prototype.canUndo = function () {
        return this.snapshots.length > 0 && !this.running;
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], EditorComponent.prototype, "workflow", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Array)
    ], EditorComponent.prototype, "processes", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChildren */])(__WEBPACK_IMPORTED_MODULE_2_app_components_task_task_component__["a" /* TaskComponent */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["W" /* QueryList */])
    ], EditorComponent.prototype, "taskComponents", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
        __metadata("design:type", Object)
    ], EditorComponent.prototype, "workflowChanged", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], EditorComponent.prototype, "running", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('mousedown', ['$event']),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [MouseEvent]),
        __metadata("design:returntype", void 0)
    ], EditorComponent.prototype, "mouseDown", null);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('mouseup'),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [Object]),
        __metadata("design:returntype", void 0)
    ], EditorComponent.prototype, "dragEnd", null);
    EditorComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-editor',
            template: __webpack_require__("../../../../../src/app/components/editor/editor.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/editor/editor.component.scss")],
            changeDetection: __WEBPACK_IMPORTED_MODULE_0__angular_core__["j" /* ChangeDetectionStrategy */].OnPush,
            animations: [
                Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["k" /* trigger */])('fade', [
                    Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["j" /* transition */])(':leave', [
                        Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["e" /* animate */])('233ms ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["i" /* style */])({ opacity: 0 }))
                    ]),
                ])
            ]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */], __WEBPACK_IMPORTED_MODULE_0__angular_core__["P" /* NgZone */], __WEBPACK_IMPORTED_MODULE_0__angular_core__["k" /* ChangeDetectorRef */]])
    ], EditorComponent);
    return EditorComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/process-dialog/process-dialog.component.html":
/***/ (function(module, exports) {

module.exports = "<h2 mat-dialog-title>{{ process.title }}</h2>\n<mat-dialog-content class=\"content\">\n\n  <mat-tab-group>\n    <mat-tab label=\"Info\">\n      <div class=\"tab-content\">\n        <div class=\"info-box\">\n          <div>\n            <span class=\"info\">abstract: </span>{{ process.abstract }}\n          </div>\n          <div>\n            <span class=\"info\">identifier: </span>{{ process.identifier }}\n          </div>\n        </div>\n      </div>\n    </mat-tab>\n\n    <mat-tab *ngIf=\"process.inputs.length > 0\" label=\"Inputs\">\n      <div class=\"tab-content\">\n        <div *ngFor=\"let input of process.inputs\" class=\"info-box\">\n          <div *ngIf=\"input.abstract\">{{ input.abstract }} </div>\n          <div>\n            <span class=\"info\">type: </span>\n            <span [style.color]=\"getTypeColor(input.type)\">{{ getTypeName(input.type) }}</span>\n          </div>\n        </div>\n      </div>\n    </mat-tab>\n\n\n    <mat-tab *ngIf=\"process.outputs.length > 0\" label=\"Outputs\">\n      <div class=\"tab-content\">\n        <div *ngFor=\"let output of process.outputs\" class=\"info-box\">\n          <div *ngIf=\"output.abstract\">{{ output.abstract }}</div>\n          <div>\n            <span class=\"info\">type: </span>\n            <span [style.color]=\"getTypeColor(output.type)\">{{ getTypeName(output.type) }}</span>\n          </div>\n        </div>\n      </div>\n    </mat-tab>\n  </mat-tab-group>\n\n\n</mat-dialog-content>\n<mat-dialog-actions fxLayout=\"row\" fxLayoutAlign=\"end\">\n  <button mat-button mat-dialog-close i18n=\"@@close\">Close</button>\n</mat-dialog-actions>"

/***/ }),

/***/ "../../../../../src/app/components/process-dialog/process-dialog.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".content {\n  width: 40vw; }\n\n.tab-content {\n  padding: 8px; }\n\n.info {\n  padding: 2px;\n  color: #595959; }\n\n.title {\n  color: #373737;\n  font-size: 21px;\n  padding: 8px; }\n\n.info-box {\n  background: #F9F9F9;\n  border-radius: 3px;\n  padding: 8px;\n  margin: 3px; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/process-dialog/process-dialog.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ProcessDialogComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};



var ProcessDialogComponent = (function () {
    /**
     * creates a process dialog object
     * @param process the associated process
     */
    function ProcessDialogComponent(process) {
        this.process = process;
    }
    ProcessDialogComponent.prototype.ngOnInit = function () {
    };
    /**
     * returns the name of the parameter type
     * @param type the type of the parameter
     */
    ProcessDialogComponent.prototype.getTypeName = function (type) {
        return __WEBPACK_IMPORTED_MODULE_2_app_services_process_service__["a" /* ProcessService */].getTypeName(type);
    };
    /**
     * returns the color of the parameter type
     * @param type the type of the parameter
     */
    ProcessDialogComponent.prototype.getTypeColor = function (type) {
        return __WEBPACK_IMPORTED_MODULE_2_app_services_process_service__["a" /* ProcessService */].getTypeColor(type);
    };
    ProcessDialogComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-process-dialog',
            template: __webpack_require__("../../../../../src/app/components/process-dialog/process-dialog.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/process-dialog/process-dialog.component.scss")]
        }),
        __param(0, Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Inject */])(__WEBPACK_IMPORTED_MODULE_1__angular_material__["a" /* MAT_DIALOG_DATA */])),
        __metadata("design:paramtypes", [Object])
    ], ProcessDialogComponent);
    return ProcessDialogComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/process-list/process-list.component.html":
/***/ (function(module, exports) {

module.exports = "<mat-card class=\"card\">\n  <ng-container *ngIf=\"wps && processes; else loadingTemplate\">\n\n    <ng-container *ngIf=\"processes.length > 0; else noProcessesTemplate\">\n      <mat-list class=\"list\">\n        <ng-container *ngFor=\"let w of wps\">\n          <h3 matSubheader>\n            <div>{{ w.title }}</div>\n          </h3>\n          <div class=\"provider-title\">\n            {{ w.provider?.title }}\n          </div>\n          <app-process *ngFor=\"let process of processByWPS(w.id)\" [process]=\"process\"></app-process>\n          <mat-divider></mat-divider>\n        </ng-container>\n      </mat-list>\n    </ng-container>\n    <ng-template #noProcessesTemplate>\n      <div class=\"no-processes\">No Processes Availible</div>\n    </ng-template>\n\n  </ng-container>\n\n\n  <ng-template #loadingTemplate>\n    <mat-spinner class=\"loading\" diameter=\"55\" color=\"accent\"></mat-spinner>\n  </ng-template>\n</mat-card>"

/***/ }),

/***/ "../../../../../src/app/components/process-list/process-list.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  position: relative; }\n\n.card {\n  padding: 5px;\n  background: #fafafa;\n  height: calc(100% - 10px);\n  overflow: hidden; }\n\n.list {\n  overflow-y: scroll;\n  height: 100%; }\n\n.loading {\n  position: absolute;\n  top: calc(50% - 25px);\n  left: calc(50% - 25px); }\n\n.provider-title {\n  font-size: 8px;\n  padding-left: 15px;\n  margin-top: -13px;\n  color: #909090; }\n\n.no-processes {\n  font-size: 13px;\n  line-height: 21px;\n  color: rgba(0, 0, 0, 0.34);\n  padding: 21px 3px;\n  width: 100%;\n  text-align: center; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/process-list/process-list.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ProcessListComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var ProcessListComponent = (function () {
    /**
     * creates a process list object
     */
    function ProcessListComponent() {
    }
    ProcessListComponent.prototype.ngOnInit = function () { };
    /**
     * returns the process by the wps id
     * @param id the id of the wps
     */
    ProcessListComponent.prototype.processByWPS = function (id) {
        return this.processes.filter(function (process) { return process.wps_id === id; });
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Array)
    ], ProcessListComponent.prototype, "processes", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Array)
    ], ProcessListComponent.prototype, "wps", void 0);
    ProcessListComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-process-list',
            template: __webpack_require__("../../../../../src/app/components/process-list/process-list.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/process-list/process-list.component.scss")],
            changeDetection: __WEBPACK_IMPORTED_MODULE_0__angular_core__["j" /* ChangeDetectionStrategy */].OnPush
        }),
        __metadata("design:paramtypes", [])
    ], ProcessListComponent);
    return ProcessListComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/process/process.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container\">{{ process.title }}</div>\n\n<div class=\"title\">{{ process.title }}</div>\n\n<div *ngIf=\"process.inputs\" class=\"inputs\">\n  <span *ngFor=\"let input of process.inputs\" class=\"input\" [matTooltip]=\"input.title\" matTooltipPosition=\"above\" matTooltipShowDelay=\"200\"\n    [style.border-color]=\"getParameterColor(input.type)\"></span>\n</div>\n\n<div *ngIf=\"process.outputs\" class=\"outputs\">\n  <span *ngFor=\"let output of process.outputs\" class=\"output\" [matTooltip]=\"output.title\" matTooltipPosition=\"below\" matTooltipShowDelay=\"200\"\n    [style.background]=\"getParameterColor(output.type)\"></span>\n</div>"

/***/ }),

/***/ "../../../../../src/app/components/process/process.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  display: block;\n  position: relative;\n  background-color: #ffffff;\n  border-radius: 3px;\n  border: solid 1px #eeeeee;\n  width: 200px;\n  margin: 21px 2px;\n  padding: 8px;\n  cursor: move; }\n  :host:hover {\n    background-color: #f8f8f8; }\n  .title {\n  margin: 8px 8px;\n  color: #444444;\n  -webkit-user-select: none;\n     -moz-user-select: none;\n      -ms-user-select: none;\n          user-select: none; }\n  .outputs {\n  position: absolute;\n  padding: 2px;\n  bottom: -16px;\n  right: 0; }\n  .inputs {\n  position: absolute;\n  padding: 2px;\n  top: -12px;\n  left: 0; }\n  .input {\n  display: inline-block;\n  width: 13px;\n  height: 13px;\n  border-radius: 20px;\n  margin: 1px;\n  border: solid 2px #2196F3;\n  background: #ffffff; }\n  .output {\n  display: inline-block;\n  width: 13px;\n  height: 13px;\n  border-radius: 20px;\n  margin: 1px;\n  border: solid 2px #ffffff;\n  background: #2196F3; }\n  .container {\n  z-index: -1;\n  position: absolute;\n  width: 100%;\n  height: 100%;\n  border: dashed 1px #555555;\n  border-radius: 3px;\n  padding: 3px;\n  font-size: 13px;\n  line-height: 100%;\n  color: #555555; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/process/process.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ProcessComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__ = __webpack_require__("../../../../../src/app/models/ProcessParameter.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_app_components_process_dialog_process_dialog_component__ = __webpack_require__("../../../../../src/app/components/process-dialog/process-dialog.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var ProcessComponent = (function () {
    /**
     * creates a process object
     * @param dialog the dialog that opens a process dialog
     * @param el element reference
     */
    function ProcessComponent(dialog, el) {
        this.dialog = dialog;
        this.el = el;
        this.draggable = true;
    }
    /**
     * triggered if host clicks
     */
    ProcessComponent.prototype.hostClicked = function () {
        this.openDialog();
    };
    /**
     * opens a process dialog
     */
    ProcessComponent.prototype.openDialog = function () {
        this.dialog.open(__WEBPACK_IMPORTED_MODULE_3_app_components_process_dialog_process_dialog_component__["a" /* ProcessDialogComponent */], {
            data: this.process
        });
    };
    /**
     * returns the color of the parameter
     * @param type the parameter type
     */
    ProcessComponent.prototype.getParameterColor = function (type) {
        switch (type) {
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].LITERAL: return '#03A9F4';
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX: return '#FFC107';
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX: return '#4CAF50';
            default: return '#000000';
        }
    };
    /**
     * triggered if user starts to drag element
     * @param event the user starts dragging an element
     */
    ProcessComponent.prototype.dragStart = function (event) {
        var native = this.el.nativeElement;
        for (var i = 0; i < native.childElementCount; i++) {
            var c = native.children[i];
            if (c.classList.contains('container')) {
                event.dataTransfer.setDragImage(c, c.clientWidth / 2, c.clientHeight / 2);
                event.dataTransfer.setData('json', JSON.stringify(this.process));
                break;
            }
        }
    };
    ProcessComponent.prototype.ngOnInit = function () {
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], ProcessComponent.prototype, "process", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["z" /* HostBinding */])('draggable'),
        __metadata("design:type", Object)
    ], ProcessComponent.prototype, "draggable", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('click'),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", []),
        __metadata("design:returntype", void 0)
    ], ProcessComponent.prototype, "hostClicked", null);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('dragstart', ['$event']),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [DragEvent]),
        __metadata("design:returntype", void 0)
    ], ProcessComponent.prototype, "dragStart", null);
    ProcessComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-process',
            template: __webpack_require__("../../../../../src/app/components/process/process.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/process/process.component.scss")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_material__["f" /* MatDialog */], __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */]])
    ], ProcessComponent);
    return ProcessComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/result-dialog/result-dialog.component.html":
/***/ (function(module, exports) {

module.exports = "<h2 mat-dialog-title>{{ workflow.title }} - Result</h2>\n\n<mat-dialog-content class=\"content\">\n  <div class=\"result\" *ngFor=\"let result of results\">\n    <pre>{{ result.data }}</pre>\n  </div>\n</mat-dialog-content>\n\n<mat-divider></mat-divider>\n<mat-dialog-actions fxLayout=\"row\" fxLayoutAlign=\"end\">\n  <button mat-button mat-dialog-close i18n=\"@@close\">CLOSE</button>\n</mat-dialog-actions>"

/***/ }),

/***/ "../../../../../src/app/components/result-dialog/result-dialog.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  display: block;\n  position: relative; }\n\n.content {\n  width: 40vw; }\n\n.result {\n  background: #F9F9F9;\n  padding: 8px;\n  margin: 5px;\n  border-radius: 3px; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/result-dialog/result-dialog.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ResultDialogComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};


var ResultDialogComponent = (function () {
    /**
     * creates an artefact object
     * @param data the artefact data
     * @param dialog the artefact dialog
     */
    function ResultDialogComponent(workflow, dialog) {
        this.workflow = workflow;
        this.dialog = dialog;
    }
    ResultDialogComponent.prototype.ngOnInit = function () {
    };
    Object.defineProperty(ResultDialogComponent.prototype, "results", {
        get: function () {
            var out = [];
            var _loop_1 = function (task) {
                var _loop_2 = function (artefact) {
                    if (this_1.workflow.edges.findIndex(function (edge) { return edge.output_id === artefact.parameter_id && edge.from_task_id === task.id; }) === -1) {
                        out.push(artefact);
                    }
                };
                for (var _i = 0, _a = task.output_artefacts; _i < _a.length; _i++) {
                    var artefact = _a[_i];
                    _loop_2(artefact);
                }
            };
            var this_1 = this;
            for (var _i = 0, _a = this.workflow.tasks; _i < _a.length; _i++) {
                var task = _a[_i];
                _loop_1(task);
            }
            return out;
        },
        enumerable: true,
        configurable: true
    });
    ResultDialogComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-result-dialog',
            template: __webpack_require__("../../../../../src/app/components/result-dialog/result-dialog.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/result-dialog/result-dialog.component.scss")],
        }),
        __param(0, Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Inject */])(__WEBPACK_IMPORTED_MODULE_1__angular_material__["a" /* MAT_DIALOG_DATA */])),
        __metadata("design:paramtypes", [Object, __WEBPACK_IMPORTED_MODULE_1__angular_material__["h" /* MatDialogRef */]])
    ], ResultDialogComponent);
    return ResultDialogComponent;
}());



/***/ }),

/***/ "../../../../../src/app/components/task/task.component.html":
/***/ (function(module, exports) {

module.exports = "<mat-menu #menu=\"matMenu\">\n  <button mat-menu-item (click)=\"openDetail()\" i18n=\"@@info\">Info</button>\n  <button *ngIf=\"!this.running\" mat-menu-item (click)=\"clickDelete()\" i18n=\"@@delete\">Delete</button>\n</mat-menu>\n\n\n<div class=\"title\">{{ process.title }}</div>\n<span *ngIf=\"running\" class=\"state\" [style.color]=\"stateInfo.color\" [style.borderColor]=\"stateInfo.color\">{{ stateInfo.name }}</span>\n<span [matMenuTriggerFor]=\"menu\"></span>\n\n<div class=\"inputs\" #inputs>\n  <span *ngFor=\"let input of process.inputs\" [attr.data-id]=\"input.id\" class=\"input nomove\" [matTooltip]=\"input.title\" matTooltipPosition=\"above\"\n    matTooltipShowDelay=\"200\" [style.border-color]=\"getParameterColor(input.type)\" (mousedown)=\"parameterMouseDown(input, $event)\"\n    (mouseup)=\"parameterMouseUp(input, $event)\" [class.artefact]=\"hasArtefact(input)\">\n  </span>\n</div>\n\n<div class=\"outputs\" #outputs>\n  <span *ngFor=\"let output of process.outputs\" [attr.data-id]=\"output.id\" class=\"output nomove\" [matTooltip]=\"output.title\"\n    matTooltipPosition=\"below\" matTooltipShowDelay=\"200\" [style.background]=\"getParameterColor(output.type)\" (mousedown)=\"parameterMouseDown(output, $event)\"\n    (mouseup)=\"parameterMouseUp(output, $event)\" [class.artefact]=\"hasArtefact(output)\">\n  </span>\n</div>"

/***/ }),

/***/ "../../../../../src/app/components/task/task.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ":host {\n  display: block;\n  position: relative;\n  background-color: #ffffff;\n  border-radius: 3px;\n  border: solid 1px #eeeeee;\n  width: 200px;\n  margin: 21px 2px;\n  padding: 8px;\n  -webkit-user-select: none;\n     -moz-user-select: none;\n      -ms-user-select: none;\n          user-select: none;\n  cursor: move; }\n  :host:hover {\n    background-color: #f8f8f8; }\n  .title {\n  margin: 8px 8px;\n  color: #444444;\n  -webkit-user-select: none;\n     -moz-user-select: none;\n      -ms-user-select: none;\n          user-select: none;\n  width: 60%;\n  font-size: 14px; }\n  .outputs {\n  position: absolute;\n  padding: 2px;\n  bottom: -16px;\n  right: 0; }\n  .inputs {\n  position: absolute;\n  padding: 2px;\n  top: -12px;\n  left: 0; }\n  .input {\n  display: inline-block;\n  width: 13px;\n  height: 13px;\n  border-radius: 20px;\n  margin: 1px;\n  border: solid 2px #2196F3;\n  background: #ffffff;\n  cursor: pointer; }\n  .input:hover {\n    -webkit-transform: scale(1.3);\n            transform: scale(1.3);\n    -webkit-box-shadow: 0 3px 3px rgba(0, 0, 0, 0.13);\n            box-shadow: 0 3px 3px rgba(0, 0, 0, 0.13); }\n  .output {\n  display: inline-block;\n  width: 13px;\n  height: 13px;\n  border-radius: 20px;\n  margin: 1px;\n  border: solid 2px #ffffff;\n  background: #2196F3;\n  cursor: pointer; }\n  .output:hover {\n    -webkit-transform: scale(1.3);\n            transform: scale(1.3);\n    -webkit-box-shadow: 0 3px 3px rgba(0, 0, 0, 0.13);\n            box-shadow: 0 3px 3px rgba(0, 0, 0, 0.13); }\n  .state {\n  position: absolute;\n  right: 16px;\n  top: 16px;\n  font-size: 10px;\n  pointer-events: none;\n  color: #909090;\n  border: solid 1px #909090;\n  padding: 3px 8px;\n  border-radius: 3px;\n  opacity: 0.55; }\n  .artefact {\n  border-radius: 0 !important;\n  -webkit-transform: rotate(45deg) scale(0.8);\n          transform: rotate(45deg) scale(0.8); }\n  .artefact:hover {\n    -webkit-transform: rotate(45deg) scale(0.8);\n            transform: rotate(45deg) scale(0.8); }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/components/task/task.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TaskComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__ = __webpack_require__("../../../../../src/app/models/ProcessParameter.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_app_components_process_dialog_process_dialog_component__ = __webpack_require__("../../../../../src/app/components/process-dialog/process-dialog.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_app_models_Task__ = __webpack_require__("../../../../../src/app/models/Task.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_app_components_artefact_dialog_artefact_dialog_component__ = __webpack_require__("../../../../../src/app/components/artefact-dialog/artefact-dialog.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







var TaskComponent = (function () {
    /**
     * creates a task object
     * @param dialog material dialog
     * @param el element reference
     */
    function TaskComponent(dialog, el) {
        this.dialog = dialog;
        this.el = el;
        this.parameterDrag = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.parameterDrop = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.taskRemove = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.changeArtefact = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["x" /* EventEmitter */]();
        this.running = false;
    }
    TaskComponent.prototype.ngOnInit = function () {
    };
    Object.defineProperty(TaskComponent.prototype, "stateInfo", {
        /**
         * @returns the task state as an object
         */
        get: function () {
            var _this = this;
            var infoMap = [
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].DEPRECATED, name: 'DEPRECATED', color: '#E91E63' },
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].FAILED, name: 'FAILED', color: '#F44336' },
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].FINISHED, name: 'FINISHED', color: '#2196F3' },
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].READY, name: 'READY', color: '#9E9E9E' },
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].RUNNING, name: 'RUNNING', color: '#FFC107' },
                { state: __WEBPACK_IMPORTED_MODULE_4_app_models_Task__["a" /* TaskState */].WAITING, name: 'WAITING', color: '#03A9F4' },
            ];
            return infoMap.find(function (info) { return info.state === _this.task.state; });
        },
        enumerable: true,
        configurable: true
    });
    /**
     * triggered when the user clicks
     * @param event the user clicks the mouse button
     */
    TaskComponent.prototype.hostMouseDown = function (event) {
        if (event.button === 0) {
            this.mouseDownPos = [event.pageX, event.pageY];
        }
    };
    /**
     * triggered when user releases mouse button
     * @param event user releases mouse button
     */
    TaskComponent.prototype.hostMouseUp = function (event) {
        if (event.target.classList.contains('nomove')) {
            return;
        }
        if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY) {
            this.menuComponent.openMenu();
        }
        this.mouseDownPos = undefined;
    };
    /**
     * opens task menu
     * @param event context menu event
     */
    TaskComponent.prototype.hostContextmenu = function (event) {
        this.menuComponent.openMenu();
        return false;
    };
    /**
     * deletes the task
     */
    TaskComponent.prototype.clickDelete = function () {
        this.taskRemove.emit(this.task);
    };
    /**
     * opens the process dialog
     */
    TaskComponent.prototype.openDetail = function () {
        this.dialog.open(__WEBPACK_IMPORTED_MODULE_3_app_components_process_dialog_process_dialog_component__["a" /* ProcessDialogComponent */], {
            data: this.process
        });
    };
    /**
     * returns the color of the process parameter
     * @param type type of the process parameter
     */
    TaskComponent.prototype.getParameterColor = function (type) {
        switch (type) {
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].LITERAL: return '#03A9F4';
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX: return '#FFC107';
            case __WEBPACK_IMPORTED_MODULE_2_app_models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX: return '#4CAF50';
            default: return '#000000';
        }
    };
    /**
     * triggered when user clicks on task
     * @param parameter process parameter
     * @param event user clicks mouse
     */
    TaskComponent.prototype.parameterMouseDown = function (parameter, event) {
        if (this.hasArtefact(parameter)) {
            return;
        }
        this.mouseDownPos = [event.pageX, event.pageY];
        this.parameterDrag.emit(parameter);
    };
    /**
     * opens artefact dialog
     * @param parameter process parameter
     * @param event user releases mouse button
     */
    TaskComponent.prototype.parameterMouseUp = function (parameter, event) {
        if (this.mouseDownPos && this.mouseDownPos[0] === event.pageX && this.mouseDownPos[1] === event.pageY) {
            // Can't open output dialog when editing
            if (parameter.role === 'output' && !this.running) {
                return;
            }
            // Can't open input dialog when running
            if (parameter.role === 'input' && this.running) {
                return;
            }
            // Can't open output artefakt without a result
            if (parameter.role === 'output' &&
                this.task.output_artefacts.findIndex(function (artefact) { return artefact.parameter_id === parameter.id; }) === -1) {
                return;
            }
            this.dialog.open(__WEBPACK_IMPORTED_MODULE_5_app_components_artefact_dialog_artefact_dialog_component__["a" /* ArtefactDialogComponent */], {
                data: {
                    task: this,
                    parameter: parameter
                }
            });
        }
        else {
            if (!this.hasArtefact(parameter)) {
                this.parameterDrop.emit(parameter);
            }
        }
    };
    /**
     * adds data to an artefact
     * @param parameter process parameter
     * @param data the added data
     */
    TaskComponent.prototype.addArtefact = function (parameter, data) {
        this.changeArtefact.emit([{ task: this.task, parameter: parameter }, data]);
    };
    TaskComponent.prototype.removeArtefact = function (parameter) {
        this.changeArtefact.emit([{ task: this.task, parameter: parameter }, null]);
    };
    /**
     * returns if the task component has an artefact
     * @param parameter process parameter
     */
    TaskComponent.prototype.hasArtefact = function (parameter) {
        if (!this.task.input_artefacts || !this.task.output_artefacts) {
            return false;
        }
        if (parameter.role === 'input') {
            return -1 !== this.task.input_artefacts.findIndex(function (artefact) { return artefact.parameter_id === parameter.id; });
        }
        else if (this.running) {
            return -1 !== this.task.output_artefacts.findIndex(function (artefact) { return artefact.parameter_id === parameter.id; });
        }
        return false;
    };
    /**
     * returns the parameter position
     * @param role the parameter role which can either be input or output
     * @param id the parameter id
     */
    TaskComponent.prototype.getParameterPosition = function (role, id) {
        var n = (role === 'input' ? this.inputContainer : this.outputContainer).nativeElement;
        for (var i = 0; i < n.childElementCount; i++) {
            if (n.children[i].getAttribute('data-id') === '' + id) {
                var rect = n.children[i].getBoundingClientRect();
                return [rect.left + 11, rect.top + 11];
            }
        }
        return null;
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "process", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "task", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('inputs'),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */])
    ], TaskComponent.prototype, "inputContainer", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('outputs'),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */])
    ], TaskComponent.prototype, "outputContainer", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])(__WEBPACK_IMPORTED_MODULE_1__angular_material__["o" /* MatMenuTrigger */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1__angular_material__["o" /* MatMenuTrigger */])
    ], TaskComponent.prototype, "menuComponent", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "parameterDrag", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "parameterDrop", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "taskRemove", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "changeArtefact", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], TaskComponent.prototype, "running", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('mousedown', ['$event']),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [MouseEvent]),
        __metadata("design:returntype", void 0)
    ], TaskComponent.prototype, "hostMouseDown", null);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('mouseup', ['$event']),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [MouseEvent]),
        __metadata("design:returntype", void 0)
    ], TaskComponent.prototype, "hostMouseUp", null);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* HostListener */])('contextmenu', ['$event']),
        __metadata("design:type", Function),
        __metadata("design:paramtypes", [MouseEvent]),
        __metadata("design:returntype", void 0)
    ], TaskComponent.prototype, "hostContextmenu", null);
    TaskComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-task',
            template: __webpack_require__("../../../../../src/app/components/task/task.component.html"),
            styles: [__webpack_require__("../../../../../src/app/components/task/task.component.scss")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_material__["f" /* MatDialog */], __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */]])
    ], TaskComponent);
    return TaskComponent;
}());



/***/ }),

/***/ "../../../../../src/app/models/ProcessParameter.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ProcessParameterType; });
/**
 * The type of the process parameter
 * which according to the ogc wps
 * accepts literals, complex data
 * and bounding box data
 *
 * @export
 * @enum {number}
 */
var ProcessParameterType;
(function (ProcessParameterType) {
    ProcessParameterType[ProcessParameterType["LITERAL"] = 0] = "LITERAL";
    ProcessParameterType[ProcessParameterType["COMPLEX"] = 1] = "COMPLEX";
    ProcessParameterType[ProcessParameterType["BOUNDING_BOX"] = 2] = "BOUNDING_BOX";
})(ProcessParameterType || (ProcessParameterType = {}));


/***/ }),

/***/ "../../../../../src/app/models/Task.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return TaskState; });
/**
 * Describes the current state of a task.
 *
 * @export
 * @enum {number}
 */
var TaskState;
(function (TaskState) {
    TaskState[TaskState["NONE"] = 0] = "NONE";
    TaskState[TaskState["READY"] = 1] = "READY";
    TaskState[TaskState["WAITING"] = 2] = "WAITING";
    TaskState[TaskState["RUNNING"] = 3] = "RUNNING";
    TaskState[TaskState["FINISHED"] = 4] = "FINISHED";
    TaskState[TaskState["FAILED"] = 5] = "FAILED";
    TaskState[TaskState["DEPRECATED"] = 6] = "DEPRECATED";
})(TaskState || (TaskState = {}));


/***/ }),

/***/ "../../../../../src/app/pages/editor-page/editor-page.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"toolbar mat-elevation-z2\" fxLayout=\"row\" fxLayoutAlign=\"space-between\">\n  <div *ngIf=\"workflow\">\n    <div [style.display]=\"editTitleMode ? 'none' : 'block'\" class=\"title\">\n      {{ workflow?.title }}\n      <button @slide *ngIf=\"!runs()\" mat-icon-button class=\"edit-name\" (click)=\"clickTitleEdit()\">\n        <mat-icon aria-label=\"Example icon-button with a heart icon\">edit</mat-icon>\n      </button>\n    </div>\n    <div [style.display]=\"editTitleMode ? 'block' : 'none'\">\n      <mat-form-field>\n        <input #tileInput id=\"titleInput\" matInput [placeholder]=\"workflow?.title\" (keyup.enter)=\"save()\" autofocus>\n      </mat-form-field>\n    </div>\n  </div>\n\n  <div>\n    <div @slide *ngIf=\"!runs()\">\n      <button mat-button (click)=\"undo()\" [disabled]=\"!canUndo()\" i18n=\"@@undo\">UNDO</button>\n      <button mat-raised-button (click)=\"save()\" color=\"primary\" i18n=\"@@save\">SAVE</button>\n    </div>\n\n\n    <button @slide (click)=\"showResults()\" *ngIf=\"finished()\" class=\"results\" mat-raised-button color=\"primary\">SHOW RESULT</button>\n  </div>\n</div>\n\n<app-editor class=\"editor\" [workflow]=\"workflow\" [processes]=\"processes | async\" (workflowChanged)=\"workflowChanged($event)\"\n  [running]=\"runs()\"></app-editor>\n\n\n<app-process-list @slide *ngIf=\"!runs()\" [processes]=\"processes | async\" [wps]=\"wps | async\" class=\"process-list\"></app-process-list>\n\n<ng-container *ngIf=\"workflow?.id >= 0\">\n  <button *ngIf=\"!runs(); else runningTemplate\" mat-fab color=\"primary\" class=\"run\" [disabled]=\"workflowError !== ''\" (click)=\"run()\">\n    <mat-icon [matTooltip]=\"workflowError\" aria-label=\"Run\">play_arrow</mat-icon>\n  </button>\n\n  <ng-template #runningTemplate>\n    <mat-spinner *ngIf=\"!finished()\" class=\"run\" class=\"spinner\" diameter=\"89\"></mat-spinner>\n    <button mat-fab color=\"primary\" class=\"run\" (click)=\"stop()\">\n      <mat-icon *ngIf=\"!finished()\" matTooltip=\"Stop\" aria-label=\"Stop\">stop</mat-icon>\n      <mat-icon *ngIf=\"finished()\" matTooltip=\"Edit\" aria-label=\"Edit\">edit</mat-icon>\n    </button>\n  </ng-template>\n</ng-container>"

/***/ }),

/***/ "../../../../../src/app/pages/editor-page/editor-page.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".content {\n  margin-top: 48px;\n  height: calc(100vh - 48px); }\n\n.navbar {\n  max-height: 48px;\n  border-bottom: 2px solid #00796B;\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  z-index: 2; }\n\n.tab-nav {\n  width: calc(90% - 116px);\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-pack: center;\n      -ms-flex-pack: center;\n          justify-content: center;\n  color: rgba(255, 255, 255, 0.87); }\n\n.logo {\n  height: 34px;\n  cursor: pointer; }\n\n:host {\n  display: block;\n  position: relative;\n  width: 100%;\n  height: 100%;\n  overflow: hidden; }\n\n.toolbar {\n  position: fixed;\n  top: 48px;\n  left: 0;\n  right: 0;\n  height: 58px;\n  background: #fafafa;\n  padding: 11px; }\n\n.editor {\n  margin-top: 60px;\n  width: 100%;\n  height: calc(100% - 60px); }\n\n.title {\n  display: inline-block;\n  color: #373737;\n  padding: 9px;\n  cursor: pointer; }\n\n.run {\n  position: fixed;\n  bottom: 34px;\n  left: 34px; }\n\n.process-list {\n  min-width: 230px;\n  position: fixed;\n  top: 118px;\n  bottom: 8px;\n  right: 8px; }\n\n.edit-name {\n  float: left;\n  margin-top: -12px; }\n\n.edit-name mat-icon {\n    color: #adadad;\n    font-size: 18px; }\n\n.spinner {\n  position: fixed;\n  bottom: 17px;\n  left: 17px; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/editor-page/editor-page.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EditorPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__ = __webpack_require__("../../../../../src/app/services/workflow.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_app_components_editor_editor_component__ = __webpack_require__("../../../../../src/app/components/editor/editor.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__angular_animations__ = __webpack_require__("../../../animations/esm5/animations.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_app_services_wps_service__ = __webpack_require__("../../../../../src/app/services/wps.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8_app_components_result_dialog_result_dialog_component__ = __webpack_require__("../../../../../src/app/components/result-dialog/result-dialog.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9_rxjs_operators__ = __webpack_require__("../../../../rxjs/_esm5/operators.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};










/**
 * Editor page.
 *
 * @export
 * @class EditorPageComponent
 * @implements {OnInit}
 */
var EditorPageComponent = (function () {
    /**
     * Creates an instance of EditorPageComponent.
     *
     * @param {ProcessService} processService
     * @param {WorkflowService} workflowService
     * @param {WpsService} wpsService
     * @param {ActivatedRoute} route
     * @param {Router} router
     * @param {MatDialog} dialog
     * @param {ChangeDetectorRef} cd
     * @param {NgZone} zone
     * @memberof EditorPageComponent
     */
    function EditorPageComponent(processService, workflowService, wpsService, route, router, dialog, cd, zone) {
        this.processService = processService;
        this.workflowService = workflowService;
        this.wpsService = wpsService;
        this.route = route;
        this.router = router;
        this.dialog = dialog;
        this.cd = cd;
        this.zone = zone;
        this.editTitleMode = false;
        this.showProcessList = true;
        this.workflowError = 'error';
        this.fresh = false;
        this.canRefreshWorkflow = true;
    }
    /**
     * Sets up this component.
     *
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.processes = this.processService.all();
        this.wps = this.wpsService.all();
        this.route.params.subscribe(function (params) {
            if (params['id'] !== undefined) {
                _this.fresh = false;
                _this.workflowService.get(+params['id']).subscribe(function (w) {
                    _this.workflow = w;
                });
            }
            else {
                _this.fresh = true;
                _this.workflow = {
                    id: -Math.round(Math.random() * 10000),
                    title: 'My New Workflow',
                    edges: [],
                    tasks: [],
                    creator_id: 0,
                    shared: false,
                    created_at: (new Date()).getTime(),
                    updated_at: (new Date()).getTime(),
                };
            }
        });
        setInterval(function () {
            _this.updateWorkflowStatus();
        }, 1500);
        setTimeout(function () {
            _this.workflowChanged(_this.workflow);
            _this.detectChanges();
        }, 500);
    };
    /**
     * Shows result dialog.
     *
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.showResults = function () {
        this.dialog.open(__WEBPACK_IMPORTED_MODULE_8_app_components_result_dialog_result_dialog_component__["a" /* ResultDialogComponent */], {
            data: this.workflow
        });
    };
    /**
     * Updates workflow status.
     *
     * @returns {Promise<void>} Updated
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.updateWorkflowStatus = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!this.canRefreshWorkflow || !this.runs()) {
                            return [2 /*return*/];
                        }
                        this.canRefreshWorkflow = false;
                        _a = this;
                        return [4 /*yield*/, this.workflowService.get(this.workflow.id).toPromise()];
                    case 1:
                        _a.workflow = _b.sent();
                        return [4 /*yield*/, this.workflowService.refresh(this.workflow.id)];
                    case 2:
                        _b.sent();
                        console.log('-- Refreshed Workflow Execution Status --');
                        this.canRefreshWorkflow = true;
                        setTimeout(function () { _this.detectChanges(); }, 1);
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Toggles whether the process list
     * is shown
     *
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.toggleProcessList = function () {
        this.showProcessList = !this.showProcessList;
    };
    /**
     * Reverts the last workflow.
     *
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.undo = function () {
        this.editorComponent.undo();
        this.save();
    };
    /**
     * Tells whether there is something to undo.
     *
     * @returns {boolean} Can Undo
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.canUndo = function () {
        return this.editorComponent ? this.editorComponent.canUndo() : false;
    };
    /**
     * Executes workflow if not empty.
     *
     * @param id the id of the workflow
     */
    EditorPageComponent.prototype.run = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.workflow) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.save()];
                    case 1:
                        _a.sent();
                        return [4 /*yield*/, this.workflowService.start(this.workflow.id)];
                    case 2:
                        _a.sent();
                        this.workflowService.get(this.workflow.id).pipe(Object(__WEBPACK_IMPORTED_MODULE_9_rxjs_operators__["d" /* take */])(1)).subscribe(function (workflow) {
                            _this.workflow = workflow;
                            setTimeout(function () { _this.detectChanges(); }, 10);
                        });
                        this.updateWorkflowStatus();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Stops running workflow.
     *
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.stop = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.workflowService.stop(this.workflow.id)];
                    case 1:
                        _a.sent();
                        this.workflowService.get(this.workflow.id).pipe(Object(__WEBPACK_IMPORTED_MODULE_9_rxjs_operators__["d" /* take */])(1)).subscribe(function (workflow) {
                            _this.workflow = workflow;
                            setTimeout(function () { _this.detectChanges(); }, 10);
                        });
                        this.updateWorkflowStatus();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * enables clicking the title in order to change it
     */
    EditorPageComponent.prototype.clickTitleEdit = function () {
        var _this = this;
        this.editTitleMode = true;
        setTimeout(function () {
            var native = _this.titleInputComponent.nativeElement;
            native.focus();
        }, 150);
    };
    /**
     * Saves the workflow.
     *
     * @returns {Promise<void>} Promise
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.save = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _this = this;
            var name;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        name = document.getElementById('titleInput').value;
                        if (name.length === 0) {
                            name = 'My Workflow';
                        }
                        else if (name.length > 24) {
                            name = name.slice(0, 24);
                        }
                        this.workflow.title = name;
                        if (!this.fresh) return [3 /*break*/, 1];
                        this.workflowService.create(this.editorComponent.workflow).subscribe(function (obj) {
                            _this.router.navigate(["/editor/" + obj.id]);
                        });
                        return [3 /*break*/, 3];
                    case 1: return [4 /*yield*/, this.workflowService.update(this.workflow.id, this.workflow).toPromise()];
                    case 2:
                        _a.sent();
                        _a.label = 3;
                    case 3:
                        this.workflowChanged(this.workflow);
                        this.editTitleMode = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
   * Called when changes detected
   *
   * @private
   * @memberof EditorComponent
   */
    EditorPageComponent.prototype.detectChanges = function () {
        if (!this.cd['destroyed']) {
            this.cd.detectChanges();
        }
    };
    /**
     * Tells whether the current workflow is running.
     *
     * @returns {boolean} Is Running
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.runs = function () {
        if (!this.workflow) {
            return null;
        }
        var running = this.workflowService.isRunning(this.workflow);
        this.canRefreshWorkflow = running && !this.finished();
        return running;
    };
    /**
     * Tells whether the current workflow is finished.
     *
     * @returns {boolean} Is Finished
     * @memberof EditorPageComponent
     */
    EditorPageComponent.prototype.finished = function () {
        return this.workflowService.finished(this.workflow);
    };
    /**
     * Tells if the workflow has changed.
     *
     * @param workflow the workflow which is checked
     */
    EditorPageComponent.prototype.workflowChanged = function (workflow) {
        var _this = this;
        var errorMessages = [
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].SUCCESSFUL, message: '' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].ERROR, message: 'Unknown Error' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].TITLE_TOO_LONG, message: 'Workflow name is to long' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].TITLE_TOO_SHORT, message: 'Workflow name is to short' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].EMPTY, message: 'Workflow is empty' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].LOOP_TO_SAME_TASK, message: 'Loop to same task' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].WRONG_INPUT_TYPES, message: 'Wrong input types' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].MISSING_TASK_INPUT, message: 'Missing task input' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].MISSING_WORKFLOW, message: 'No Workflow provided' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].MISSING_PROCESSES, message: 'No Process List provided' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].CYCLE_IN_WORKFLOW, message: 'Workflow has a cycle' },
            { type: __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["b" /* WorkflowValidationResult */].MULIPLE_INPUTS, message: 'Workflow has taks with multiple inputs' },
        ];
        var result = errorMessages.find(function (m) { return m.type === _this.workflowService.validate(workflow); });
        this.workflowError = result ? result.message : 'No Error Message Found';
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('sidenav'),
        __metadata("design:type", Object)
    ], EditorPageComponent.prototype, "sidenavComponent", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["F" /* Input */])(),
        __metadata("design:type", Object)
    ], EditorPageComponent.prototype, "showProcessList", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])(__WEBPACK_IMPORTED_MODULE_4_app_components_editor_editor_component__["a" /* EditorComponent */]),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_4_app_components_editor_editor_component__["a" /* EditorComponent */])
    ], EditorPageComponent.prototype, "editorComponent", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('tileInput'),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */])
    ], EditorPageComponent.prototype, "titleInputComponent", void 0);
    EditorPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-editor-page',
            template: __webpack_require__("../../../../../src/app/pages/editor-page/editor-page.component.html"),
            styles: [__webpack_require__("../../../../../src/app/pages/editor-page/editor-page.component.scss")],
            changeDetection: __WEBPACK_IMPORTED_MODULE_0__angular_core__["j" /* ChangeDetectionStrategy */].OnPush,
            animations: [
                Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["k" /* trigger */])('slide', [
                    Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["j" /* transition */])(':enter', [
                        Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["i" /* style */])({ transform: 'translateX(100%)' }),
                        Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["e" /* animate */])('233ms ease-in-out')
                    ]),
                    Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["j" /* transition */])(':leave', [
                        Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["e" /* animate */])('233ms ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_5__angular_animations__["i" /* style */])({ transform: 'translateX(100%)' }))
                    ]),
                ])
            ]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_app_services_process_service__["a" /* ProcessService */],
            __WEBPACK_IMPORTED_MODULE_3_app_services_workflow_service__["a" /* WorkflowService */],
            __WEBPACK_IMPORTED_MODULE_6_app_services_wps_service__["a" /* WpsService */],
            __WEBPACK_IMPORTED_MODULE_2__angular_router__["a" /* ActivatedRoute */],
            __WEBPACK_IMPORTED_MODULE_2__angular_router__["c" /* Router */],
            __WEBPACK_IMPORTED_MODULE_7__angular_material__["f" /* MatDialog */],
            __WEBPACK_IMPORTED_MODULE_0__angular_core__["k" /* ChangeDetectorRef */],
            __WEBPACK_IMPORTED_MODULE_0__angular_core__["P" /* NgZone */]])
    ], EditorPageComponent);
    return EditorPageComponent;
}());



/***/ }),

/***/ "../../../../../src/app/pages/login-page/login-page.component.html":
/***/ (function(module, exports) {

module.exports = "<div *ngIf=\"!(loggedIn | async) else logoutTemplate\" class=\"container login-page\">\n    <h1>Login</h1>\n\n    <mat-card fxLayout=\"row\" fxLayoutAlign=\"space-between\">\n        <div>\n            <mat-form-field>\n                <input #usernameInput matInput placeholder=\"Name\" autofocus>\n            </mat-form-field>\n            <mat-form-field>\n                <input #passwordInput matInput placeholder=\"Password\" type=\"password\">\n            </mat-form-field>\n\n        </div>\n        <button mat-raised-button color=\"primary\" (click)=\"login(usernameInput.value, passwordInput.value)\"\n                                                (keyup.enter)=\"login(usernameInput.value, passwordInput.value)\">LOGIN</button>\n    </mat-card>\n</div>\n\n<ng-template #logoutTemplate>\n    <div class=\"container login-page\">\n        <h1>Logout</h1>\n\n        <button mat-raised-button color=\"primary\" (click)=\"logout()\">LOGOUT</button>\n    </div>\n\n</ng-template>"

/***/ }),

/***/ "../../../../../src/app/pages/login-page/login-page.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".login-page {\n  padding: 21px 0; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/login-page/login-page.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LoginPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_app_services_user_service__ = __webpack_require__("../../../../../src/app/services/user.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_rxjs_operators_map__ = __webpack_require__("../../../../rxjs/_esm5/operators/map.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};





/**
 * Simple login page.
 *
 * @export
 * @class LoginPageComponent
 * @implements {OnInit}
 */
var LoginPageComponent = (function () {
    function LoginPageComponent(userService, router, bar) {
        this.userService = userService;
        this.router = router;
        this.bar = bar;
    }
    /**
     * Component setup.
     *
     * @memberof LoginPageComponent
     */
    LoginPageComponent.prototype.ngOnInit = function () {
        this.loggedIn = this.userService.get().pipe(Object(__WEBPACK_IMPORTED_MODULE_4_rxjs_operators_map__["a" /* map */])(function (user) { return user !== undefined && user['error'] === undefined; }));
    };
    /**
     * User login.
     *
     * @param {string} username Login name
     * @param {string} password Login Password
     * @memberof LoginPageComponent
     */
    LoginPageComponent.prototype.login = function (username, password) {
        var _this = this;
        this.userService.login(username, password).subscribe(function (user) {
            if (!user || user['error']) {
                _this.bar.open("Wrong Username or Password", 'CLOSE', { duration: 2500 });
            }
            else {
                _this.router.navigate(['/']);
            }
        });
    };
    /**
     * User logout.
     *
     * @memberof LoginPageComponent
     */
    LoginPageComponent.prototype.logout = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.userService.logout()];
                    case 1:
                        _a.sent();
                        this.router.navigateByUrl('/');
                        return [2 /*return*/];
                }
            });
        });
    };
    LoginPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-login-page',
            template: __webpack_require__("../../../../../src/app/pages/login-page/login-page.component.html"),
            styles: [__webpack_require__("../../../../../src/app/pages/login-page/login-page.component.scss")],
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_app_services_user_service__["a" /* UserService */],
            __WEBPACK_IMPORTED_MODULE_2__angular_router__["c" /* Router */],
            __WEBPACK_IMPORTED_MODULE_3__angular_material__["s" /* MatSnackBar */]])
    ], LoginPageComponent);
    return LoginPageComponent;
}());



/***/ }),

/***/ "../../../../../src/app/pages/settings-page/settings-page.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container settings-page\">\n    <h1 i18n=\"@@settings_header\">Settings</h1>\n\n    <h3>WPS Server List</h3>\n    <ng-container *ngIf=\"(wpsList | async)?.length > 0; else noWpsTemplate\">\n        <div *ngFor=\"let wps of wpsList | async\">\n            <mat-card @slide fxLayout=\"row\" fxLayoutAlign=\"space-between\">\n                <div>\n                    <div class=\"wps-title\">{{wps.title}}</div>\n                    <div class=\"wps-site\">{{wps.provider.site}}</div>\n                </div>\n                <button mat-button (click)=\"remove(wps.id)\" i18n=\"@@delete\" color=\"warn\">DELETE</button>\n            </mat-card>\n        </div>\n    </ng-container>\n    <ng-template #noWpsTemplate>\n        <mat-card fxLayout=\"row\" fxLayoutAlign=\"center\">\n            <span class=\"wps-site\">There Are Currently No WPS Server</span>\n        </mat-card>\n    </ng-template>\n\n    <br>\n    <br>\n\n    <div fxLayout=\"row\">\n        <div class=\"box-left\" fxFlex=\"70\">\n            <h3 i18n=\"@@settings_wps_header\">Add WPS server</h3>\n\n            <mat-card>\n                <mat-form-field>\n                    <input #url type=\"url\" placeholder=\"WPS Server URL\" (keyup.enter)=\"add(url.value)\" autocomplete=\"url\" matInput>\n                </mat-form-field>\n                <button class=\"add\" [disabled]=\"!url.value\" mat-button (click)=\"add(url.value)\" i18n=\"@@add\" color=\"primary\">ADD</button>\n                <div class=\"wps-site\">Add WPS server URL. Note that the URL must not end with a /wps. For example http://localhost:5000</div>\n            </mat-card>\n        </div>\n        <div fxFlex=\"30\">\n            <h3 i18n=\"@@settings_reload_wps\">Reload WPS server</h3>\n            <mat-card>\n                <button class=\"refresh\" (click)=\"refresh()\" mat-raised-button i18n=\"@@reload\">RELOAD</button>\n                <div class=\"wps-site\">Refreshes Process information for the entie WPS Server list.</div>\n            </mat-card>\n        </div>\n    </div>\n</div>"

/***/ }),

/***/ "../../../../../src/app/pages/settings-page/settings-page.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".settings-page {\n  padding: 21px 0; }\n\n.wps-site {\n  font-size: 12px;\n  color: rgba(0, 0, 0, 0.38); }\n\n.box-left {\n  margin-right: 13px; }\n\n.refresh {\n  width: 100%;\n  margin-bottom: 8px; }\n\n.add {\n  margin: 0 21px; }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/settings-page/settings-page.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SettingsPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_app_services_wps_service__ = __webpack_require__("../../../../../src/app/services/wps.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_animations__ = __webpack_require__("../../../animations/esm5/animations.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};




/**
 * Settings page.
 *
 * @export
 * @class SettingsPageComponent
 * @implements {OnInit}
 */
var SettingsPageComponent = (function () {
    /**
     * Creates an instance of SettingsPageComponent.
     *
     * @param {ProcessService} processService
     * @param {WpsService} wpsService
     * @memberof SettingsPageComponent
     */
    function SettingsPageComponent(processService, wpsService) {
        this.processService = processService;
        this.wpsService = wpsService;
    }
    /**
     * Component setup.
     *
     * @memberof SettingsPageComponent
     */
    SettingsPageComponent.prototype.ngOnInit = function () {
        this.wpsList = this.wpsService.all();
    };
    /**
     * Refreshes wps servers to check for new processes.
     *
     * @memberof SettingsPageComponent
     */
    SettingsPageComponent.prototype.refresh = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.wpsService.refresh()];
                    case 1:
                        _a.sent();
                        this.wpsList = this.wpsService.all();
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Adds wps server by a given wps server url.
     *
     * @param {string} url WPS server url
     * @memberof SettingsPageComponent
     */
    SettingsPageComponent.prototype.add = function (url) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.wpsService.create(url).toPromise()];
                    case 1:
                        _a.sent();
                        this.wpsList = this.wpsService.all();
                        this.urlComponent.nativeElement.value = '';
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * removes the wps server with the given id.
     *
     * @param id the id of the wps
     */
    SettingsPageComponent.prototype.remove = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.wpsService.remove(id)];
                    case 1:
                        _a.sent();
                        this.wpsList = this.wpsService.all();
                        return [2 /*return*/];
                }
            });
        });
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_12" /* ViewChild */])('url'),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["u" /* ElementRef */])
    ], SettingsPageComponent.prototype, "urlComponent", void 0);
    SettingsPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-settings-page',
            template: __webpack_require__("../../../../../src/app/pages/settings-page/settings-page.component.html"),
            styles: [__webpack_require__("../../../../../src/app/pages/settings-page/settings-page.component.scss")],
            animations: [
                Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["k" /* trigger */])('slide', [
                    Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["j" /* transition */])(':enter', [
                        Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["i" /* style */])({ transform: 'translateX(-100%)' }),
                        Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["e" /* animate */])('233ms ease-in-out')
                    ]),
                    Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["j" /* transition */])(':leave', [
                        Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["e" /* animate */])('233ms ease-in-out', Object(__WEBPACK_IMPORTED_MODULE_3__angular_animations__["i" /* style */])({ transform: 'translateX(100%)' }))
                    ]),
                ])
            ]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1_app_services_process_service__["a" /* ProcessService */],
            __WEBPACK_IMPORTED_MODULE_2_app_services_wps_service__["a" /* WpsService */]])
    ], SettingsPageComponent);
    return SettingsPageComponent;
}());



/***/ }),

/***/ "../../../../../src/app/pages/workflows-page/workflows-page.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container workflows-list\">\n    <h1 i18n=\"@@my_workflows\">My Workflows</h1>\n    <mat-accordion *ngIf=\"workflows && processes; else loadingTemplate\">\n\n        <ng-container *ngIf=\"workflows.length > 0; else noWorkflowsTemplate\">\n            <mat-expansion-panel *ngFor=\"let workflow of workflows\" (opened)=\"opened(workflow)\" (closed)=\"closed(workflow)\">\n                <mat-expansion-panel-header>\n                    <mat-panel-title>\n                        <span>{{ workflow.title }}</span>\n                        <span class=\"running\" *ngIf=\"runs(workflow) && !finished(workflow)\">(Running {{ workflow.percent_done }}%)</span>\n                        <span class=\"finished\" *ngIf=\"finished(workflow)\">(Finished)</span>\n                    </mat-panel-title>\n                    <div class=\"last-update\">{{ (workflow.updated_at * 1000) | date }}</div>\n                </mat-expansion-panel-header>\n\n                <app-editor *ngIf=\"workflow.id === openedWorkflowID\" class=\"editor\" [workflow]=\"workflow\" [processes]=\"processes\" class=\"editor\"></app-editor>\n                <div class=\"actions\">\n                    <div class=\"actions-left\">\n                        <button mat-button color=\"warn\" (click)=\"remove(workflow.id)\" i18n=\"@@delete\">Delete</button>\n                    </div>\n                    <div class=\"actions-right\">\n                        <button mat-raised-button (click)=\"edit(workflow.id)\" i18n=\"@@edit\">Edit</button>\n                        <button *ngIf=\"validate(workflow) && !finished(workflow)\" mat-raised-button color=\"primary\" (click)=\"run(workflow.id)\" [disabled]=\"runs(workflow)\">{{runs(workflow) ? 'RUNNING' : 'RUN'}}</button>\n                        <button *ngIf=\"finished(workflow)\" mat-raised-button color=\"primary\" disabled>FINISHED</button>\n                    </div>\n                </div>\n            </mat-expansion-panel>\n        </ng-container>\n        <ng-template #noWorkflowsTemplate>\n            <div class=\"no-workflows\">There Are Currently No Workflow, You Can Add Them In The Editor Page.</div>\n        </ng-template>\n\n    </mat-accordion>\n    <ng-template #loadingTemplate>\n        <mat-spinner class=\"spinner\" color=\"accent\"></mat-spinner>\n    </ng-template>\n</div>"

/***/ }),

/***/ "../../../../../src/app/pages/workflows-page/workflows-page.component.scss":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".workflows-list {\n  padding: 21px 0; }\n\n.actions {\n  margin-top: 20px;\n  display: -webkit-box;\n  display: -ms-flexbox;\n  display: flex;\n  -webkit-box-pack: justify;\n      -ms-flex-pack: justify;\n          justify-content: space-between; }\n\n.editor {\n  height: 50vh;\n  border: solid 1px #e0e0e0;\n  pointer-events: none; }\n\n.spinner {\n  margin: auto; }\n\n.last-update {\n  margin-right: 30px;\n  font-size: 13px;\n  line-height: 21px;\n  color: rgba(0, 0, 0, 0.34); }\n\n.no-workflows {\n  font-size: 13px;\n  line-height: 21px;\n  color: rgba(0, 0, 0, 0.34);\n  margin: 21px;\n  width: 100%;\n  text-align: center; }\n\n.running, .finished {\n  font-size: 13px;\n  line-height: 21px;\n  margin-left: 21px; }\n\n.finished {\n  color: rgba(33, 150, 243, 0.89); }\n\n.running {\n  color: rgba(255, 152, 0, 0.89); }\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/pages/workflows-page/workflows-page.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return WorkflowsPageComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_app_services_workflow_service__ = __webpack_require__("../../../../../src/app/services/workflow.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




/**
 * Workflow list page.
 *
 * @export
 * @class WorkflowsPageComponent
 * @implements {OnInit}
 */
var WorkflowsPageComponent = (function () {
    /**
     * Creates an instance of WorkflowsPageComponent.
     *
     * @param {ProcessService} processService
     * @param {WorkflowService} workflowService
     * @param {Router} router
     * @memberof WorkflowsPageComponent
     */
    function WorkflowsPageComponent(processService, workflowService, router) {
        this.processService = processService;
        this.workflowService = workflowService;
        this.router = router;
        this.openedWorkflowID = -1;
        this.running = [];
    }
    /**
     * Component setup.
     *
     * @memberof WorkflowsPageComponent
     */
    WorkflowsPageComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.workflowService.all().subscribe(function (workflows) { return _this.workflows = workflows; });
        this.processService.all().subscribe(function (processes) { return _this.processes = processes; });
    };
    /**
     * Checks whether a workflow is opened.
     *
     * @param workflow the workflow which is checked
     */
    WorkflowsPageComponent.prototype.opened = function (workflow) {
        this.openedWorkflowID = workflow.id;
    };
    /**
     * Checks whether a workflow is closed.
     *
     * @param workflow the workflow which is checked
     */
    WorkflowsPageComponent.prototype.closed = function (workflow) {
        if (this.openedWorkflowID === workflow.id) {
            this.openedWorkflowID = -1;
        }
    };
    /**
     * Removes a workflow.
     *
     * @param id Workflow id
     */
    WorkflowsPageComponent.prototype.remove = function (id) {
        var index = this.workflows.findIndex(function (workflow) { return workflow.id === id; });
        if (index !== -1) {
            this.workflows.splice(index, 1);
            this.workflowService.remove(id);
        }
    };
    /**
     * Routes to the editor opening a workflow.
     *
     * @param id Workflow id
     */
    WorkflowsPageComponent.prototype.edit = function (id) {
        this.router.navigate(["/editor/" + id]);
    };
    /**
     * Gets a workflow from the database.
     *
     * @param id Workflow id
     */
    WorkflowsPageComponent.prototype.getWorkflow = function (id) {
        return this.workflowService.get(id);
    };
    /**
     * Executes a workflow.
     *
     * @param id Workflow id
     */
    WorkflowsPageComponent.prototype.run = function (id) {
        this.workflowService.start(id);
        this.running.push(id);
    };
    /**
     * Validates a given workflow.
     *
     * @param workflow Workflow object
     */
    WorkflowsPageComponent.prototype.validate = function (workflow) {
        return this.workflowService.validate(workflow) === __WEBPACK_IMPORTED_MODULE_1_app_services_workflow_service__["b" /* WorkflowValidationResult */].SUCCESSFUL;
    };
    /**
     * Checks if a workflow is running.
     *
     * @param worflow Workflow to check
     */
    WorkflowsPageComponent.prototype.runs = function (workflow) {
        return this.workflowService.isRunning(workflow) || this.running.includes(workflow.id);
    };
    /**
     * Checks if a workflow is finished.
     *
     * @param worflow Workflow to check
     */
    WorkflowsPageComponent.prototype.finished = function (workflow) {
        return this.workflowService.finished(workflow);
    };
    WorkflowsPageComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-workflows-page',
            template: __webpack_require__("../../../../../src/app/pages/workflows-page/workflows-page.component.html"),
            styles: [__webpack_require__("../../../../../src/app/pages/workflows-page/workflows-page.component.scss")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_3_app_services_process_service__["a" /* ProcessService */],
            __WEBPACK_IMPORTED_MODULE_1_app_services_workflow_service__["a" /* WorkflowService */],
            __WEBPACK_IMPORTED_MODULE_2__angular_router__["c" /* Router */]])
    ], WorkflowsPageComponent);
    return WorkflowsPageComponent;
}());



/***/ }),

/***/ "../../../../../src/app/services/process.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return ProcessService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__ = __webpack_require__("../../../../../src/app/models/ProcessParameter.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




/**
 * Fetches process data from server.
 *
 * @export
 * @class ProcessService
 */
var ProcessService = (function () {
    /**
     * Constructs process Service.
     *
     * @param {HttpClient} http
     */
    function ProcessService(http) {
        this.http = http;
    }
    /**
     * Return color for each process parameter type.
     *
     * @param {ProcessParameterType} type
     * @returns {string} Hexadecimal color number as string
     */
    ProcessService.getTypeColor = function (type) {
        switch (type) {
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].LITERAL: return '#03A9F4';
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX: return '#FFC107';
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX: return '#4CAF50';
            default: return '#000000';
        }
    };
    /**
     * Return the name of each process parameter type.
     *
     * @param {ProcessParameterType} type
     * @returns {string} name
     */
    ProcessService.getTypeName = function (type) {
        switch (type) {
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].LITERAL: return 'Literal';
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].COMPLEX: return 'Complex';
            case __WEBPACK_IMPORTED_MODULE_2__models_ProcessParameter__["a" /* ProcessParameterType */].BOUNDING_BOX: return 'Bounding Box';
            default: return 'Undefined';
        }
    };
    /**
     * Returns observable of all processes.
     *
     * @returns {Observable<Process[]>}
     */
    ProcessService.prototype.all = function () {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_3_environments_environment__["a" /* environment */].ip + "/process/", { withCredentials: true });
    };
    /**
     * Returns process with given id.
     *
     * @param {number} id
     * @returns {Observable<Process>}
     */
    ProcessService.prototype.get = function (id) {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_3_environments_environment__["a" /* environment */].ip + "/process/" + id, { withCredentials: true });
    };
    ProcessService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]])
    ], ProcessService);
    return ProcessService;
}());



/***/ }),

/***/ "../../../../../src/app/services/user.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return UserService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators__ = __webpack_require__("../../../../rxjs/_esm5/operators.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};





/**
 * Fetches users data from server.
 *
 * @export
 * @class UserService
 */
var UserService = (function () {
    function UserService(http, router) {
        this.http = http;
        this.router = router;
    }
    /**
     * Returns currently logged in user.
     *
     * @returns {Observable<User>} Logged in User.
     * @memberof UserService
     */
    UserService.prototype.get = function () {
        var _this = this;
        return this.http.get(__WEBPACK_IMPORTED_MODULE_4_environments_environment__["a" /* environment */].ip + "/user/", { withCredentials: true }).pipe(Object(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__["c" /* map */])(function (message) {
            if (message['error']) {
                _this.router.navigate(['/login']);
            }
            return message;
        }));
    };
    /**
     * User login.
     *
     * @param {string} username Username
     * @param {string} password Password
     * @returns {Observable<User>} Loggedin User
     * @memberof UserService
     */
    UserService.prototype.login = function (username, password) {
        return this.http.post(__WEBPACK_IMPORTED_MODULE_4_environments_environment__["a" /* environment */].ip + "/login/", { username: username, password: password }, { withCredentials: true });
    };
    /**
     * User logout.
     *
     * @returns {Promise<any>} Logout promise
     * @memberof UserService
     */
    UserService.prototype.logout = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.http.delete(__WEBPACK_IMPORTED_MODULE_4_environments_environment__["a" /* environment */].ip + "/logout/", { withCredentials: true }).toPromise()];
            });
        });
    };
    UserService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_3__angular_router__["c" /* Router */]])
    ], UserService);
    return UserService;
}());



/***/ }),

/***/ "../../../../../src/app/services/workflow.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return WorkflowValidationResult; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return WorkflowService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_Task__ = __webpack_require__("../../../../../src/app/models/Task.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_app_services_process_service__ = __webpack_require__("../../../../../src/app/services/process.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};






/**
 * Different workflow validation results
 */
var WorkflowValidationResult;
(function (WorkflowValidationResult) {
    /**
     * Unknown Error
     */
    WorkflowValidationResult[WorkflowValidationResult["ERROR"] = 0] = "ERROR";
    /**
     * Valid workflow
     */
    WorkflowValidationResult[WorkflowValidationResult["SUCCESSFUL"] = 1] = "SUCCESSFUL";
    /**
     * Workflow title too long
     */
    WorkflowValidationResult[WorkflowValidationResult["TITLE_TOO_LONG"] = 2] = "TITLE_TOO_LONG";
    /**
     * Workflow title too short
     */
    WorkflowValidationResult[WorkflowValidationResult["TITLE_TOO_SHORT"] = 3] = "TITLE_TOO_SHORT";
    /**
     * Workflow is empty
     */
    WorkflowValidationResult[WorkflowValidationResult["EMPTY"] = 4] = "EMPTY";
    /**
     * Workflow has a task with loop to itself
     */
    WorkflowValidationResult[WorkflowValidationResult["LOOP_TO_SAME_TASK"] = 5] = "LOOP_TO_SAME_TASK";
    /**
     * Workflow has edges to tasks with not matching in-/output types
     */
    WorkflowValidationResult[WorkflowValidationResult["WRONG_INPUT_TYPES"] = 6] = "WRONG_INPUT_TYPES";
    /**
     * Workflow has a task without inputs
     */
    WorkflowValidationResult[WorkflowValidationResult["MISSING_TASK_INPUT"] = 7] = "MISSING_TASK_INPUT";
    /**
     * Missing Workflow
     */
    WorkflowValidationResult[WorkflowValidationResult["MISSING_WORKFLOW"] = 8] = "MISSING_WORKFLOW";
    /**
     * Missing Processes
     */
    WorkflowValidationResult[WorkflowValidationResult["MISSING_PROCESSES"] = 9] = "MISSING_PROCESSES";
    /**
     * Workflow has a cycle
     */
    WorkflowValidationResult[WorkflowValidationResult["CYCLE_IN_WORKFLOW"] = 10] = "CYCLE_IN_WORKFLOW";
    /**
     * Workflow has task with multiple inputs
     */
    WorkflowValidationResult[WorkflowValidationResult["MULIPLE_INPUTS"] = 11] = "MULIPLE_INPUTS";
})(WorkflowValidationResult || (WorkflowValidationResult = {}));
/**
 * Fetches workflow data from server.
 *
 * @export
 * @class WorkflowService
 */
var WorkflowService = (function () {
    /**
     * Constructs workflowService.
     *
     * @param {HttpClient} http
     * @param {MatSnackBar} bar
     * @param {ProcessService} processService
     */
    function WorkflowService(http, bar, processService) {
        var _this = this;
        this.http = http;
        this.bar = bar;
        this.processService = processService;
        this.processService.all().subscribe(function (processes) { return _this.processes = processes; });
    }
    /**
     * Returns Observable of all Workflows.
     *
     * @returns {Observable<Workflow[]>}
     */
    WorkflowService.prototype.all = function () {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow/", { withCredentials: true });
    };
    /**
     * Returns Observable of the Workflow with the given id.
     *
     * @param {number} id
     * @returns {Observable<Workflow>}
     */
    WorkflowService.prototype.get = function (id) {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow/" + id, { withCredentials: true });
    };
    /**
     * Create an Observable to a given partial workflow.
     *
     * @param {Partial<Workflow>} workflow
     * @returns {Observable<Workflow>}
     */
    WorkflowService.prototype.create = function (workflow) {
        return this.http.post(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow/", workflow, { withCredentials: true });
    };
    /**
     * Refreshes the observable of the given workflow.
     *
     * @param {number} id
     * @param {Partial<Workflow>} workflow
     * @returns {Observable<Workflow>}
     */
    WorkflowService.prototype.update = function (id, workflow) {
        this.bar.open("Updated Workflow", 'CLOSE', { duration: 2500 });
        return this.http.patch(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow/" + id, workflow, { withCredentials: true });
    };
    /**
     * Removes the workflow with the given id.
     *
     * @param {number} id
     * @returns {Promise<boolean>}
     */
    WorkflowService.prototype.remove = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.bar.open("Deleted Workflow", 'CLOSE', { duration: 2500 });
                return [2 /*return*/, this.http.delete(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow/" + id, { withCredentials: true }).toPromise()];
            });
        });
    };
    /**
     * Returns if the workflow is running (workflow can't be running if not runnable).
     *
     * @param {Partial<Workflow>} workflow
     * @returns {boolean}
     */
    WorkflowService.prototype.isRunning = function (workflow) {
        if (!workflow || !workflow.tasks || workflow.tasks.length === 0) {
            return false;
        }
        for (var _i = 0, _a = workflow.tasks; _i < _a.length; _i++) {
            var task = _a[_i];
            if (task.state !== __WEBPACK_IMPORTED_MODULE_1__models_Task__["a" /* TaskState */].NONE) {
                return true;
            }
        }
        return false;
    };
    /**
     * Checks whether a workflow is finished.
     *
     * @param {Partial<Workflow>} workflow Workflow to check
     * @returns {boolean} Finished
     * @memberof WorkflowService
     */
    WorkflowService.prototype.finished = function (workflow) {
        if (!workflow || !workflow.tasks || workflow.tasks.length === 0) {
            return false;
        }
        for (var _i = 0, _a = workflow.tasks; _i < _a.length; _i++) {
            var task = _a[_i];
            if (task.state !== __WEBPACK_IMPORTED_MODULE_1__models_Task__["a" /* TaskState */].FINISHED
                && task.state !== __WEBPACK_IMPORTED_MODULE_1__models_Task__["a" /* TaskState */].DEPRECATED
                && task.state !== __WEBPACK_IMPORTED_MODULE_1__models_Task__["a" /* TaskState */].FAILED) {
                return false;
            }
        }
        return true;
    };
    /**
     * Returns if the workflow is a valid workflow for execution.
     *
     * @param {Workflow} workflow
     * @returns {WorkflowValidationResult}
     */
    WorkflowService.prototype.validate = function (workflow) {
        if (!workflow) {
            return WorkflowValidationResult.MISSING_WORKFLOW;
        }
        else if (!this.processes) {
            return WorkflowValidationResult.MISSING_PROCESSES;
        }
        // check name
        if (!workflow.title || workflow.title.length > 255) {
            return WorkflowValidationResult.TITLE_TOO_LONG;
        }
        else if (workflow.title.length < 1) {
            return WorkflowValidationResult.TITLE_TOO_SHORT;
        }
        else if (workflow.tasks && workflow.tasks.length < 1) {
            return WorkflowValidationResult.EMPTY;
        }
        else if (workflow.edges) {
            for (var i = 0; i < workflow.edges.length; i++) {
                // check for loop to same task
                if (workflow.edges[i].from_task_id === workflow.edges[i].to_task_id) {
                    return WorkflowValidationResult.LOOP_TO_SAME_TASK;
                }
                // check for wrong input types
                var inputTaskNumber = null;
                var outputTaskNumber = null;
                for (var j = 0; j < workflow.tasks.length; j++) {
                    if (workflow.tasks[j].id === workflow.edges[i].to_task_id) {
                        inputTaskNumber = workflow.tasks[j].process_id;
                    }
                    if (workflow.tasks[j].id === workflow.edges[i].from_task_id) {
                        outputTaskNumber = workflow.tasks[j].process_id;
                    }
                }
                var inputProcessNumber = null;
                var outputPrecessNumber = null;
                for (var k = 0; k < this.processes.length; k++) {
                    if (this.processes[k].id === inputTaskNumber) {
                        inputProcessNumber = k;
                    }
                    if (this.processes[k].id === outputTaskNumber) {
                        outputPrecessNumber = k;
                    }
                }
                var processParameterTypeCorrect = false;
                for (var l = 0; l < this.processes[inputProcessNumber].inputs.length; l++) {
                    for (var m = 0; m < this.processes[outputPrecessNumber].outputs.length; m++) {
                        if (this.processes[inputProcessNumber].inputs[l].type === this.processes[outputPrecessNumber].outputs[m].type) {
                            processParameterTypeCorrect = true;
                        }
                    }
                }
                if (!processParameterTypeCorrect) {
                    return WorkflowValidationResult.WRONG_INPUT_TYPES;
                }
            }
        }
        // check for missing input
        if (workflow.tasks && workflow.edges) {
            for (var i = 0; i < workflow.tasks.length; i++) {
                var numberOfInputs = 0;
                for (var k = 0; k < workflow.edges.length; k++) {
                    if (workflow.edges[k].to_task_id === workflow.tasks[i].id) {
                        numberOfInputs++;
                    }
                }
                numberOfInputs += workflow.tasks[i].input_artefacts.length;
                for (var j = 0; j < this.processes.length; j++) {
                    if (workflow.tasks[i].process_id === this.processes[j].id) {
                        if (numberOfInputs < this.processes[j].inputs.length) {
                            return WorkflowValidationResult.MISSING_TASK_INPUT;
                        }
                    }
                }
            }
        }
        // cycle check
        if (workflow.tasks && workflow.edges) {
            for (var i = 0; i < workflow.tasks.length; i++) {
                for (var j = 0; j < workflow.edges.length; j++) {
                    var checkedTasks = [];
                    if (workflow.tasks[i].id === workflow.edges[j].to_task_id) {
                        var visitedTasks = [];
                        if (!this.contains(checkedTasks, workflow.edges[j].from_task_id)) {
                            if (this.checkCycle(workflow.edges[j], workflow, visitedTasks)) {
                                return WorkflowValidationResult.CYCLE_IN_WORKFLOW;
                            }
                            checkedTasks = visitedTasks;
                        }
                    }
                }
            }
        }
        // check for multiple inputs
        if (workflow.edges) {
            for (var i = 0; i < workflow.edges.length; i++) {
                for (var j = i + 1; j < workflow.edges.length; j++) {
                    if (workflow.edges[i].to_task_id === workflow.edges[j].to_task_id && workflow.edges[i].input_id === workflow.edges[j].input_id) {
                        return WorkflowValidationResult.MULIPLE_INPUTS;
                    }
                }
            }
        }
        return WorkflowValidationResult.SUCCESSFUL;
    };
    /**
     * Checks if an array contains a variable.
     *
     * @param {Array<T>} array
     * @param {T} variable
     * @returns {boolean}
     */
    WorkflowService.prototype.contains = function (array, variable) {
        for (var i = 0; i < array.length; i++) {
            if (array[i] === variable) {
                return true;
            }
        }
        return false;
    };
    /**
     * Recursive method to check for cycle in workflow.
     *
     * @param {Edge} currentWorkflowEdge starting edge
     * @param {Partial<Workflow>} workflow entire workflow
     * @param {number[]} visitedTasks list of visited Tasks (empty for 1st run)
     * @returns {boolean}
     */
    WorkflowService.prototype.checkCycle = function (currentWorkflowEdge, workflow, visitedTasks) {
        visitedTasks.push(currentWorkflowEdge.to_task_id);
        // check task at end of edge
        for (var i = 0; i < workflow.tasks.length; i++) {
            if (this.contains(visitedTasks, currentWorkflowEdge.from_task_id)) {
                return true;
            }
            if (workflow.tasks[i].id === currentWorkflowEdge.to_task_id) {
                // check for new edges at task
                var cycle = false;
                for (var j = 0; j < workflow.edges.length; j++) {
                    if (workflow.edges[j].to_task_id === currentWorkflowEdge.to_task_id) {
                        if (this.contains(visitedTasks, workflow.edges[j].from_task_id)) {
                            return true;
                        }
                        for (var l = 0; l < workflow.edges.length; l++) {
                            if (workflow.edges[j].from_task_id === workflow.edges[l].to_task_id) {
                                var newVisitedTasks = [];
                                for (var k = 0; k < visitedTasks.length; k++) {
                                    newVisitedTasks.push(visitedTasks[k]);
                                }
                                cycle = cycle || this.checkCycle(workflow.edges[l], workflow, newVisitedTasks);
                            }
                        }
                    }
                }
                return cycle;
            }
        }
        return false;
    };
    /**
     * Execute given workflow.
     *
     * @param {number} id
     * @returns {Promise<boolean>}
     */
    WorkflowService.prototype.start = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            var result;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow_start/" + id).toPromise()];
                    case 1:
                        result = _a.sent();
                        if (result['error']) {
                            this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
                            return [2 /*return*/, false];
                        }
                        else {
                            return [2 /*return*/, true];
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Refreshes workflow by a given workflow ID.
     *
     * @param {number} id Workflow ID
     * @returns {Promise<boolean>} Refresh successful
     * @memberof WorkflowService
     */
    WorkflowService.prototype.refresh = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            var result;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow_refresh/" + id).toPromise()];
                    case 1:
                        result = _a.sent();
                        if (result['error']) {
                            this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
                            return [2 /*return*/, false];
                        }
                        else {
                            return [2 /*return*/, true];
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    /**
     * Stops workflow by a given workflow id.
     *
     * @param {number} id Workflow ID
     * @returns {Promise<boolean>} Stop successful
     * @memberof WorkflowService
     */
    WorkflowService.prototype.stop = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            var result;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/workflow_stop/" + id).toPromise()];
                    case 1:
                        result = _a.sent();
                        if (result['error']) {
                            this.bar.open(result['error'], 'CLOSE', { duration: 5000 });
                            return [2 /*return*/, false];
                        }
                        else {
                            return [2 /*return*/, true];
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    WorkflowService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_3__angular_material__["s" /* MatSnackBar */], __WEBPACK_IMPORTED_MODULE_4_app_services_process_service__["a" /* ProcessService */]])
    ], WorkflowService);
    return WorkflowService;
}());



/***/ }),

/***/ "../../../../../src/app/services/wps.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return WpsService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_rxjs_operators__ = __webpack_require__("../../../../rxjs/_esm5/operators.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3_rxjs_observable_ErrorObservable__ = __webpack_require__("../../../../rxjs/_esm5/observable/ErrorObservable.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_material__ = __webpack_require__("../../../material/esm5/material.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};






/**
 * Fetches wps data from server.
 *
 * @export
 * @class WpsService
 */
var WpsService = (function () {
    /**
     * Constructs wps service.
     *
     * @param {HttpClient} http
     * @param {MatSnackBar} bar
     */
    function WpsService(http, bar) {
        this.http = http;
        this.bar = bar;
    }
    /**
     * Returns an observable to all WPS.
     *
     * @returns {Observable<WPS[]>}
     */
    WpsService.prototype.all = function () {
        return this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/wps/", { withCredentials: true });
    };
    /**
     * Create WPS and returns observable of WPS.
     * currently disabled
     *
     * @param {string} url
     * @returns {Observable<WPS>}
     */
    WpsService.prototype.create = function (url) {
        var _this = this;
        this.bar.open("Created WPS", 'CLOSE', { duration: 3000 });
        return this.http.post(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/wps/", url, { withCredentials: true }).pipe(Object(__WEBPACK_IMPORTED_MODULE_2_rxjs_operators__["a" /* catchError */])(function (error) {
            _this.bar.open("ERROR. Can not add WPS Server. Wrong URL?", 'CLOSE', { duration: 5000 });
            return new __WEBPACK_IMPORTED_MODULE_3_rxjs_observable_ErrorObservable__["a" /* ErrorObservable */]("can't create wps");
        }));
    };
    /**
     * Removes WPS with given id.
     *
     * @param {number} id
     * @returns {Promise<boolean>}
     */
    WpsService.prototype.remove = function (id) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.bar.open("Deleted WPS", 'CLOSE', { duration: 3000 });
                return [2 /*return*/, this.http.delete(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/wps/" + id, { withCredentials: true }).toPromise()];
            });
        });
    };
    /**
     * Refreshes all wps servers.
     *
     * @returns {Promise<boolean>} Refresh succsessful
     * @memberof WpsService
     */
    WpsService.prototype.refresh = function () {
        return __awaiter(this, void 0, void 0, function () {
            var result;
            return __generator(this, function (_a) {
                this.bar.open("Refreshed WPS Processes", 'CLOSE', { duration: 3000 });
                result = this.http.get(__WEBPACK_IMPORTED_MODULE_5_environments_environment__["a" /* environment */].ip + "/wps_refresh/", { withCredentials: true }).toPromise();
                return [2 /*return*/, result['error'] === undefined];
            });
        });
    };
    WpsService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["C" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */], __WEBPACK_IMPORTED_MODULE_4__angular_material__["s" /* MatSnackBar */]])
    ], WpsService);
    return WpsService;
}());



/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return environment; });
// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
var environment = {
    production: false,
    ip: 'https://vforwater-gis.scc.kit.edu/:8000/wps_workflow',
};


/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/esm5/platform-browser-dynamic.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_hammerjs__ = __webpack_require__("../../../../hammerjs/hammer.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_hammerjs___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_4_hammerjs__);





if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_18" /* enableProdMode */])();
}
// we use the webpack raw-loader to return the content as a string
var translations = __webpack_require__("../../../../raw-loader/index.js!../../../../../src/locale/messages.de.xlf");
/**
 * translation is loaded here
 */
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */], {
    missingTranslation: __WEBPACK_IMPORTED_MODULE_0__angular_core__["J" /* MissingTranslationStrategy */].Error,
    providers: [
        { provide: __WEBPACK_IMPORTED_MODULE_0__angular_core__["_7" /* TRANSLATIONS */], useValue: translations },
        { provide: __WEBPACK_IMPORTED_MODULE_0__angular_core__["_8" /* TRANSLATIONS_FORMAT */], useValue: 'xlf' }
    ]
});


/***/ }),

/***/ "../../../../raw-loader/index.js!../../../../../src/locale/messages.de.xlf":
/***/ (function(module, exports) {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<xliff version=\"1.2\" xmlns=\"urn:oasis:names:tc:xliff:document:1.2\">\n  <file source-language=\"en\" datatype=\"plaintext\" original=\"ng2.template\">\n    <body>\n      <trans-unit id=\"editor_header\" datatype=\"html\">\n        <source>Editor</source>\n        <target>Editor</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/app/app.component.ts</context>\n          <context context-type=\"linenumber\">5</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"workflows_header\" datatype=\"html\">\n        <source>Workflows</source>\n        <target>Workflows</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/app/app.component.ts</context>\n          <context context-type=\"linenumber\">6</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"settings_header\" datatype=\"html\">\n        <source>Settings</source>\n        <target>Einstellungen</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/app/app.component.ts</context>\n          <context context-type=\"linenumber\">7</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">2</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"close\" datatype=\"html\">\n        <source>Close</source>\n        <target>Schließen</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/process-dialog/process-dialog.component.ts</context>\n          <context context-type=\"linenumber\">47</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/artefact-dialog/artefact-dialog.component.ts</context>\n          <context context-type=\"linenumber\">56</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/result-dialog/result-dialog.component.ts</context>\n          <context context-type=\"linenumber\">11</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"delete\" datatype=\"html\">\n        <source>DELETE</source>\n        <target>LÖSCHEN</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/artefact-dialog/artefact-dialog.component.ts</context>\n          <context context-type=\"linenumber\">59</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/task/task.component.ts</context>\n          <context context-type=\"linenumber\">3</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/workflows-page/workflows-page.component.ts</context>\n          <context context-type=\"linenumber\">19</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">12</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"save\" datatype=\"html\">\n        <source>SAVE</source>\n        <target>SPEICHERN</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/artefact-dialog/artefact-dialog.component.ts</context>\n          <context context-type=\"linenumber\">60</context>\n        </context-group>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/editor-page/editor-page.component.ts</context>\n          <context context-type=\"linenumber\">20</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"info\" datatype=\"html\">\n        <source>Info</source>\n        <target>Info</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/components/task/task.component.ts</context>\n          <context context-type=\"linenumber\">2</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"undo\" datatype=\"html\">\n        <source>UNDO</source>\n        <target>RÜCKGÄNGIG</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/editor-page/editor-page.component.ts</context>\n          <context context-type=\"linenumber\">19</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"my_workflows\" datatype=\"html\">\n        <source>My Workflows</source>\n        <target>Meine Workflows</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/workflows-page/workflows-page.component.ts</context>\n          <context context-type=\"linenumber\">2</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"edit\" datatype=\"html\">\n        <source>Edit</source>\n        <target>Bearbeiten</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/workflows-page/workflows-page.component.ts</context>\n          <context context-type=\"linenumber\">22</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"settings_wps_header\" datatype=\"html\">\n        <source>Add WPS server</source>\n        <target>WPS Server hinzufügen</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">27</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"add\" datatype=\"html\">\n        <source>ADD</source>\n        <target>HINZUFÜGEN</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">33</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"settings_reload_wps\" datatype=\"html\">\n        <source>Reload WPS server</source>\n        <target>WPS Server neu laden</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">38</context>\n        </context-group>\n      </trans-unit>\n      <trans-unit id=\"reload\" datatype=\"html\">\n        <source>RELOAD</source>\n        <target>Neu laden</target>\n        <context-group purpose=\"location\">\n          <context context-type=\"sourcefile\">app/pages/settings-page/settings-page.component.ts</context>\n          <context context-type=\"linenumber\">40</context>\n        </context-group>\n      </trans-unit>\n    </body>\n  </file>\n</xliff>\n"

/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map
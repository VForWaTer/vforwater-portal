import {Component, OnInit, Inject, ViewEncapsulation, ViewChild, ElementRef} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {Workflow} from 'app/models/Workflow';
import {Artefact} from 'app/models/Artefact';



/**
 * Component Class
 * @class ResultDialogComponent
 * @export
 * @implements {OnInit}
 */
@Component({
    selector: 'app-result-dialog',
    templateUrl: './result-dialog.component.html',
    styleUrls: ['./result-dialog.component.scss'],
})
export class ResultDialogComponent implements OnInit
{

    /**
     * creates an artefact object
     * @param data the artefact data
     * @param dialog the artefact dialog
     */
    constructor(
        @Inject(MAT_DIALOG_DATA) public workflow: Workflow,
        public dialog: MatDialogRef<ResultDialogComponent>
    )
    {

    }


    /**
     *
     */
    public ngOnInit()
    {

    }

    /**
     *
     * @returns {any[]}
     */
    public get results(): Artefact<'output'>[]
    {
        const out = [];
        for (const task of this.workflow.tasks)
        {
            for (const artefact of task.output_artefacts)
            {
                if (this.workflow.edges.findIndex(edge => edge.output_id === artefact.parameter_id && edge.from_task_id === task.id) === -1)
                {
                    out.push(artefact);
                }
            }
        }
        return out;
    }
}

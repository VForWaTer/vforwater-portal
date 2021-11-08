class Box {

    /**
     * Box class to be added (dropped) on a draw2d.Canvas Element.
     * @param {string} name Name of the box
     * @param {string} name Name of the box
     * @param {string} orgId ID of the dataset used on the website out of workflowjs
     * @param {string} type Used to define style of box. Implemented is 'tool', which increases the height of the box
     * @param {list} inputs List of strings to define port types. Implemented are timeseries, string, boolean
     * @param {list} outputs List of strings to define port types. Implemented are timeseries, string, boolean
     * @param {number} boxwidth ~90% of the width of the box
     * @param {string} sessionstore Source of the button
     * @param {string} service wps of tool
     * @param {string} boxid originally given from draw2d
     */
    constructor(name, orgId, type, inputs, outputs,
                sessionstore, service, boxID) {
        this._boxname = name;
        this._service = service;
        this._sessionstore = sessionstore;
        this._orgid = orgId;
        this._boxid = boxID;
        this._boxtype = type;
        this._inputs = inputs;
        this._outputs = outputs;
        // assign text width:
        let c = document.getElementById('textWidthCanvas');
        let ctx = c.getContext("2d");
        ctx.font = "15px Arial";
        this._boxwidth = ctx.measureText(name).width
        // this._boxwidth = 0;
        this._connectable_types = ['array', 'iarray', 'varray', 'ndarray', '_2darray',
            'timeseries', 'vtimeseries', 'raster', 'vraster', 'idataframe', 'vdataframe',
            'time-dataframe', 'vtime-dataframe', 'html', 'plot', 'figure', 'image',
            'string', 'boolean', 'float', 'integer', 'positiveInteger', 'dateTime', 'list']
    }

    /**
     * Public function to create a box.
     * @public
     * @return {draw2d.shape} A box with ports to be placed on a draw2d.canvas.
     */
    get box() {
        return this._createBox();
    }

    /**
     * Private function to create a box. Called from get box()
     * @private
     * @return {draw2d.shape} A box with ports to be placed on a draw2d.canvas.
     */
    _createBox() {
        // create a blank box with name and class TODO: and ID
        let box = this._blankBox()

        // add ports to the box
        let relOutPort_y;
        let outPortDist = (this._outputs.length / ((3 + this._outputs.length) * this._outputs.length)) * 100
        let relInPort_y;
        let inPortDist = (this._inputs.length / ((3 + this._inputs.length) * this._inputs.length)) * 100
        for (let i in this._outputs) {
            if (this._connectable_types.includes(this._outputs[i])) {
                relOutPort_y = 100
            } else {
                relOutPort_y = 97
            }
            this._createOutPort(box, this._outputs[i], 100 - (parseInt(i) + 1) * outPortDist, relOutPort_y)
        }
        for (let i in this._inputs) {
            if (this._connectable_types.includes(this._inputs[i])) {
                relInPort_y = 0
            } else {
                relInPort_y = 3
            }
            this._createInPort(box, this._inputs[i], (parseInt(i) + 1) * inPortDist, relInPort_y)
        }
        return box
    }

    /**
     * Create a simple box. Height of the box is defined through the type of the box.
     * @private
     * @return {draw2d.shape} A blank box without any ports to be extended or placed on a draw2d.canvas.
     */
    _blankBox() {
        let boxHeight = 30;
        let boxTexty = 3;
        let boxType = this._boxtype;
        // let boxId = 'box' + this._orgid;
        let name = this._orgid;
        let service = this._service;

        if (boxType === 'tool') {
            boxHeight = 50;
            boxTexty = 12;
        }

        let box = new draw2d.shape.basic.Rectangle({
            // id: boxId,
            minWidth: 100,
            width: this._boxwidth * 1.1,
            height: boxHeight,
            // resizable: true,
            radius: 5,
            bgColor: '#D9EFFD',
            stroke: 0,
            cssClass: 'box-' + this._boxtype,
        })
        box.attr({id: boxId})
        let label = new draw2d.shape.basic.Label({
                text: this._boxname,
                stroke: 0,
                fontSize: 15,
                x: 5,  // Position of text in box
                y: boxTexty
            })
        if (boxType === 'tool') {
            box.on('click', function () {
                wpsprocess(service, name);
            })
            label.on('click', function () {
                wpsprocess(service, name);
            })
        }
        box.on('removed', function(ev) {
            update_workflow({'state': 'remove', 'id': ev.id})
        })
        box.add(
            label,
            new draw2d.layout.locator.Locator());

        // Don't show handles around rectangle when moving it
        box.installEditPolicy(new draw2d.policy.figure.GlowSelectionFeedbackPolicy())
        return box
    }

    /**
     * Take a simple/blank box and add output ports to it.
     * @private
     * @param {draw2d.shape} blankbox Object to add the port to.
     * @param {String} porttype Definies CSS class to style port.
     * @param {Number} relPortx Relative position of x in percent; 0,0 is upper left.
     * @param {Number} relPorty Relative position of y in percent; 0,0 is upper left.
     * @return {draw2d.shape} The input Objected with an port added.
     */
    _createOutPort(blankbox, porttype, relPortx, relPorty) {
        // let port = new draw2d.OutputPort();
        let port = blankbox.createPort(
            'output',
            new draw2d.layout.locator.XYRelPortLocator(relPortx, relPorty),  // Position in % of box 0,0 is upper left
        );
        port.setCssClass(porttype)

        port.on('click', function () {
            console.log('clicked on outPort, this: ', this)
            console.log('parent: ', port.getParent())
            // console.log('policy: ', port.installEditPolicy(new draw2d.policy.ResizeSelectionFeedbackPolicy()))
        })
        port.setConnectionDirection(2)
        port.setValue(this._orgid)
        port.setUserData(this._service)
        return blankbox
    }

    /**
     * Take a simple/blank box and add input ports to it.
     * @private
     * @param {draw2d.shape} blankbox Object to add the port to
     * @param {String} porttype definies CSS class to style port
     * @param {Number} relPortx relative position of x in percent; 0,0 is upper left
     * @param {Number} relPorty relative position of y in percent; 0,0 is upper left
     * @return {draw2d.shape} The input Objected with an port added.
     */
    _createInPort(blankbox, porttype, relPortx, relPorty) {
        let port;
        port = blankbox.createPort(
            'input',
            new draw2d.layout.locator.XYRelPortLocator(relPortx, relPorty),
        );
        /*// hide port when connected
        let show=function(){this.setVisible(true);};
        let hide=function(){this.setVisible(false);};
        port.on('connect',hide, port);
        port.on('disconnect',show, port);*/

        port.setCssClass(porttype)
        port.on('click', function () {
            console.log('clicked Inport: this: ', this)
            console.log('parent: ', port.getParent())
            // console.log('policy: ', port.installEditPolicy(new draw2d.policy.ResizeSelectionFeedbackPolicy()))
        })
        port.on("connect", function(emitterPort, connection){
            // console.log('emitterPort: ', emitterPort.getValue())
            // console.log('emitterPort: ', emitterPort.getUserData())
            if (connection.port.getCssClass() === connection.connection.sourcePort.getCssClass()) {

            }
            console.log('connection: ', connection.connection.sourcePort.getUserData())
            console.log('connection: ', connection.connection.sourcePort.getValue())
            console.log('connection: ', connection.connection.sourcePort.getCssClass())
            console.log('connection port: ', connection.port.getValue())
            console.log('connection port: ', connection.port.getUserData())
            console.log('connection port: ', connection.port.getCssClass())
            console.log('port: ', port)
            console.log('port: ', port.getValue())
            console.log('port: ', port.getUserData())
            console.log(port.getCoronaWidth())
 });
        // console.log('onDragEnter: ', port.onDragEnter(function () {console.log('Enter')}))
        // port.attr({selectable: false})
        // port.setDraggable(false)
        port.setConnectionDirection(0)
        // port.setValue('TestValue')
        // port.setUserData('TestUserData')
        port.setValue(this._orgid)
        port.setUserData(this._service)
        return blankbox
    }
}

class Connection {

    constructor() {
    }

    /**
     * Define the connection policy (the style of the connection between ports).
     * @public
     * @return {draw2d.policy.connection.ConnectionCreatePolicy} Defines the style of the connection used on a draw2d.canvas.
     */
    get connectionPolicy() {
        return this._createConnection();
    }

    /**
     * Actual (private) function to define the connection policy (the style of the connection between ports).
     * Called from get connectionPolicy.
     * @private
     * @return {draw2d.policy.connection.ConnectionCreatePolicy} The actual connection used on a draw2d.canvas.
     */
    _createConnection() {
        let connector_function = function () {
            // To options to connect ports. A) spline, B) rubber band
            // A) Define a spline to connect ports
            let SplineCon = new draw2d.Connection();
            SplineCon.setRouter(new draw2d.layout.connection.SplineConnectionRouter());
            // Add Arrow to spline end
            let arrow = new draw2d.decoration.connection.ArrowDecorator(17, 12);
            arrow.setBackgroundColor(new draw2d.util.Color("#326dc4"))
            SplineCon.setTargetDecorator(arrow);
            return SplineCon

            /*// b) Define a rubber band to connect ports
            let RubberConnection = draw2d.Connection.extend({
                NAME: "RubberConnection",

                init: function (attr, setter, getter) {
                    this._super($.extend({
                            color: "#33691e",
                            stroke: 1,
                            outlineStroke: 0,
                            outlineColor: null
                        }, attr),
                        setter,
                        getter);
                    this.setRouter(new draw2d.layout.connection.RubberbandRouter());
                },

                repaint: function (attributes) {
                    if (this.repaintBlocked === true || this.shape === null) {
                        return;
                    }
                    attributes = attributes || {};
                    // enrich the rendering with a "fill" attribute
                    if (typeof attributes.fill === "undefined") {
                        attributes.fill = "#aed581";
                    }
                    this._super(attributes);
                }
            });
            return new RubberConnection();*/
        }

        // Following policies are used to style any edit interactions in the canvas
        // Two possibilities to connect ports:
        // 1. With drag&drop (with resize of suitable target connections) or
        // 2. click on start and end position (with waves around start port, see draw2d.js code ripple)
        //
        // 1. Bind connection to the canvas (drag & drop):
        let connection = new draw2d.policy.connection.DragConnectionCreatePolicy({
            createConnection: connector_function
            // onMouseDown: vfw_drag  // change the original drag behaviour
        })
        // 2. Bind connection to the canvas (click on start and end port):
    /*    let connection = new draw2d.policy.connection.ClickConnectionCreatePolicy({
            createConnection: connector_function
        })*/
        return connection
    }
}


// define drag and drop interaction from outside to canvas to the draw2d canvas
function onclick_handler(ev) {
}

function vfw_drag() {

}


let canvas = new draw2d.Canvas('dropdiv');

// Define policies to style any edit interactions in the canvas
let connection = new Connection()
canvas.installEditPolicy(connection.connectionPolicy);


function process_drop_params(service, id) {
    // TODO: improve data object to avoid building this obj manually!
    let box_param = ''
    let inputs = []
    let outputs = []
    get_sessionStorage_tools(service)
    let metadata = JSON.parse(sessionStorage.getItem("tools"))[service][id]
    if (!metadata) {
        get_wpsprocess(service, id);
        metadata = JSON.parse(sessionStorage.getItem("tools"))[service][id]
    }
    if (metadata.dataInputs) {
        for (let i of metadata.dataInputs) {
            if ('keywords' in i) {

                for (let j of i['keywords']) {
                    inputs.push(j)
                }
            } else {
                inputs.push(i.dataType)
            }
        }
    }
    if (metadata.processOutputs) {
        for (let i of metadata.processOutputs) {
            if (i.identifier !== 'error') {
                if ('keywords' in i) {
                for (let j in i.keywords) {
                    outputs.push(j)
                }
            } else {
                outputs.push(i.dataType)
            }
            }
        }
    }
    box_param = {
        inputs: inputs,
        name: metadata.title,
        orgid: metadata.identifier,
        outputs: outputs,
        type: 'tool'
    }
    return box_param;
}


function update_workflow(event) {
    let workflow = get_sessionStorage_workflow()
    let workflow_name = document.getElementById('workflow_name')
    console.log('workflow name: ', workflow_name)
    if (event.state === 'remove') {
        delete workflow[event.id]
    // } else if (event.state == 'drop' && event.element._boxtype == 'tool') {
    } else if (event.state === 'drop') {
        workflow[event.element.box.id] = {
            name: event.element._name,
            orgid: event.element._orgid,
            boxtype: event.element._boxtype,
            inputs: event.element._inputs,
            outputs: event.element._outputs,
            source: event.element._sessionstore,
            service: event.element._service
        }
    }
    sessionStorage.setItem('workflow', JSON.stringify(workflow))
    // workflow[box.id] = box
}

/**
 * Used when an element is dropped in the dropzone. Collects parameters to build box.
 * @listens event:DragEvent
 * @param {Object} ev Start of the drag event outside of the canvas, set by dragstart_handler
 * @param {integer} x
 * @param {integer} y
 * @param {integer} id
 * @param {string} source which sesseionstore
 * @param {string} service
 * @return {dict} {box, boxID} - box object and global ID of box dropped on workarea
 */
function drop_handler(ev, x, y, id, source, service) {
    let box_param = ''
    let receivedData;

    try {
        ev.preventDefault();  // needed for Firefox
        receivedData = JSON.parse(ev.dataTransfer.getData("text/html"))
        x = ev.layerX;
        y = ev.layerY;
        id = receivedData[0]  // process name
        source = receivedData[1]
        service = receivedData[2]
    } catch {
        console.log('catch ev: ', ev)
    }
    if (source === 'workspace') {
        let metadata = JSON.parse(sessionStorage.getItem("dataBtn"))[id.substring(7)]
        service = 'dataBtn'
        console.log('metadata: ', metadata)
        // TODO: improve data object to avoid building this obj manually!
        box_param = {
            inputs: [],
            name: metadata.name + ' - ' + metadata.dbID,
            orgid: metadata.orgID,
            outputs: [metadata.outputs],
            type: 'data'
        }
    } else if (source === 'toolbar') {
        box_param = process_drop_params(service, id)
    } else if (source === 'workspace_results') {
        box_param = JSON.parse(sessionStorage.getItem("resultBtn"))[id]['dropBtn']
    }

    let boxID = box_param.orgid + get_workflow_id_affix()
    // console.log('box_param.name: ', box_param.name)
    let box = new Box(
        box_param.name, box_param.orgid, box_param.type,
        box_param.inputs, box_param.outputs, source, service, boxID
    )

    canvas.add(box.box, x, y);
    update_workflow({'state': 'drop', 'element': box});
    // reduce_lap(x, y)
    return {'box': box.box, 'boxID': boxID};
}

/**
 * Check for a tools in sessionStorage. When tools or service does not exist this function creates it.
 * @param {string} service
 * @return {obj} json - object of a wps process as saved in sessionStorage
 */
function get_sessionStorage_tools(service) {
    let tools = JSON.parse(sessionStorage.getItem('tools'))
    if (!tools) {
        tools = {}
    }
    if (!tools[service]) {
        tools[service] = {}
    }
    sessionStorage.setItem('tools', JSON.stringify(tools))
    return tools
}


/**
 * Check for a Workflow in sessionStorage. When no Workflow exists this function creates it.
 * @return {obj} json - object of a Workflow
 */
function get_sessionStorage_workflow() {
    let workflow = JSON.parse(sessionStorage.getItem('workflow'))
    if (!workflow) {
        workflow = set_sessionStorage_workflow_name()
        sessionStorage.setItem('workflow', JSON.stringify(workflow))
    }
    return workflow
}


/**
 * Check for a Workflow in sessionStorage. When no Workflow exists this function creates it.
 * @return {obj} json - object of a Workflow
 */
function set_sessionStorage_workflow_name(name = 'my workflow') {
    let workflow = JSON.parse(sessionStorage.getItem('workflow'))
    if (!workflow) {
        workflow = {'name': name}
    } else {
        workflow['name'] = name;
    }
    sessionStorage.setItem('workflow', JSON.stringify(workflow))
    return workflow
}


/**
 * Get a number to create a unique id for workflow elements. Counts plus one with each call.
 * @return {string} number
 */
function get_workflow_id_affix() {
    let affix = JSON.parse(sessionStorage.getItem('workflowIdAffix'))
    if (!affix) {
        affix = 1;
    } else {
        affix += 1;
    }
    sessionStorage.setItem('workflowIdAffix', JSON.stringify(affix))
    return "_box" + affix.toString()
}

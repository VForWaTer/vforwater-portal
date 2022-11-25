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
        return this.#createBox();
    }

    /**
     * Private function to create a box. Called from get box()
     * @private
     * @return {draw2d.shape} A box with ports to be placed on a draw2d.canvas.
     */
    #createBox() {
        // create a blank box with name and class TODO: and ID
        let box = this.#blankBox()

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
            this.#createOutPort(box, this._outputs[i], 100 - (parseInt(i) + 1) * outPortDist, relOutPort_y, i)
        }
        for (let i in this._inputs) {
            if (this._connectable_types.includes(this._inputs[i])) {
                relInPort_y = 0
            } else {
                relInPort_y = 3
            }
            this.#createInPort(box, this._inputs[i], (parseInt(i) + 1) * inPortDist, relInPort_y, i)
        }
        return box
    }

    /**
     * Create a simple box. Height of the box is defined through the type of the box.
     * @private
     * @return {draw2d.shape} A blank box without any ports to be extended or placed on a draw2d.canvas.
     */
    #blankBox() {
        let boxHeight = 30;
        let boxTexty = 3;
        let boxType = this._boxtype;
        let name = this._orgid;
        let service = this._service;

        if (boxType === 'tool') {
            boxHeight = 50;
            boxTexty = 12;
        }

        let box = new vfw.draw2d.Rectangle({
            minWidth: 100,
            width: this._boxwidth * 1.1,
            height: boxHeight,
            radius: 5,
            bgColor: '#D9EFFD',
            stroke: 0,
            cssClass: 'box-' + this._boxtype,
        })
        box.setId(this._boxid);
        let label = new draw2d.shape.basic.Label({
            text: this._boxname,
            stroke: 0,
            fontSize: 15,
            x: 5,  // Position of text in box
            y: boxTexty
        })
        if (boxType === 'tool') {
            box.on('click', function (ev) {
                vfw.workspace.modal.open_wpsprocess(service, name, box.getId());
                document.getElementById("workflowID").value = JSON.stringify({'id': box.getId(), 'service': service});
            })
            label.on('click', function (ev) {
                vfw.workspace.modal.open_wpsprocess(service, name, box.getId());
                document.getElementById("workflowID").value = JSON.stringify({'id': box.getId(), 'service': service});
            })
        }
        box.on('removed', function (ev) {
            vfw.workspace.workflow.update({'state': 'remove', 'id': ev.id})
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
    #createOutPort(blankbox, porttype, relPortx, relPorty, portNum) {
        let port = blankbox.createPort(
            'output',
            new draw2d.layout.locator.XYRelPortLocator(relPortx, relPorty),  // Position in % of box 0,0 is upper left
        );
        port.setCssClass(porttype)

        port.on('click', function () {
            vfw.workspace.modal.open_port(port.userData.service, port.userData.orgid,
                port.userData.boxid, port.userData.index, port.cssClass, 'output');
        })
        port.setConnectionDirection(2)
        port.setValue(this._orgid)
        port.setUserData({'service': this._service, 'boxid': this._boxid, 'orgid': this._orgid, 'index': portNum})
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
    #createInPort(blankbox, porttype, relPortx, relPorty, portNum) {
        let port;
        port = blankbox.createPort(
            'input',
            new draw2d.layout.locator.XYRelPortLocator(relPortx, relPorty),
        );

        port.setCssClass(porttype)
        port.on('click', function () {
        })
        port.on("connect", function (emitterPort, connection) {
            if (connection.port.getCssClass() === connection.connection.sourcePort.getCssClass()) {
                let source = {
                    'datatype': connection.connection.sourcePort.getCssClass(),
                    'service': connection.connection.sourcePort.getUserData()['service'],
                    'boxid': connection.connection.sourcePort.getUserData()['boxid'],
                    'orgid': connection.connection.sourcePort.getUserData()['orgid'],
                    'index': parseInt(connection.connection.sourcePort.getUserData()['index']),
                    'name': connection.connection.sourcePort.getValue(),
                };
                let target = {
                    'datatype': connection.port.getCssClass(),
                    'service': connection.port.getUserData()['service'],
                    'boxid': connection.port.getUserData()['boxid'],
                    'orgid': connection.port.getUserData()['orgid'],
                    'index': parseInt(portNum),
                };
                vfw.workspace.workflow.update({'state': 'change', 'source': source, 'target': target});
            } else {
                console.log("TODO: This shouldn't be connectable. Fix!")
            }
        });
        port.setConnectionDirection(0)
        port.setValue(this._orgid)
        port.setUserData({'service': this._service, 'boxid': this._boxid, 'orgid': this._orgid, 'index': portNum})
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
        return this.#createConnection();
    }

    /**
     * Actual (private) function to define the connection policy (the style of the connection between ports).
     * Called from get connectionPolicy.
     * @private
     * @return {draw2d.policy.connection.ConnectionCreatePolicy} The actual connection used on a draw2d.canvas.
     */
    #createConnection() {
        let connector_function = function () {
            // To options to connect ports. A) spline, B) rubber band
            // A) Define a spline to connect ports
            let SplineCon = new draw2d.Connection();
            SplineCon.on("added", function (connection, obj) {
                vfw.session.draw2d.setdata()
            })
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

/**
 * @method
 * Constructor for a draw2d.shape.basic.Rectangle, but extended with a serializer for the label and ports position.
 * Used from writer.marshal.
 *
 * @returns {Object}
 */
vfw.draw2d.Rectangle = draw2d.shape.basic.Rectangle.extend({
    NAME: "vfw.draw2d.Rectangle",
    /**
     * @method
     * Return an objects with all important attributes for XML or JSON serialization
     *
     * @returns {Object}
     */
    getPersistentAttributes: function () {
        var memento = this._super();

        // add all decorations to the memento
        memento.labels = [];
        this.children.each(function (i, e) {
            var labelJSON = e.figure.getPersistentAttributes();
            labelJSON.locator = e.locator.NAME;
            memento.labels.push(labelJSON);
        });

        this.inputPorts.data.forEach(function (e, i) {
            memento.ports[i].locatorAttr["x"] = e.locator.x;
            memento.ports[i].locatorAttr["y"] = e.locator.y;
        })
        var inputportlen = this.inputPorts.data.length;
        this.outputPorts.data.forEach(function (e, i) {
            memento.ports[inputportlen + i].locatorAttr["x"] = e.locator.x;
            memento.ports[inputportlen + i].locatorAttr["y"] = e.locator.y;
        })

        return memento;
    },

    /**
     * @method
     * Read all attributes from the serialized properties and transfer them into the shape.
     *
     * @param {Object} memento
     * @returns
     */
    setPersistentAttributes: function (memento) {
        this._super(memento);

        // remove all decorations created in the constructor of this element
        this.resetChildren();

        // and add all children of the JSON document.
        $.each(memento.labels, $.proxy(function (i, json) {
            // create the figure stored in the JSON
            var figure = eval("new " + json.type + "()");

            // apply all attributes
            figure.attr(json);

            // instantiate the locator
            var locator = eval("new " + json.locator + "()");

            // add the new figure as child to this figure
            this.add(figure, locator);
        }, this));
    }
});

vfw.session.draw2d = {
    setdata: function () {
        let writer = new draw2d.io.json.Writer();

        writer.marshal(canvas, function (json) {
            // convert the json object into string representation
            console.log('json writer: ', json)
            let jsonTxt = JSON.stringify(json, null, 2);
            sessionStorage.setItem("draw2ddata", jsonTxt)

        });
    },

    getworkflow: function () {
        return sessionStorage.getItem("draw2ddata")
    },

}

// define drag and drop interaction from outside to canvas to the draw2d canvas
function onclick_handler(ev) {
}

function vfw_drag() {

}

const canvas = new draw2d.Canvas('dropdiv');

// Define policies to style any edit interactions in the canvas
connection = new Connection();
canvas.installEditPolicy(connection.connectionPolicy);


/**
 * Collect metadata of element needed to draw a box.
 * @param service
 * @param id
 * @returns {{outputs: *[], inputs: *[], name, type: string, orgid: string}}
 */
vfw.workspace.workflow.process_drop_params = function (service, id) {
    // TODO: improve data object to avoid building this obj manually!
    let box_param = '';
    let inputs = [];
    let input_key_list = [];
    let output_key_list = [];
    let outputs = [];
    let metadata = vfw.session.get_wpsprocess(service, id);

    if (metadata.hasOwnProperty('dataInputs')) {
        for (let i of metadata.dataInputs) {
            if ('keywords' in i) {

                for (let j of i['keywords']) {
                    inputs.push(j)
                }
            } else {
                inputs.push(i.dataType)
            }
            input_key_list.push(i.identifier)
        }
    }
    if (metadata.hasOwnProperty('processOutputs')) {
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
            output_key_list.push(i.identifier)
        }
    }
    box_param = {
        inputs: inputs,
        input_ids: [],
        input_values: [],
        name: metadata.title,
        input_key_list: input_key_list,
        orgid: metadata.identifier,
        outputs: outputs,
        type: 'tool'
    }
    return box_param;
}


/**
 * Remove elements from sessionStorage or add new elements according to the event on the Dropzone ('dropdiv')
 * @param event
 */
vfw.workspace.workflow.update = function (event) {
    console.log('update workflow event: ', event)
    let delete_element, index, chained_id;
    let workflow = vfw.session.get_workflow();
    if (event.state === 'remove') {
        delete_element = workflow[event.id];
        if (delete_element.input_ids) {
            for (let i in delete_element.input_ids) {
                chained_id = delete_element.input_ids[i];
                if (workflow[chained_id]) {
                    index = workflow[chained_id].output_ids.indexOf(event.id);
                    workflow[chained_id].output_ids[index] = '';
                    workflow[chained_id].output_values[index] = '';
                }
            }
        }
        if (delete_element.output_ids) {
            for (let o in delete_element.output_ids) {
                chained_id = delete_element.output_ids[o];
                if (workflow[chained_id]) {
                    index = workflow[chained_id].input_ids.indexOf(event.id);
                    workflow[chained_id].input_ids[index] = '';
                    workflow[chained_id].input_values[index] = '';
                }
            }
        }
        delete workflow[event.id]
    } else if (event.state === 'drop') {
        workflow[event.element.box.id] = {
            name: event.element._boxname,
            orgid: event.element._orgid,
            boxtype: event.element._boxtype,
            inputs: event.element._inputs,
            input_values: event.params.input_values,
            input_keys: event.params.input_key_list,
            input_ids: event.params.input_ids,
            input_boxes: [],
            outputs: event.element._outputs,
            output_values: event.params.output_values,
            output_keys: event.params.output_key_list,
            output_ids: event.params.output_ids,
            output_boxes: [],
            source: event.element._sessionstore,
            service: event.element._service,
        }
    } else if (event.state === 'change') {
        if (event.hasOwnProperty('target')) {
            workflow[event.target.boxid]['input_values'] = []
            let newinsert = vfw.var.array.insert(workflow[event.target.boxid]['input_ids'],
                event.target.index, event.source.boxid)
            workflow[event.target.boxid]['input_ids'] = vfw.var.array.insert(workflow[event.target.boxid]['input_ids'],
                event.target.index, event.source.boxid)
        }
        if (event.hasOwnProperty('source')) {
            workflow[event.source.boxid]['output_values'] = []
            workflow[event.source.boxid]['output_ids'] = vfw.var.array.insert(workflow[event.source.boxid]['output_ids'],
                event.source.index, event.target.boxid)
        } else if (event.hasOwnProperty('source')) {
            console.log('else if has to be impplemented here')
        }
        workflow[event.target.boxid]['input_values'][event.target.index] = event.source.orgid;
        workflow[event.target.boxid]['input_ids'][event.target.index] = event.source.boxid;
        workflow[event.source.boxid]['output_values'][event.source.index] = event.target.orgid;
        workflow[event.source.boxid]['output_ids'][event.source.index] = event.target.boxid;

    }
    sessionStorage.setItem('workflow', JSON.stringify(workflow))
    vfw.session.draw2d.setdata()
}

/**
 * General function to insert a string in an array of strings.
 *
 * @param {array} arr - array of string
 * @param {integer} index - position to change an item
 * @param {string} newItem - the new item for index position
 */
vfw.var.array.insert = function (arr, index, newItem) {
    if (!arr) {
        arr = [...Array(index)].map(i => '')
    } else if (arr.length < (index - 1)) {
        arr = arr.concat([...Array(index - arr.length - 1)].map(i => ''));
    }
    arr.splice(index, 1, newItem)
    return arr;
}

/**
 * Add values to input_ids and input_values of box parameters used in SessionStorage and to create box.
 * @param {Object} ev
 * @param {string} id
 * @param {string} source
 * @param {string} service
 */
vfw.draw2d.box_params = function (ev, id, source, service = "") {
    let box_param = '';
    if (source === 'workspace') {
        let metadata = JSON.parse(sessionStorage.getItem("dataBtn"))[id.substring(7)]
        service = 'dataBtn'
        // TODO: improve data object to avoid building this obj manually!
        box_param = {
            inputs: [],
            name: metadata.name + ' - ' + metadata.dbID,
            orgid: metadata.orgID,
            outputs: [metadata.outputs],
            type: 'data'
        }
    } else if (source === 'toolbar') {
        box_param = vfw.workspace.workflow.process_drop_params(service, id)
        try {
            box_param['input_ids'] = ev.inId_list;
            box_param['input_values'] = ev.value_list;
        } catch {
            box_param['input_ids'] = [];
            box_param['input_values'] = [];
        }
    } else if (source === 'workspace_results') {
        box_param = JSON.parse(sessionStorage.getItem("resultBtn"))[id]['dropBtn']
    }
    return {'params': box_param, 'service': service};
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
vfw.workspace.drop_handler = function (ev, x, y, id, source, service) {
    let box_param = '';
    let receivedData, prepared_params, newBox;

    try {
        ev.preventDefault();  // needed for Firefox
        receivedData = JSON.parse(ev.dataTransfer.getData("text/html"))
        x = ev.layerX;
        y = ev.layerY;
        id = receivedData[0]  // process name
        source = receivedData[1]
        service = receivedData[2]
    } catch {
        console.log('0 catch ev: ', ev)
    }
    prepared_params = vfw.draw2d.box_params(ev, id, source, service);
    box_param = prepared_params.params;
    service = prepared_params.service;

    let boxID = box_param.orgid + vfw.workspace.workflow.get_workflow_id_affix()
    let box = new Box(
        box_param.name, box_param.orgid, box_param.type,
        box_param.inputs, box_param.outputs, source, service, boxID
    )
    newBox = box.box;
    canvas.add(newBox, x, y);

    vfw.workspace.workflow.update({'state': 'drop', 'element': box, 'params': box_param});
    return {'box': newBox, 'boxID': boxID};
}


/**
 * Check for a tools in sessionStorage. When tools or service does not exist this function creates it.
 * @param {string} service
 * @return {obj} json - object of a wps process as saved in sessionStorage
 */
vfw.session.get_tools = function (service) {
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
vfw.session.get_workflow = function () {
    let workflow = JSON.parse(sessionStorage.getItem('workflow'))
    if (!workflow) {
        workflow = vfw.session.set_workflow_name()
        sessionStorage.setItem('workflow', JSON.stringify(workflow))
    }
    return workflow
}


/**
 * Check for a Workflow in sessionStorage. When no Workflow exists this function creates it.
 * @return {obj} json - object of a Workflow
 */
vfw.session.set_workflow_name = function (name = 'my workflow') {
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
vfw.workspace.workflow.get_workflow_id_affix = function () {
    let affix = JSON.parse(sessionStorage.getItem('workflowIdAffix'))
    if (!affix) {
        affix = 1;
    } else {
        affix += 1;
    }
    sessionStorage.setItem('workflowIdAffix', JSON.stringify(affix))
    return "_box" + affix.toString()
}


/**
 * Collect information from session Storage and draw workflow boxes as given there.
 */
vfw.workspace.workflow.draw_workflow = function () {
    let jsonDocument = vfw.session.draw2d.getworkflow()
    if (jsonDocument) {
        let reader = new draw2d.io.json.Reader();
        reader.unmarshal(canvas, JSON.parse(jsonDocument));
    }
}

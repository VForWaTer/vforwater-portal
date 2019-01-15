import base64
import os
import re
import requests
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from heron.settings import wps_log, BASE_DIR
from io import StringIO, BytesIO
from lxml import etree

import wps_workflow.utils as utils_module
from wps_workflow.models import WPS, Task, InputOutput, Artefact, Process, STATUS, Workflow, Edge, DataEdge, SqlData
from wps_workflow.utils import ns_map, wps_em, ows_em


def scheduler():
    """
    Main scheduling function. Schedules Tasks in Workflows according to their execution order, generates execution XML files and sends tasks to
    their server for execution
    @return: None
    @rtype: NoneType
    """

    # TODO: set to changeable by settings & config file
    wps_log.debug("starting schedule")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    xml_dir = os.path.join(dir_path, 'testfiles/')

    exec_list = []

    for current_workflow in Workflow.objects.all():
        all_tasks = Task.objects.filter(workflow = current_workflow, status = '1')
        wps_log.debug(
                f"found {len(all_tasks)} tasks in workflow{current_workflow.id}")
        for current_task in all_tasks:
            previous_tasks_failed = False
            previous_tasks_finished = True
            edges_to_current_task = Edge.objects.filter(to_task = current_task)
            wps_log.debug(
                    f"found {len(edges_to_current_task)} edges to task{current_task.id} in workflow{current_workflow.id}")
            for current_edge in edges_to_current_task:
                if current_edge.from_task.status == '4':
                    wps_log.debug(
                            f"task{current_task.id}'s prior task{current_edge.from_task.id} is finished")
                    if not Artefact.objects.filter(task = current_task, role = '0'):
                        wps_log.warning(f"something is wrong here, task{current_task.id} has no artefacts,"
                                        f"but there should at least be input artefacts")
                        previous_tasks_finished = False
                        break
                    else:
                        for current_artefact in Artefact.objects.filter(task = current_task, role = '0'):
                            wps_log.debug(
                                    f"checking data of artefact{current_artefact.id} of task{current_task.id}")
                            if not current_artefact.data:
                                wps_log.warning(
                                        f"task{current_task.id} has artefact{current_artefact.id} which has no data")
                                previous_tasks_finished = False
                                break
                else:
                    wps_log.debug(
                            f"task{current_task.id}s prior task{current_edge.from_task.id} is not finished")
                    previous_tasks_finished = False
                    if current_edge.from_task.status == '5':
                        wps_log.debug(f"task{current_task.id}'s prior task{current_edge.from_task.id} has failed")
                        previous_tasks_failed = True
                    break
            if previous_tasks_failed:
                current_task.status = '5'
                current_task.save()
            elif previous_tasks_finished:
                wps_log.debug(
                        f"previous task is finished, scheduling now following task{current_task.id}")
                current_task.status = '2'
                exec_list.append(current_task.id)
                current_task.save()

    # generate execute xmls for all tasks with status waiting
    xml_generator(xml_dir)

    wps_log.debug(f"xmls generated for tasks: {exec_list}")

    # send tasks
    for tid in exec_list:
        wps_log.debug(f"sending execution request to server for task{tid}")
        send_task(tid, xml_dir)

        # sys.stdout = orig_stdout
        # f.close()


def xml_generator(xml_dir):
    """
    Traverses Database and generates execution XML files for every Task set to status WAITING
    @param xml_dir: Directory where XMLs are generated in
    @type xml_dir: string
    @return: None
    @rtype: NoneType
    """
    wps_log.debug("starting xml generator")
    try:
        task_list = list(Task.objects.filter(status = '2'))
    except Task.DoesNotExist:
        wps_log.debug("no running tasks found")
        task_list = []
    wps_log.debug(f"scheduled tasks: {[task.id for task in task_list]}")
    for task in task_list:
        try:
            process = task.process
        except Process.DoesNotExist:
            # process not found
            wps_log.warning(f"process of task{task.id} not found")
            return
        root = wps_em.Execute(ows_em.Identifier(process.identifier))
        root.set('service', 'WPS')
        root.set('version', '1.0.0')
        inputs_tree = create_data_doc(task)
        if inputs_tree == 1:
            # error code, something wrong with task TODO: check for better handling?
            wps_log.warning(f"Error: missing input artefact for task{task.id}")
            continue
        root.append(inputs_tree)

        wps_log.debug(
                f"successfully inserted inputs to xml document for task{task.id}")

        response_doc = wps_em.ResponseDocument()
        response_doc.set('storeExecuteResponse', 'true')
        response_doc.set('lineage', 'true')
        response_doc.set('status', 'true')

        output_list = list(InputOutput.objects.filter(
                process = task.process, role = '1'))
        wps_log.debug(
                f"list of outputs of task{task.id}: {[output.id for output in output_list]}")
        for output in output_list:
            response_doc.append(wps_em.Output(ows_em.Identifier(output.identifier), ows_em.Title(output.title),
                                              {'asReference': 'true'}))

        root.append(wps_em.ResponseForm(response_doc))

        wps_log.debug(f"successfully created xml for task{task.id}")
        # f":\n{etree.tostring(root, pretty_print=True).decode()}") # use to print xml to log

        # write to file, for testing let pretty_print=True for better readability
        # TODO: rework if file path problem is solved
        try:
            with open(f"{xml_dir}/task{task.id}.xml", 'w') as xml_file:
                xml_file.write(etree.tostring(root, pretty_print = True).decode())
            wps_log.debug(f"successfully written xml of task{task.id} to file, ready for sending to server")
        except:
            wps_log.warning(f"writing failed for task{task.id}")


def create_data_doc(task):
    """
    Creates subtree for execute request for model.Task task.
    @param task: the task for which the data subtree is created
    @type task: models.Task
    @return: subtree on success, error code 1 otherwise
    @rtype: lxml.etree._Element/int
    """
    # returns [] if no match found
    wps_log.debug(f"creating data subtree for task{task.id}")
    inputs = list(InputOutput.objects.filter(process = task.process, role = '0'))
    data_inputs = wps_em.DataInputs()
    wps_log.debug(f"found inputs: {[input.id for input in data_inputs]}")
    for input in inputs:
        # try to get artefact from db
        try:  # do DataEdge detection here
            artefact = Artefact.objects.get(task = task, parameter = input)
        except:
            # if no artefact is found, search DataEdges
            # if DataEdge to task exists create artefact
            try:
                wps_log.debug(f"try to get dataedges")
                dataedges = list(DataEdge.objects.filter(to_task = task, task_input = input))
                wps_log.debug(f"got dataedges")
                for dataedge in dataedges:  # this should be only one element
                    wps_log.debug(f"edge id {dataedge.id}")
                    sqldata = SqlData.objects.get(id = dataedge.from_sqldata_id)
                    wps_log.debug(f"sqldata id {sqldata.id}")

                wps_log.debug(f"getting current time")
                time_now = datetime.now()
                wps_log.debug(f"current time is {time_now}")
                input_data = '' + str(sqldata.data)
                wps_log.debug(f"input data: {input_data}")
                wps_log.debug(f"try to create artefact")
                artefact = Artefact.objects.create(task = task, parameter = input, role = '0', format = 'plain', data = input_data, created_at = time_now, updated_at = time_now)
                artefact.save()
                wps_log.debug(f"created artefact..?")
            except:
                # something is wrong here if artefact has not been created yet
                # as execute documents for next execution are only started if previous task has finished
                # and when previous task has finished, the output data is automatically passed to next tasks input
                wps_log.warning(
                        f"Error: artefact for task{task.id}s input{input.id} has not been created yet")
                return 1

        # create identifier and title as they are used in any case
        identifier = ows_em.Identifier(input.identifier)
        title = ows_em.Title(input.title)

        # first check if it is a file path, as data with length over 490 chars will be stored in a file
        # if so insert file path in Reference node
        # TODO: must check if this equals correct url of own server matching to task
        if artefact.data == utils_module.get_file_path(task):
            wps_log.debug(
                    f"file path found in task{task.id}s artefact{artefact.id}s data, inserting as data")
            data_inputs.append(wps_em.Input(identifier, title, wps_em.Reference({"method": "GET"},
                                                                                {ns_map["href"]: utils_module.get_file_path(artefact)})))
            # go to loop header and continue
            continue

        wps_log.debug(
                f"no file path as data in task{task.id}s artefact{artefact.id}, so there must be data")
        # literal data case, there is either a url or real data in the LiteralData element
        # in this case just send the data
        if input.datatype == '0':
            wps_log.debug(f"literal data found for task{task.id}")
            literal_data = wps_em.LiteralData(artefact.data)
            # check for attributes
            if artefact.format != 'plain':
                literal_data.set('dataType', artefact.format)

            # just create subtree with identifier, title and data with nested literaldata containing the artefacts data
            data_inputs.append(wps_em.Input(
                    identifier, title, wps_em.Data(literal_data)))
        # complex data case, first try to parse xml, if successfully append to ComplexData element
        #                    second check if there is CDATA ??
        elif input.datatype == '1':
            wps_log.debug(f"complex data found for task{task.id}")
            # append format data as attributes to complex data element
            # TODO is this a comment out from PSE team or later? if later, explain why. Complex Data handling was tested, taking it out will break the program
            # TODO: delete if unneeded, uncommented complex data format handling - complicated stuff
            # check if there is cdata in format
            # if artefact.format.split(";")[0] == "CDATA":
            #     wps_log.debug(
            #         f"cdata found in task{task.id} inserting cdata nested in tags into data of artefact{artefact.id}")
            #     complex_data.append(f"<![CDATA[{artefact.data}]]")
            #     # put data nested in cdata tag in complex data element
            #     data_inputs.append(wps_em.Input(
            #         identifier, title, wps_em.Data(complex_data)))
            # else:
            # just append it as if it is in xml format, it can also be inserted as text, will then not be in
            # pretty_print format, but wps server doesn't care about that
            try:
                wps_log.debug(
                        f"just inserting complex data for task{task.id} of artefact{artefact.id} in xml")
                data_inputs.append(wps_em.Input(
                        identifier, title, wps_em.Data(wps_em.ComplexData(artefact.data))))
            except:
                wps_log.debug(
                        f"inserting CDATA for task{task.id} of artefact{artefact.id} in xml")
                data_inputs.append(wps_em.Input(
                        identifier, title, wps_em.Data(wps_em.ComplexData(etree.CDATA(base64.b64decode(artefact.data))))))
        # bounding box case there should just be lowercorner and uppercorner data
        elif input.datatype == '2':
            wps_log.debug(f"boundingbox data found for task{task.id}: {artefact.data}")
            lower_corner = ows_em.LowerCorner()
            upper_corner = ows_em.UpperCorner()
            data = artefact.data
            wps_log.debug(f"{len(data.split('LowerCorner')) == 2 and len(data.split('UpperCorner')) == 2}")
            if len(data.split("LowerCorner")) == 2 and len(data.split("UpperCorner")) == 2:
                bbox_corners = data.split(";")
                lower_corner_data = bbox_corners[1].lstrip('LowerCorner').split(' ')
                upper_corner_data = bbox_corners[0].lstrip('UpperCorner').split(' ')
                upper_corner = ows_em.UpperCorner(f"{upper_corner_data[0]} {upper_corner_data[1]}")
                lower_corner = ows_em.LowerCorner(f"{lower_corner_data[0]} {lower_corner_data[1]}")

            # quite strange, but this node is called BoundingBoxData for inputs, for outputs it's just BoundingBox
            # also for inputs it is used with wps namespace, for outputs the ows namespace is used
            bbox_elem = wps_em.Data(wps_em.BoundingBoxData(lower_corner, upper_corner, {'crs': 'EPSG:4326', 'dimensions': '2'}))

            # finally create subtree
            data_inputs.append(wps_em.Input(identifier, title, bbox_elem))

    wps_log.debug(f"finished input xml generation for task{task.id}")
    return data_inputs


def send_task(task_id, xml_dir):
    """
    Sends a Task identified by its Database ID to its WPS Server.
    @param task_id: ID of Task in Database
    @type task_id: int
    @param xml_dir: Directory where XMLs are stored in
    @type xml_dir: string
    @return: None
    @rtype: NoneType
    """
    filepath = str(xml_dir) + 'task' + str(task_id) + '.xml'
    if not os.path.isfile(filepath):
        wps_log.warning(f"file for task {task_id} does not exist, aborting...")
        return
    try:
        # This only is outsourced to extra function for better readability
        execute_url = get_execute_url(Task.objects.get(id = task_id))
    except Task.DoesNotExist:
        wps_log.warning("Error, execute url is empty, but is not allowed to. Aborting...")
        return

    # TODO: validate execution url
    file = '<?xml version="1.0" encoding="utf-8" standalone="yes"?>' + \
           str(open(filepath, 'r').read())

    # send to url
    try:
        response = requests.post(execute_url, data = file)
        # get response from send
        xml = ET.fromstring(response.text)

    except:
        task = Task.objects.get(id = task_id)
        task.status = '5'
        task.save()
        task_failed_handling(task, "status could not be read, check internet connection or server availability")
        wps_log.warning(f"request for task{task_id} could not be posted or returned something unexpected, aborting")
        return

    err_msg = ""

    # check for status node in xml
    if xml.find(ns_map['Status']) is not None:
        # if there is status node, search for process status
        if xml.find(ns_map['Status']).find(ns_map['ProcessAccepted']) is not None:
            status = '3'
        elif xml.find(ns_map['Status']).find(ns_map['ProcessStarted']) is not None:
            status = '3'
        elif xml.find(ns_map['Status']).find(ns_map['ProcessPaused']) is not None:
            status = '3'
        elif xml.find(ns_map['Status']).find(ns_map['ProcessSucceeded']) is not None:
            status = '4'
        elif xml.find(ns_map['Status']).find(ns_map['ProcessFailed']) is not None:
            status = '5'
            try:
                err_msg = xml.find(ns_map['Status']).find(ns_map['ProcessFailed']) \
                    .find(ns_map['ExceptionReport']).find(ns_map['Exception']).find(ns_map['ExceptionText']).text
            except:
                err_msg = "unknown error"
        else:
            status = '5'
            err_msg = 'unknown error'
    elif xml.find(ns_map['Exception']) is not None:
        status = '5'
        exception_elem = xml.find(ns_map['Exception']).find(ns_map['ExceptionText'])
        if exception_elem is None:
            err_msg = "unknown error"
        else:
            err_msg = exception_elem.text
    else:
        status = '5'
        err_msg = "unknown error"

    try:
        # Update DB Entry
        task = Task.objects.get(id = task_id)
    except Task.DoesNotExist:
        wps_log.warning(f"task{task_id} not found, aborting")
        return

    ## This part is done because the dev PyWPS Server does not deliver a correct url in status location field (hidden behind localhost)
    ## So here the correct url is built with the filename and server url from db
    ## does expect standard config of output folder
    # TODO switch in settings.py for status_url type or by comparing front of status url with execute url
    exec_part_url = get_execute_url(Task.objects.get(id = task_id))
    front_part_url = re.sub('\/wps\?request[^^]*', '', exec_part_url)

    status_url = xml.get('statusLocation')

    # TODO part_out and /demo part could be specified in settings file
    file_part_url = re.sub('\A[^^]*/outputs', '', status_url)
    part_out = '/outputs'
    if front_part_url == 'https://portal.vforwater.de':
        status_url = front_part_url + '/demo' + part_out + file_part_url  ## /demo needs to be included for demo wps server
    else:
        status_url = front_part_url + part_out + file_part_url

    if status_url is None:
        status = '5'
        status_url = "error_url"
        # else:
        # status_url = "http://" + re.sub(r"^http://", "", status_url)   # why do that?

    wps_log.info(f"STATUS URL: {status_url}")

    task.status_url = status_url

    task.status = status
    task.started_at = datetime.now()
    wps_log.debug(f"task{task_id} started at {task.started_at}")
    task.save()

    # Delete execution XML
    if os.path.isfile(filepath):
        os.remove(filepath)

    if task.status == '5':
        task_failed_handling(task, err_msg)


def get_execute_url(task):
    """
    Extracts the Execute URL from the Database for a given task. Returns empty string on error.
    @param task: Task object from Database
    @type task: Task
    @return: Execute URL. Empty on error or empty DB field
    @rtype: string
    """
    execute_url = ""

    try:
        process = task.process
        wps = process.wps
        execute_url = wps.execute_url
        wps_log.debug(f"execute url of task{task.id} is {wps.execute_url}")
    except Process.DoesNotExist or WPS.DoesNotExist:
        wps_log.warning(f"no execute url found for task{task.id}")
        execute_url = ""

    return execute_url


def receiver():
    """
    Loops all running tasks, then
    parses xml on server and checks for status.
    Overwrites status if changed and
    if task is finished, writes data to db
    @return: None
    @rtype: NoneType
    """
    wps_log.debug("starting receiver")
    running_tasks = list(Task.objects.filter(status = '3'))
    wps_log.debug(f"found {len(running_tasks)} running tasks: {running_tasks}")
    for task in running_tasks:
        parse_execute_response(task)


def parse_execute_response(task):
    """
    Checks parameter tasks status by checking xml file found at status_url for change
    If task has finished write data to db if there is any data
    @param task: the task whose status is currently checked
    @type task: subclass of models.Model
    @return: 0 on success, error code otherwise
    @rtype: int
    """

    # try to parse document which should be returned by request
    try:
        wps_log.debug(f"task{task.id}s url: {task.status_url}")
        root = etree.parse(StringIO(requests.get(task.status_url).text))
    except ValueError:
        '''
        might throw ValueError if CDATA is placed within document:
        ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
        in this case try to parse document by encoding and reading in BytesIO buffer bevore parsing
        '''
        root = etree.parse(
                BytesIO(requests.get(task.status_url).text.encode()))
    except:
        task.status = '5'
        task.save()
        task_failed_handling(task, "status could not be read, check internet connection or server availability")
        # otherwise just exit and return error code
        wps_log.debug(
                f"request of {task.status_url} for task {task.id} could not be parsed")
        return 1

    process_info = root.find(ns_map["Process"])
    try:
        output_list = root.find(
                ns_map["ProcessOutputs"]).findall(ns_map["Output"])
    except:
        # no Processes in output
        wps_log.warning(f"response xml for task{task.id} has no output nodes")
        output_list = []

    if process_info is None:
        wps_log.warning(f"Process information not found for task{task.id}")
        return 2

    for output in output_list:
        parse_output(output, task)

    try:
        process_status = root.find(ns_map["Status"])
        status_name = etree.QName(process_status[0].tag).localname
    except:
        wps_log.warning(f"no status found in xml for task{task.id}")
        return 2

    new_status = STATUS[3][0] if status_name in ["ProcessAccepted", "ProcessStarted", "ProcessPaused"] \
        else STATUS[4][0] if status_name == "ProcessSucceeded" else STATUS[5][0]

    if task.status != new_status:
        wps_log.debug(
                f"old status of task{task.id}: {task.status}, new status: {new_status}")
        task.status = new_status
        task.save()

    # if status failed, create error output artefacts for task
    if task.status == '5':
        wps_log.debug(
                f"task{task.id} failed, status link can be found here: {task.status_url}")
        try:
            err_msg = process_status[0].find(ns_map['ExceptionReport']).find(ns_map['Exception']).find(ns_map['ExceptionText']).text
            wps_log.debug("found failure information")
        except:
            wps_log.debug("could not find information about failure")
            err_msg = "unknown error"

        task_failed_handling(task, err_msg)
        return 3

    # update process of workflow after every response
    calculate_percent_done(task.workflow)

    return 0


def parse_output(output, task):
    """
    Parses output node of xml and inserts respective data if found and
    also updates status of task if there are any changes
    @param output the output that has to be parsed
    @type output lxmls.etree._Element
    @param task: the task that belongs to the output
    @type task: subclass of models.Model
    @return: None
    @rtype: NoneType
    """
    wps_log.debug(f"parsing output information for task{task.id}")
    out_id = output.find(ns_map["Identifier"]).text

    try:
        output_db = InputOutput.objects.get(
                process = task.process, identifier = out_id, role = '1')
        artefact = Artefact.objects.get(
                task = task, parameter = output_db, role = '1')
    except InputOutput.DoesNotExist:
        wps_log.warning(f"output for task{task.id} not found, aborting")
        return
    except:
        time_now = datetime.now()
        wps_log.debug(
                f"output artefact for task {task.id} not found, creating new artefact")
        artefact = Artefact.objects.create(task = task, parameter = output_db, role = '1',
                                           created_at = time_now, updated_at = time_now)

    # everything is the same up to here for each output type
    data_elem = output.find(ns_map["Data"])
    reference = output.find(ns_map["Reference"])
    time_now = datetime.now()

    if data_elem is not None:
        try:
            # there should always be just one element!
            data_elem = data_elem.getchildren()[0]
        except:
            wps_log.debug(f"data has no child for task{task.id}")
            # go back to next output
            return

        if data_elem.tag == ns_map["LiteralData"]:
            wps_log.debug(f"literal data found in data for output{output_db.id} of task{task.id}")
            parse_response_literaldata(artefact, data_elem)

        elif data_elem.tag == ns_map["BoundingBox"]:
            wps_log.debug(f"boundingbox data found in data for output{output_db.id} of task{task.id}")
            parse_response_bbox(artefact, data_elem)

        elif data_elem.tag == ns_map["ComplexData"]:
            wps_log.debug(f"complex data found in data for output{output_db.id} of task{task.id}")
            parse_response_complexdata(artefact, data_elem)
    elif reference is not None:
        # complexdata found, usually gets passed by url reference which won't be 500 chars long
        db_format = "plain" if data_elem.get("dataType") \
                               is None else data_elem.get("dataType").split(':')[-1]
        wps_log.debug("writing data to db")
        db_data = reference.text  # should be a url
        artefact.format = db_format
        artefact.data = db_data
        artefact.updated_at = time_now
        artefact.save()

    try:
        wps_log.debug(f"trying to get edge from task{task.id}, output{output_db.id}")
        edges = Edge.objects.filter(from_task = task, output = output_db)
    except Edge.DoesNotExist:
        wps_log.debug(f"edge does not exist")
        edges = []

    for edge in edges:
        if artefact.data is not None:
            try:
                to_artefact = Artefact.objects.get(
                        task = task, parameter = edge.input, role = '1')
                to_artefact.format = artefact.format
                to_artefact.data = artefact.data
                to_artefact.updated_at = time_now
                to_artefact.save()
            except Artefact.DoesNotExist:
                wps_log.debug("input artefact not found, creating new artefact")
                to_artefact = Artefact.objects.create(task = edge.to_task, parameter = edge.input, role = '0', format = artefact.format,
                                                      data = artefact.data, created_at = time_now, updated_at = time_now)
                wps_log.debug(f"artefact{to_artefact.id} has been created")


def parse_response_literaldata(artefact, data_elem):
    """
    Parses the xmls literaldata subtree and inserts data into artefact
    @param artefact: the artefact which the data is put into
    @type artefact: models.Artefact
    @param data_elem: the xml node element which holds the data
    @type data_elem: lxml.etree._Element
    @return: None
    @rtype: NoneType
    """
    time_now = datetime.now()
    db_format = "plain" if data_elem.get(
            "dataType") is None else data_elem.get("dataType").split(':')[-1]
    db_data = data_elem.text

    # if the string is less than 490 chars long write to db
    # otherwise write to file and write url to db
    if len(db_data) < 490:
        wps_log.debug("writing data to db")
        artefact.format = db_format
        artefact.data = db_data
        artefact.updated_at = time_now
        artefact.save()

    else:
        wps_log.debug("writing data to file")
        # TODO: rework if file path problem is solved!
        file_name = f"outputs/task{task.id}.xml"
        with open(file_name, 'w') as tmpfile:
            tmpfile.write(db_data)
        artefact.format = db_format
        artefact.data = f"{BASE_DIR}/{file_name}"
        artefact.updated_at = time_now
        artefact.save()


def parse_response_bbox(artefact, data_elem):
    """
    Parses the xmls boundingboxdata subtree and inserts data into artefact
    @param artefact: the artefact which the data is put into
    @type artefact: models.Artefact
    @param data_elem: the xml node element which holds the data
    @type data_elem: lxml.etree._Element
    @return: None
    @rtype: NoneType
    """
    time_now = datetime.now()
    lower_corner = data_elem.find(ns_map["LowerCorner"])
    upper_corner = data_elem.find(ns_map["UpperCorner"])
    db_format = "plain" if data_elem.get(
            "dataType") is None else data_elem.get("dataType").split(':')[-1]
    db_data = f"{lower_corner.text.split(' ')[0]},{lower_corner.text.split(' ')[1]}," \
              f"{upper_corner.text.split(' ')[0]},{upper_corner.text.split(' ')[1]}"
    wps_log.debug("writing data to db")
    artefact.format = db_format
    artefact.data = db_data
    artefact.updated_at = time_now
    artefact.save()


def parse_response_complexdata(artefact, data_elem):
    """
    Parses the xmls complexdata subtree and inserts data into artefact
    @param artefact: the artefact which the data is put into
    @type artefact: models.Artefact
    @param data_elem: the xml node element which holds the data
    @type data_elem: lxml.etree._Element
    @return: None
    @rtype: NoneType
    """
    time_now = datetime.now()
    # TODO: test!
    db_format = "plain" if data_elem.get(
            "dataType") is None else data_elem.get("dataType").split(':')[-1]
    db_data = data_elem.text
    artefact.format = db_format

    if "CDATA" in data_elem.text:
        wps_log.debug(
                f"cdata found in complex data for output{output_db.id} of task{task.id}!")
        # db_format = "CDATA;" + db_format

        # if the string is less than 490 chars long write to db
        # otherwise write to file and write url to db
        db_data = data_elem.text
        if len(db_data) < 490:
            artefact.data = db_data
            artefact.updated_at = time_now
            artefact.save()

        else:
            wps_log.debug("writing data to file")
            file_name = f"outputs/task{task.id}.xml"
            with open(file_name, 'w') as tmpfile:
                tmpfile.write(db_data)
            artefact.data = f"{BASE_DIR}/{file_name}"
            artefact.updated_at = time_now
            artefact.save()

    elif db_data is not None:
        # if the string is less than 490 chars long write to db
        # otherwise write to file and write url to db
        if len(db_data) < 490:
            wps_log.debug("writing data to db")
            artefact.data = db_data
            artefact.updated_at = time_now
            artefact.save()

        else:
            wps_log.debug("writing data to file")
            file_name = f"outputs/task{task.id}.xml"
            with open(file_name, 'w') as tmpfile:
                tmpfile.write(db_data)
            artefact.data = f"{BASE_DIR}/{file_name}"
            artefact.updated_at = time_now
            artefact.save()

    # if there is at least one other child, there seems to be a subtree
    elif len(data_elem.getchildren()) != 0:

        # read the subtree to string with pretty_print syntax
        db_data = etree.tostring(data_elem, pretty_print = True)

        # if the string is less than 490 chars long write to db
        # otherwise write to file and write url to db
        if len(db_data) < 490:
            wps_log.debug("writing data to db")
            artefact.data = db_data
            artefact.updated_at = time_now
            artefact.save()
        else:
            wps_log.debug("writing data to file")
            file_name = f"outputs/task{task.id}.xml"
            with open(file_name, 'w') as tmpfile:
                tmpfile.write(db_data)
            artefact.data = f"{BASE_DIR}/{file_name}"
            artefact.updated_at = time_now
            artefact.save()
    else:
        wps_log.debug(
                "no complex data found in complexdata tree element")


def calculate_percent_done(workflow):
    """
    Calculates the percentage of finished tasks in the workflow of task
    @param task: task with recently changed status
    @type task: Task
    @return: percentage of finished tasks in the workflow of task
    @rtype: int
    """
    err_tasks = list(Task.objects.filter(workflow = workflow, status = '5'))
    if len(err_tasks):
        wps_log.warning(f"workflow{workflow.id} execution has failed due to "
                        f"failure of tasks: {[task.id for task in err_tasks]}")
        percent_done = -1
        workflow.save()
    else:
        finished = list(Task.objects.filter(workflow = workflow, status = '4'))
        all_wf_tasks = list(Task.objects.filter(workflow = workflow))
        percent_done = int((len(finished) / len(all_wf_tasks)) * 100)
        wps_log.debug(
                f"updating progress of workflow{workflow.id} to {percent_done}%")

    workflow.percent_done = percent_done
    workflow.save()


def task_failed_handling(task, err_msg):
    """
    Is called if a task failed to create error Artefacts which signals
    the client that the task has failed
    @param task: the failed task
    @type task: models.Task
    @param err_msg: the error message
    @type err_msg: string
    @return: None
    @rtype: NoneType
    """
    wps_log.debug(f"task{task.id} failed, due to error: {err_msg}")
    wps_log.debug("error artefacts are created")

    time_now = datetime.now()
    process = task.process

    error_output_list = list(InputOutput.objects.filter(process = process, role = '1'))
    wps_log.debug(f"trying to generate {len(error_output_list)} error artefacts")
    for output in error_output_list:
        if len(list(Artefact.objects.filter(task = task, parameter = output, role = '1'))) == 0:
            Artefact.objects.create(task = task, parameter = output, role = '1', format = 'error', data = err_msg,
                                    created_at = time_now, updated_at = time_now)
        else:
            wps_log.warning(f"task{task.id} failed due to ProcessFailed status, but there are already artefacts, "
                            f"setting artefacts to error mode")
            Artefact.objects.filter(task = task, parameter = output, role = '1').update(format = 'error', data = err_msg,
                                                                                        updated_at = time_now)


def update_wps_processes():
    """
    This method update the list of WPS processes provided by the WPS Server.
    It takes a describe_processes_url of each wps server saved in database,
    open it, and parses the xml file, that comes in request message.

    It will be checked if any object present in database.
    If no, it will be saved, else it will be overwritten with the actual
    information provided by the WPS server.

    @return: None
    @rtype: NoneType
    """
    xml_namespaces = {
        'gml': 'http://www.opengis.net/gml',
        'xlink': 'http://www.w3.org/1999/xlink',
        'wps': 'http://www.opengis.net/wps/1.0.0',
        'ows': 'http://www.opengis.net/ows/1.1',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
        }

    wps_servers = WPS.objects.all()
    wps_log.debug("starting process update")
    for wps_server in wps_servers:
        wps_log.debug(f"checking WPS{wps_server.id}")
        describe_processes_url = wps_server.describe_url
        wps_log.debug(f"describe processes request sent to: {describe_processes_url}")

        temp_xml, headers = urllib.request.urlretrieve(describe_processes_url)

        tree = ET.parse(temp_xml)

        root = tree.getroot()
        process_elements = root.findall('ProcessDescription')
        wps_log.debug(
                f"found {len(process_elements)} processes on WPS{wps_server.id}")
        for process_element in process_elements:
            process = utils_module.parse_process_info(
                    process_element, xml_namespaces, wps_server)
            process_from_database = utils_module.search_process_in_database(
                    process)
            if process_from_database is None:
                process.save()
                wps_log.info(f"created new process: process{process.id}")
            else:
                process = utils_module.overwrite_process(
                        process_from_database, process)
            wps_log.debug(
                    f"found matching process in database: process{process.id}")

            # Save Inputs
            inputs_container_element = process_element.find('DataInputs')
            if inputs_container_element is not None:
                input_elements = inputs_container_element.findall('Input')

                for input_element in input_elements:
                    input = utils_module.parse_input_info(
                            input_element, xml_namespaces, process)
                    input_from_database = utils_module.search_input_output_in_database(
                            input)
                    if input_from_database is None:
                        input.save()
                        wps_log.info(f"created new input: input{input.id}")
                    else:
                        input = utils_module.overwrite_input_output(
                                input_from_database, input)
                        wps_log.debug(
                                f"found matching input in database: input{input.id}")

            # Save Outputs
            outputs_container_element = process_element.find('ProcessOutputs')
            if outputs_container_element is not None:
                output_elements = outputs_container_element.findall('Output')

                for output_element in output_elements:
                    output = utils_module.parse_output_info(
                            output_element, xml_namespaces, process)
                    output_from_database = utils_module.search_input_output_in_database(
                            output)
                    if output_from_database is None:
                        output.save()
                        wps_log.info(f"created new output: output{output.id}")
                    else:
                        output = utils_module.overwrite_input_output(
                                output_from_database, output)
                        wps_log.debug(
                                f"found matching output in database: output{output.id}")

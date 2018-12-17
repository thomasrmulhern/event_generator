import pandas as pd
from numpy.random import choice
from random import randint

patients = {
    "Patient_1": [],
    "Patient_2": [],
    "Patient_3": [],
    "Patient_4": [],
    "Patient_5": [],
    "Patient_6": [],
    "Patient_7": [],
    "Patient_8": [],
    "Patient_9": [],
    "Patient_10": [],
    "Patient_11": [],
    "Patient_12": [],
    "Patient_13": [],
    "Patient_14": [],
    "Patient_15": [],
    "Patient_16": [],
    "Patient_17": [],
    "Patient_18": [],
    "Patient_19": [],
    "Patient_20": [],
    "Patient_21": [],
    "Patient_22": [],
    "Patient_23": [],
    "Patient_24": [],
    "Patient_25": []
    }

clinicians = {
    "Clinician_1": [
        "Patient_1",
        "Patient_2",
        "Patient_3",
        "Patient_4",
        "Patient_5"],

    "Clinician_2": [
        "Patient_6",
        "Patient_7",
        "Patient_8",
        "Patient_9",
        "Patient_10"],

    "Clinician_3": [
        "Patient_11",
        "Patient_12",
        "Patient_13",
        "Patient_14",
        "Patient_15"],

    "Clinician_4": [
        "Patient_16",
        "Patient_17",
        "Patient_18",
        "Patient_19",
        "Patient_20"],

    "Clinician_5": [
        "Patient_21",
        "Patient_22",
        "Patient_23",
        "Patient_24",
        "Patient_25"]
}

import pandas as pd
from numpy.random import choice
from random import randint
from op_data_gen import create_timestamp


def goal_created(created):
    """
    Description: Create an event and unique object_id; add id to the "created"
    set and add the list to the dataframe.
    Input: list (for goals created)
    Return: list (of two items)
    Examples:
        >>> goal_created(created)
            ['GOAL_CREATED', 950152636]

        >>> goal_created(created)
            ['GOAL_CREATED', 148614186]

        >>> goal_created(created)
            ['GOAL_CREATED', 408622160]
    """

    object_id = randint(99999999,999999999)
    while object_id in created or object_id in completed or object_id in app_or_den:
        object_id = randint(99999999,999999999)
    created.append(object_id)
    row = ['GOAL_CREATED', object_id]
    #print(row)
    return row

def assign_goal(patients):
    """
    Description: Assign the most recently created goal to a patient and return the patient's name
    Input: dictionary (patients and their lists of goals created)
    Output: string (Patient's name)
    Examples:
    """

    p = choice(list(patients.keys()), 1)
    print(p)
    p = choice(list(patients.keys()), 1)
    patients[p].append(object_id)

    return p


def goal_completed(created, completed):
    """
    Description: Randomly select a goal from the "created" list and move it to
    the "completed" list.
    Input: list(for goals created, list for goals completed)
    Return: list (of two items)
    Examples:
        >>> goal_completed(created, completed)
            ['GOAL_COMPLETED', 148614186]

        >>> goal_completed(created, completed)
            ['GOAL_COMPLETED', 408622160]

        >>> goal_completed(created, completed)
            ['GOAL_COMPLETED', 950152636]
    """
    # Check to make sure the list isn't empty
    if len(created) != 0 and len(created) != None:
        object_id = choice(created, replace=False)
        completed.append(object_id)
        created.remove(object_id)
        row =  ['GOAL_COMPLETED', object_id]
        #print(row)
        return row
    else:
        pass

def approved_or_denied(completed, app_or_den):
    """
    Description: Randomly select object_id from the list of completed goals and
    approve or deny it. If it gets denied, send it back to the "completed" list
    to be recompleted and approved.
    Input: list (of completed goals, list of goals to be approved or denied)
    Return: list (of two items)
    Examples:
        >>> approved_or_denied(completed, app_or_den)
            ['GOAL_APPROVED', 408622160]

        >>> approved_or_denied(completed, app_or_den)
            ['GOAL_REJECTED', 950152636]

        >>> approved_or_denied(completed, app_or_den)
            ['GOAL_APPROVED', 148614186]
    """

    # check to make sure the list isn't empty
    if len(completed) > 0 and len(completed) != None:

        object_id = choice(completed, replace=False)
        app_or_den.append(object_id)
        completed.remove(object_id)

        # give the goals a higher probability of approval than rejection
        event = choice(['GOAL_APPROVED','GOAL_REJECTED'], p=[.7, .3])
        if event == 'GOAL_REJECTED':
            created.append(object_id)
            app_or_den.remove(object_id)
        row = [event, object_id]
        #print(row)
        return row

    else:
        pass

if __name__ == '__main__':

    # Instantiate the lists to hold data created in the functions
    df = []
    created = []
    completed = []
    app_or_den = []
    patient_list = []
    pats = []
    clins = []

    # Create some goals at the beginning in case the first event is
    # EVENT_COMPLETED or EVENT_APPROVED/ EVENT_REJECTED and causes a crash
    for _ in range(50):
        event, object_id = goal_created(created)
        patient = choice(list(patients.keys()), 1).item()
        patients[patient].append(object_id)
        for c in clinicians:
            if patient in clinicians[c]:
                clinician = c
        df.append([event, object_id, patient, clinician])



        #print(f"""patient: {patient}, patients[patient]: {patients[patient]}""")


    # Complete some goals at the beginning in case the first event is EVENT_APPROVED
    # or EVENT_REJECTED and causes a crash
    for _ in range(10):
        event, object_id = goal_completed(created, completed)
        for p in patients.keys():
            if object_id in patients[p]:
                patient = p
        for c in clins:
            if patient in clinicians[c]:
                clinician = c
        df.append([event, object_id, patient, clinician])

    # Create 10000 rows of data
    for _ in range(10000):

        # Putting function instances directly in the choice function ran each
        # function instead of choosing amongst them
        event = choice(['a','b','c'], 1, p=[0.40, 0.35, 0.25])
        if event == 'a':
            event, object_id = goal_created(created)
            patient = choice(list(patients.keys()), 1).item()
            patients[patient].append(object_id)
            for c in clins:
                if patient in clinicians[c]:
                    clinician = c
            df.append([event, object_id, patient, clinician])

        elif event == 'b':
            event, object_id = goal_completed(created, completed)
            for p in patients.keys():
                if object_id in patients[p]:
                    patient = p
            for c in clinicians:
                if patient in clinicians[c]:
                    clinician = c
            df.append([event, object_id, patient, clinician])

        elif event == 'c':
            event, object_id = approved_or_denied(completed, app_or_den)
            for p in patients.keys():
                    if object_id in patients[p]:
                        patient = p
                        for c in clinicians.keys():
                            if patient in clinicians[c]:
                                clinician = c
                        if event == 'GOAL_APPROVED':
                            patients[patient].remove(object_id)
            df.append([event, object_id, patient, clinician])



    # Convert the list of lists to a pandas dataframe and output a csv
    df = pd.DataFrame(df, columns=['Event', 'object_id', 'users', 'clinician'])
    start_date = 1452233440.404116
    timestamps = []
    for _ in df['object_id']:
        ts, seconds = create_timestamp(start_date)
        start_date = seconds
        timestamps.append(ts)
    df['timestamps'] = timestamps
    print(df)
    df.to_csv('/Users/thomasmulhern/Desktop/test1.csv', index=False)
    #path = input("csv file path:")
    #df.to_csv(path)





# def goal_created(created):
#     """
#     Description: Create an event and unique object_id; add id to the "created"
#     set and add the list to the dataframe.
#     Input: list for goals created
#     Return: list of two items
#     Examples:
#         >>> goal_created(created)
#             ['GOAL_CREATED', 950152636]
#
#         >>> goal_created(created)
#             ['GOAL_CREATED', 148614186]
#
#         >>> goal_created(created)
#             ['GOAL_CREATED', 408622160]
#     """
#
#     object_id = randint(99999999,999999999)
#     while object_id in created or object_id in completed or object_id in app_or_den:
#         object_id = randint(99999999,999999999)
#     created.append(object_id)
#     row = ['GOAL_CREATED', object_id]
#     print(row)
#     return row
#
# def goal_completed(created, completed):
#     """
#     Description: Randomly select a goal from the "created" list and move it to
#     the "completed" list.
#     Input: list for goals created, list for goals completed
#     Return: list of two items
#     Examples:
#         >>> goal_completed(created, completed)
#             ['GOAL_COMPLETED', 148614186]
#
#         >>> goal_completed(created, completed)
#             ['GOAL_COMPLETED', 408622160]
#
#         >>> goal_completed(created, completed)
#             ['GOAL_COMPLETED', 950152636]
#     """
#     # Check to make sure the list isn't empty
#     if len(created) != 0 and len(created) != None:
#         object_id = choice(created, replace=False)
#         completed.append(object_id)
#         created.remove(object_id)
#         row =  ['GOAL_COMPLETED', object_id]
#         print(row)
#         return row
#     else:
#         pass
#
# def approved_or_denied(completed, app_or_den):
#     """
#     Description: Randomly select object_id from the list of completed goals and
#     approve or deny it. If it gets denied, send it back to the "completed" list
#     to be recompleted and approved.
#     Input: list of completed goals, list of goals to be approved or denied
#     Return: list of two items
#     Examples:
#         >>> approved_or_denied(completed, app_or_den)
#             ['GOAL_APPROVED', 408622160]
#
#         >>> approved_or_denied(completed, app_or_den)
#             ['GOAL_REJECTED', 950152636]
#
#         >>> approved_or_denied(completed, app_or_den)
#             ['GOAL_APPROVED', 148614186]
#     """
#
#     # check to make sure the list isn't empty
#     if len(completed) > 0 and len(completed) != None:
#
#         object_id = choice(completed, replace=False)
#         app_or_den.append(object_id)
#         completed.remove(object_id)
#
#         # give the goals a higher probability of approval than rejection
#         event = choice(['GOAL_APPROVED','GOAL_REJECTED'], p=[.7, .3])
#         if event == 'GOAL_REJECTED':
#             created.append(object_id)
#             app_or_den.remove(object_id)
#         row = [event, object_id]
#         print(row)
#         return row
#
#     else:
#         pass
#
# if __name__ == '__main__':
#
#     # Instantiate the lists to hold data created in the functions
#     df = []
#     created = []
#     completed = []
#     app_or_den = []
#
#     # Create some goals at the beginning in case the first event is
#     # EVENT_COMPLETED or EVENT_APPROVED/ EVENT_REJECTED and causes a crash
#     for _ in range(50):
#         event, object_id = goal_created(created)
#         df.append([event, object_id])
#
#     # Complete some goals at the beginning in case the first event is EVENT_APPROVED
#     # or EVENT_REJECTED and causes a crash
#     for _ in range(10):
#         event, object_id = goal_completed(created, completed)
#         df.append([event, object_id])
#
#     # Create 10000 rows of data
#     for _ in range(10000):
#
#         # Putting function instances directly in the choice function ran each
#         # function instead of choosing amongst them
#         event = choice(['a','b','c'], 1, p=[0.40, 0.35, 0.25])
#         if event == 'a':
#             event, object_id = goal_created(created)
#         elif event == 'b':
#             event, object_id = goal_completed(created, completed)
#         elif event == 'c':
#             event, object_id = approved_or_denied(completed, app_or_den)
#         df.append([event, object_id])
#
#
#     # Convert the list of lists to a pandas dataframe and output a csv
#     df = pd.DataFrame(df, columns=['Event', 'object_id'])
#     print(df)
#     df.to_csv('/Users/thomasmulhern/Desktop/test1.csv')
#     #path = input("csv file path:")
#     #df.to_csv(path)

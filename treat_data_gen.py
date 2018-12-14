import pandas as pd
from numpy.random import choice
from random import randint



def goal_created(created):
    # Create an event and unique object_id; add id to the "created" set and add
    # the list to the dataframe
    # Input: list to append to
    # Output: list of two items

    object_id = randint(99999999,999999999)
    while object_id in created or object_id in completed or object_id in app_or_den:
        object_id = randint(99999999,999999999)
    created.append(object_id)
    row = ['GOAL_CREATED', object_id]
    print(row)
    return row

def goal_completed(created, completed):
    # Randomly select a goal from the "created" list and move it to the "completed"
    # list
    # Input: list to pull from, list to append to
    # Output: list of two items

    # Check to make sure the list isn't empty
    if len(created) != 0 and len(created) != None:
        object_id = choice(created, replace=False)
        completed.append(object_id)
        created.remove(object_id)
        row =  ['GOAL_COMPLETED', object_id]
        print(row)
        return row
    else:
        pass

def approved_or_denied(completed, app_or_den):
    # Randomly select object_id from the list of completed goals and approve or
    # deny it. If it gets denied, send it back to the "completed" list to be
    # recompleted and approved
    # Input: list to pull from, list to append to
    # Output: list of two items

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
        print(row)
        return row

    else:
        pass

if __name__ == '__main__':

    # Instantiate the lists to hold data created in the functions
    df = []
    created = []
    completed = []
    app_or_den = []

    # Create some goals at the beginning in case the first event is
    # EVENT_COMPLETED or EVENT_APPROVED/ EVENT_REJECTED and causes a crash
    for _ in range(50):
        event, object_id = goal_created(created)
        df.append([event, object_id])

    # Complete some goals at the beginning in case the first event is EVENT_APPROVED
    # or EVENT_REJECTED and causes a crash
    for _ in range(10):
        event, object_id = goal_completed(created, completed)
        df.append([event, object_id])

    # Create 10000 rows of data
    for _ in range(10000):

        # Putting function instances directly in the choice function ran each
        # function instead of choosing amongst them
        event = choice(['a','b','c'], 1, p=[0.40, 0.35, 0.25])
        if event == 'a':
            event, object_id = goal_created(created)
        elif event == 'b':
            event, object_id = goal_completed(created, completed)
        elif event == 'c':
            event, object_id = approved_or_denied(completed, app_or_den)
        df.append([event, object_id])


    # Convert the list of lists to a pandas dataframe and output a csv
    df = pd.DataFrame(df, columns=['Event', 'object_id'])
    print(df)
    df.to_csv('/Users/thomasmulhern/Desktop/test1.csv')
    #path = input("csv file path:")
    #df.to_csv(path)

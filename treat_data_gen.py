import pandas as pd
from numpy.random import choice
from random import randint



def goal_created(df, created):
    # Create an event and unique object ID tuple, add id to the "created" set,
    # and add the tuple to the dataframe
    object_id = randint(99999999,999999999)
    #print("goal_created 1")
    created.append(object_id)
    #print("goal_created 2")
    row = ['GOAL_CREATED', object_id]
    print(row)
    return row

def goal_completed(df, created, completed):
    if len(created) != 0 or len(created) != None:
        object_id = choice(created, replace=False)
        #print( "goal_completed 1")
        completed.append(object_id)
        created.remove(object_id)
        #print("goal_completed 2")
        row =  ['GOAL_COMPLETED', object_id]
        print("goal_completed 3", row)
        return row
    else:
        pass

def approved_or_denied(df, completed, app_or_den):
    if len(completed) > 0 or len(completed) != None:
        object_id = choice(completed, replace=False)
        #print( "approved_or_denied 1")
        app_or_den.append(object_id)
        completed.remove(object_id)
        #print( "approved_or_denied 2")
        event = choice(['GOAL_APPROVED','GOAL_REJECTED'], p=[.7, .3])
        if event == 'GOAL_REJECTED':
            created.append(object_id)
            app_or_den.remove(object_id)
        row = [event, object_id]
        print('approved_or_denied 3', row)
        return row
    else:
        pass

if __name__ == '__main__':

    df = []
    created = []
    completed = []
    app_or_den = []

    for _ in range(50):
        event, object_id = goal_created(df, created)
        df.append([event, object_id])
    for _ in range(10):
        event, object_id = goal_completed(df, created, completed)
        df.append([event, object_id])

    for x in range(10000):

        print("___________________:", x)

        event = choice(['a','b','c'], 1, p=[0.40, 0.35, 0.25])
        if event == 'a':
            event, object_id = goal_created(df, created)

        elif event == 'b':
            event, object_id = goal_completed(df, created, completed)
        elif event == 'c':
            event, object_id = approved_or_denied(df, completed, app_or_den)
        elif event == 'd':
            event, object_id = approved_or_denied(df, completed, app_or_den)

        df.append([event, object_id])
    df = pd.DataFrame(df, columns=['Event', 'object_id'])
    print(df)
    df.to_csv('/Users/thomasmulhern/Desktop/test1.csv', index=False)

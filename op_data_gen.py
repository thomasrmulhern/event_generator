import pandas as pd
import numpy as np
from random import choice
import datetime
import string


def create_file(num_rows):
    #TODO: Write code to dump straight to a csv rather than creating a pandas dataframe

    '''
    Description: Create a pandas df that will hold all the data and ultimately output to json. Should have a column for
    every field we want in our final json file.
    Inputs: None
    Return: Dataframe object
    Example:
        >>>create_file()
            Empty DataFrame
            Columns: [mongoID, timestamp, type, targetUserId, targetUserName, creatorUserId, creatorUserName,
            objectId]
            Index: []
    '''

    columns = ['mongoID','timestamp','type','targetUserId','targetUserName', 'targetType', 'creatorUserId',
               'creatorUserName','creatorType','objectId']

    df = pd.DataFrame(columns=columns, index=np.arange(0, num_rows))
    return df


def choose_event(event_df):

    # TODO: Add logic so that certain related events happen in order e.g. message sent before message opened,
    # messages sent to one clinician opened by same clinician, etc.

    '''
    Description: Choose randomly from a list of possible events
    Inputs: Dataframe object
    return: string
    Examples:

        >>> choose_event()
        "Goal_created"

        >>> choose_event()
        "Goal_rejected"

        >>> choose_event()
        "Survey_answered"
    '''

    chosen_event = choice(event_df['event'])
    return chosen_event


def choose_creator(event):

    #TODO: Add logic:
        # certain events happen need to in a certain order and have the right creator e.g. dont let someone open a message
        # before they've been sent one, don't let someone answer a survey before its been assigned to them, etc.
    '''
    Description: Choose a creator for the previously chosen event based on the type of event and other logic
    Inputs: string
    Return: string
    Examples:

        >>> choose_creator("Goal_created")
        "Clinician"

        >>> choose_creator("Goal_rejected")
        "Clinician"

        >>> choose_creator("Survey_answered")
        "Patient"
    '''

    # Enumerate the values of the events column. If value equals predetermined event, use the index to look at the
    # clinician and patient columns. If either is a match, append it to the list to draw from later.
    possible_user_types = []
    for index, value in enumerate(event_df['event']):
        if value == event:
            if event_df.iloc[index]['clinician'] == 1:
                possible_user_types.append("clinician")
            if event_df.iloc[index]['patient'] == 1:
                possible_user_types.append("patient")

    # Choose a value from the possible user types
    user_type = choice(possible_user_types)

    # Enumerate the values of the userType column. Compare the chosen user type to the values, and if they are equal,
    # use the index to append potential creators to a list
    possible_users = []
    for index, value in enumerate(user_df['userType']):
        if value.lower() == user_type.lower():
            possible_users.append(user_df.iloc[index]['user'])

    # Choose a creator
    creator = choice(possible_users)

    return creator


def choose_target(event, creator):
    #TODO: Add logic:
        #patients only interact with their clinicians and vice versa
        #clinicians can only create patients

    '''
    Description: Choose an event target based on a specific type of event and a specific creator
    Inputs: string
    return: string
    Examples:

        >>> choose_target('User_created', 'Clinician_4')
            'Clinician_4'

        >>> choose_target('Message_sent', 'Clinician_1')
            'Patient_17'

        >>> choose_target('Goal_rejected', 'Clinician_3')
            'Clinician_1'


    '''

    # If the userType of the row at the index where the
    if (user_df.iloc[user_df[user_df['user'] == creator].index]['userType'] == "Clinician").item():
        creator_row = cc_df[cc_df['events'] == event]
        if creator_row['creator_clinician'].item() == 1:
            pat = creator_row['target_patient'].item()
            clin = creator_row['target_clinician'].item()
            if pat == 1 and clin == 1:
                choice_type = choice(['Patient', "Clinician"])
                a = choice(user_df.iloc[user_df[user_df['userType'] == choice_type].index]['user'].values)
                return a
            elif pat == 1 and clin == 0:
                b = choice(user_df.iloc[user_df[user_df['userType'] == 'Patient'].index]['user'].values)
                return b
            # elif clin == 1 and pat == 0:
                #c = choice(user_df.iloc[user_df[user_df['userType'] == 'Clinician'].index]['user'].values)
                #return c
            else:
                return creator
        else:
            print("HOUSTON WE HAVE A CLINICIAN PROBLEM")


    elif (user_df.iloc[user_df[user_df['user'] == creator].index]['userType'] == "Patient").item():
        creator_row = cp_df[cp_df['events'] == event]
        if creator_row['creator_patient'].item() == 1:
            pat = creator_row['target_patient'].item()
            clin = creator_row['target_clinician'].item()
            if pat == 1 and clin == 1:
                choice_type = choice(['Patient', "Clinician"])
                d = choice(user_df.iloc[user_df[user_df['userType'] == choice_type].index]['user'].values)
                return d
            elif clin == 1 and pat == 0:
                f = choice(user_df.iloc[user_df[user_df['userType'] == 'Clinician'].index]['user'].values)
                return f
            # elif pat == 1 and clin == 0:
                # e = choice(user_df.iloc[user_df[user_df['userType'] == 'Patient'].index]['user'].values)
                # return e
            else:
                return creator
        else:
            print("HOUSTON WE HAVE A PATIENT PROBLEM")


def get_userIDs(creator, target):
    '''
    Description: Get the creator and target user names for  the chosen creator and target
    Inputs: string
    Return: string, string
    Examples:

        >>> get_userIDs(clinician_2, clinician_2)
        9v9lrwx5lclc44okov5d, 9v9lrwx5lclc44okov5d

        >>> get_userIDs(clinician_2, Patient_5)
        9v9lrwx5lclc44okov5d, dt0kzk9ffhjjmtcl9lvh


        >>> get_userIDs(Patient_5, clinician_2)
        dt0kzk9ffhjjmtcl9lvh, 9v9lrwx5lclc44okov5d
    '''

    creatorID = user_df[user_df['user'] == creator]['userId'].item()
    targetID = user_df[user_df['user'] == target]['userId'].item()
    return creatorID, targetID

def get_types(creator, target):
    '''
    Description: Get the creator and target types
    Inputs: string, string
    Return: string, string
    Examples:

        >>> get_types(clinician_2, clinician_2)
        Clinician, Clinician

        >>> get_types(clinician_2, Patient_5)
       Clinician, Patient

        >>> get_types(Patient_5, clinician_2)
        Patient, Clinician
    '''
    creator_type = user_df.iloc[user_df[user_df['user'] == creator].index]['userType'].item()
    target_type = user_df.iloc[user_df[user_df['user'] == target].index]['userType'].item()

    return creator_type, target_type



def get_objectId(event):
    '''
    Description: Get the object ID for the event
    Inputs: string
    Return: string
    Examples:

        >>> get_objectId('Goal_rejected')
        q6aqbyr5e176wdz657o4

        >>> get_objectId('Message_opened')
        boevapphzp8vblskmwbd

        >>> get_objectId('User_profile_change')
        d07pkjihm273doctvr5b
    '''

    #
    return event_df.iloc[event_df[event_df['event']== event].index]['objectId'].item()


def create_timestamp(startDate):
    # TODO: add logic:
        # events happen within realistic times
    '''
    Description: Generates a timestamp by converting epoch to timestamp after adding a random number between 10 and 90
    equating to between 10 and 90 minutes
    Inputs: epoch start timer
    Return: timestamp object
    Examples:

        >>> create_timestamp(start,l)
        "2018-11-13T14:21:02.22000"

        >>> create_timestamp(start,l)
        "2018-11-13T14:43:02.22000"

        >>> create_timestamp(start,l)
        "2018-11-13T15:51:02.22000"
    '''

    delta = choice(np.arange(300, 15000))
    epoch = startDate + delta
    dt = datetime.datetime.fromtimestamp(epoch)
    new_dt = "".join('{0}-{1}-{2} {3}:{4}:{5}.{6}'.format(str(dt.year), str(dt.month), str(dt.day), str(dt.hour),
                                                          str(dt.minute),str(dt.second), str(dt.microsecond)))
    #print (f"new dt: {new_dt}, delta: {delta/3600}")
    return new_dt, epoch

def create_mongoid():
    '''
    Description: Generate random string to represent mongoid
    Inputs: None
    Return: string
    Examples:
        >>> create_mongoid()
        5beaddce8f76c34362863d1b

        >>> create_mongoid()
        P9vE1ZqsoDZJAGeHP95ESVL9

    '''

    mongoid = ''.join([choice(string.ascii_letters + string.digits) for n in range(24)])
    return mongoid


def output(df):
    '''
    Description: Turns the pandas data frame we've been working on into a json file so we can import it other
    databases, and data viz/ analytics tools for testing
    Inputs: Pandas data frame with the data we've iterated to collect
    Return: Json file
    Examples:
        >>> output(df)
        >>>What file type? (csv or json): <<csv>>
        >>>Output path: <</Users/thomasmulhern/Desktop/data.csv>>
        Process finished with exit code 0
    '''
    ext = input('What file type? (csv or json): ')
    #path = input('Path for json file: ')
    path = input('Output path: ')
    if ext == 'csv':
        return df.to_csv(path)
    if ext == 'json':
        return df.to_json(path)




if __name__ == "__main__":

    # import data into data frames
    user_df = pd.read_csv('/Users/thomasmulhern/new_desk/post/itether/data_generator/event_generator/data/user_data.csv')
    event_df = pd.read_csv('/Users/thomasmulhern/new_desk/post/itether/data_generator/event_generator/data/event_data.csv')
    cp_df = pd.read_csv('/Users/thomasmulhern/new_desk/post/itether/data_generator/event_generator/data/cp.csv')
    cc_df = pd.read_csv('/Users/thomasmulhern/new_desk/post/itether/data_generator/event_generator/data/cc.csv')

    # get user input for number of rows to create
    num_rows = int(input('How many rows of data do you want?: '))
    df = create_file(num_rows)
    start_date = 1452233440.404116 # 2016, 1, 7, 23, 10, 40, 404116 # There is no special significance to this date

    # Create the data for a single line, add it to the dataframe, and repeat for the length of the dataframe
    for index in range(num_rows):
        event = choose_event(event_df)
        creator = choose_creator(event)
        target = choose_target(event, creator)
        creatorID, targetID = get_userIDs(creator, target)
        creatorType, targetType = get_types(creator, target)
        objectid = get_objectId(event)
        timestamp, seconds = create_timestamp(start_date)
        start_date = seconds
        mongoid = create_mongoid()

        # Add rows of data to the data frame
        df.iloc[index] = {'type':event, 'creatorUserName':creator, 'targetUserName':target, 'creatorUserId':creatorID,
                          'targetUserId':targetID, 'objectId':objectid, 'timestamp':timestamp, 'mongoID':mongoid,
                          'creatorType':creatorType, 'targetType':targetType}

    #print(df.iloc[0])
    output(df)

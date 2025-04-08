# -*- coding: utf-8 -*-
"""

# Gradio Visualisation for ML Model Deployment
"""

import pandas as pd
import numpy as np
import joblib
import gradio as grd

"""Load Model"""

clf = joblib.load(filename='app/model/rfc_model.pkl')
print(clf.get_params())

"""Gradio UI Settings - Input Components"""

in_Pid = grd.Textbox(lines=1, placeholder=None, value="", label="Passenger Id")
in_PClass = grd.Radio([1, 2, 3], type="value", label="Passenger Class")
in_Pname = grd.Textbox(lines=1, placeholder=None, value="", label="Passenger Name")
in_sex = grd.Radio(['Male', 'Female'], type="value", label="Gender")
in_age = grd.Textbox(lines=1, placeholder=None, value="", label="Age of passenger in yrs")
in_sibsp = grd.Textbox(lines=1, placeholder=None, value="", label="No of siblings/spouse of the Passenger aboard")
in_parch = grd.Textbox(lines=1, placeholder=None, value="", label="No of parents/childern of the passenger aboard")
in_ticket = grd.Textbox(lines=1, placeholder=None, value="", label="Ticket number")
in_cabin = grd.Radio(['Yes', 'No'], type="value", label="Has Cabin")
in_embarked = grd.Radio(['Southampton', 'Cherbourg', 'Queenstown'], type="value", label="Port of Embarkation")
in_fare = grd.Textbox(lines=1, placeholder=None, value="", label="Passenger fare")

"""Clean input data for the model"""

def clean_df(df, drop_passenger_id):

    #Mapping functions for Categorical variables
    cabin_mapping = {'Yes':1, 'No':0}
    genders_mapping = {'Male':1, 'Female':0}

    # Transform Sex from a string to a number representation
    df['Sex_Val'] = df['Sex'].map(genders_mapping).astype(int)

    df['Embarked_S'] = (df['Embarked'] == 'Southampton')
    df['Embarked_C'] = (df['Embarked'] == 'Cherbourg')
    df['Embarked_Q'] = (df['Embarked'] == 'Queenstown')

    # Define a new feature FamilySize that is the sum of
    # Parch (number of parents or children on board) and
    # SibSp (number of siblings or spouses):
    df['FamilySize'] = df['SibSp'] + df['Parch']

    # Drop the columns we won't use:
    df = df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'Embarked'], axis=1)

    # Drop the Age column since we will be using the AgeFill column instead.
    # Drop the SibSp and Parch columns since we will be using FamilySize.
    # Drop the PassengerId column since it won't be used as a feature.
    df = df.drop(['Age', 'SibSp', 'Parch'], axis=1)

    if drop_passenger_id:
        df = df.drop(['PassengerId'], axis=1)
    return df

"""Gradio UI Settings - Output Component"""

out_label = grd.Textbox(type="text", label='Prediction', elem_id="out_textbox")

"""Label Prediction Funcion"""

def get_output_prediction(in_Pid, in_PClass, in_Pname, in_sex, in_age, in_sibsp,  in_parch,  in_ticket, in_fare, in_cabin,  in_embarked):
  input_df = pd.DataFrame({'PassengerId': [in_Pid],
                           'Pclass': [in_PClass],
                           'Name': [in_Pname],
                           'Age': [in_age],
                           'Sex': [in_sex],
                           'SibSp':[int(in_sibsp)],
                           'Parch':[int(in_parch)],
                           'Ticket':[in_ticket],
                           'Fare': [in_fare],
                           'Cabin':[in_cabin],
                           'Embarked':[in_embarked]
                           })
  #print(input_df)
  input_ = clean_df(input_df, drop_passenger_id=False);
  #print(input_)
  prediction = clf.predict(input_);
  if prediction[0] == 1:
    label = "Likely to Survive"
  else:
    label = "Less likely to Survive"
  return label

"""Create gradio interface object"""

intFace = grd.Interface(fn=get_output_prediction,
                        inputs= [in_Pid, in_PClass, in_Pname, in_sex, in_age, in_sibsp,  in_parch,  in_ticket,  in_fare, in_cabin,  in_embarked ],
                        outputs= [out_label],
                        title= 'Titanic Survival Prediction API',
                        description="Based on demographic information, predict if a passenger is likely to survive",
                        flagging_mode = "never"
                      )

intFace.launch(share=True)

#intFace.close()


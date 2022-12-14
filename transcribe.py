#!/usr/bin/env python
# coding: utf-8

# In[17]:


import time
import boto3
import os
import urllib.request
import numpy as np
import audioread
import wave
import io
import time
import json, datetime
from pathlib import Path
#Amazon files.
import logging

import requests
from botocore.exceptions import ClientError

# ******** if you want to Change the Directory to your local  *******************
#os.chdir('')

transcribe = boto3.client('transcribe')


# In[ ]:


# to upload the local speech file in S3 bucket

def upload_file(file_name, object_name=None):
    bucket='geekcon2022-zaphod' # ********************* Mention your own bucket name *****************************
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    start = time.time()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(time.time() - start)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# In[13]:


# loading the Json file

def load_json(file):

    json_filepath = Path(file)
    assert json_filepath.is_file(), "JSON file does not exist"

    data = json.load(open(json_filepath.absolute(), "r", encoding="utf-8"))
    assert "jobName" in data
    assert "results" in data
    assert "status" in data

    assert data["status"] == "COMPLETED", "JSON file Status Incomlpete."

    return data

def convert_time_stamp(n):
    ts = datetime.timedelta(seconds=float(n))
    ts = ts - datetime.timedelta(microseconds=ts.microseconds)
    return str(ts)

def decode_transcript(data):
    data = data
    decoded_data = {"time": [], "speaker": [], "comment": []}
    if "speaker_labels" in data["results"].keys():
        for segment in data["results"]["speaker_labels"]["segments"]:
            if len(segment["items"]) > 0:
                decoded_data["time"].append(convert_time_stamp(segment["start_time"]))
                decoded_data["speaker"].append(segment["speaker_label"])
                decoded_data["comment"].append("")
                for word in segment["items"]:
                    pronunciations = list(
                        filter(
                            lambda x: x["type"] == "pronunciation",
                            data["results"]["items"],
                        )
                    )
                    word_result = list(
                        filter(
                            lambda x: x["start_time"] == word["start_time"]
                            and x["end_time"] == word["end_time"],
                            pronunciations,
                        )
                    )
                    result = sorted(
                        word_result[-1]["alternatives"], key=lambda x: x["confidence"]
                    )[-1]
                    decoded_data["comment"][-1] += " " + result["content"]
                    try:
                        word_result_index = data["results"]["items"].index(
                            word_result[0]
                        )
                        next_item = data["results"]["items"][word_result_index + 1]
                        if next_item["type"] == "punctuation":
                            decoded_data["comment"][-1] += next_item["alternatives"][0][
                                "content"
                            ]
                    except IndexError:
                        pass
    #df = pandas.DataFrame(decoded_data, columns=["time", "speaker", "comment"])
    #df["comment"] = df["comment"].str.lstrip()
    return decoded_data

def write(file, **kwargs):
    data = load_json(file)
    df = decode_transcript(data)
    print(df)
    return df


# ## Main function

# In[27]:

def sound_to_text_assemblyai(filename):
    filename = "temp_audio.wav"
    #uploading file in S3 bucket
    upload_file(filename)
    s3_floc='https://s3.amazonaws.com/geekcon2022-zaphod/{}'.format(filename)
    import requests
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        # "audio_url": "https://bit.ly/3yxKEIY"
        "audio_url": s3_floc,
    }
    headers = {
        "authorization": open('assemblyai_apikey.txt','r').read().strip(),
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    print(response.json())
    transc_id = response.json()['id']

    while True:
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transc_id}"
        headers = {
            "authorization": open('assemblyai_apikey.txt','r').read().strip(),
        }
        response = requests.get(endpoint, headers=headers)
        j = response.json()
        if j['status'] == 'processing':
            time.sleep(0.1)
            continue
        print(response.json())

        return response.json()['text']



def sound_to_text_aws(filename):
    filename = "temp_audio.wav"
    #uploading file in S3 bucket
    upload_file(filename)

#***************** Accessing uploaded file in S3 bucket ******************
    s3_floc='https://s3.amazonaws.com/geekcon2022-zaphod/{}'.format(filename)

# *********************Job name has to be unique always ********************
    job_name = "GeekCon_0"
    job_uri = s3_floc

    try:
        transcribe.delete_transcription_job(TranscriptionJobName=job_name)
    except:
        pass

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2
        }
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            resurl=response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            #Downloading the Transcript
            urllib.request.urlretrieve(resurl, '{}.json'.format(job_name))
            #Storing it in Xlsx File.
            text = write( '{}.json'.format(job_name),format="xlsx")
            return text
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'FAILED':
            print('Transcription Failed')
            break
        time.sleep(5)

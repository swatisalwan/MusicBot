import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "musicbot-ibajti"

from pymongo import MongoClient
client=MongoClient("mongodb+srv://test:test@cluster0-wfyyk.mongodb.net/test?retryWrites=true&w=majority")
from musixmatch import Musixmatch
import json
musixmatch = Musixmatch('145099f77530ea27687d9ea7bbf7cd00')
def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

db=client.get_database("db_songs")
records=db.records
#create doc


def get_track(parameters):
    print(parameters)
    qTrack = parameters['song_type']
    musicArtist = parameters['music-artist']
    language  = parameters['language']
    new_song={
    'song_name':qTrack
    }
    records.insert_one(new_song)
    trackInfo=musixmatch.track_search(q_artist=musicArtist, q_track=qTrack,page_size=2, page=2, s_track_rating='desc')
   
    return trackInfo


def get_lyrics(parameters):
    track = parameters['song_type']
    artist = parameters['music_artist']
    new_lyrics={
        'song_name':track
    }
    records.insert_one(new_lyrics)
    info=musixmatch.matcher_track_get(track,artist)
    return info
#print(client)

        
def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    if response.intent.display_name == 'get_songs':
        trackInfo=get_track(response.parameters)
        #trackInfo=json.loads(trackInfoJSON)
        trackURL=trackInfo['message']['body']['track_list'][0]['track']['track_share_url']
        print(str(trackURL))
        return trackURL
    elif response.intent.display_name == 'get_lyrics':
        lyricInfo=get_lyrics(response.parameters)
        lyricURL=lyricInfo['message']['body']['track']['track_share_url']
        return lyricURL


    else:
        return response.fulfillment_text
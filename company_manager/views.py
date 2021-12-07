import json

from django.shortcuts import render
from django.contrib import messages
from .domain.models import *


def create_mech(request):
    return render(request, "mechs/add_mech.html")


def upload_flechs_json(request):
    if request.method == "POST":
        json_file = request.FILES["file"]

        if not json_file.name.endswith(".json"):
            messages.warning(request, "JSON files only")
        else:
            json_data = json.load(json_file)
            mechs = json_data["sheets"]

            for mech in mechs:
                # parse through string
                # get list of categories that contain items
segment_armor = [
    "la armor",
    "ra armor",
    "lt armor",
    "rt armor",
    "ct armor",
    "hd armor",
    "ll armor",
    "rl armor",
    "rtl armor",
    "rtr armor",
    "rtc armor",
]

all_segments = [
    "left arm",
    "right arm",
    "right torso",
    "left torso",
    "center torso",
    "left leg",
    "right leg",
]
meta_items = [
    "weapons",
    "walk mp",
    "jump mp",
]
                mech_data = get_mech_data(mech)
                segment_data = get_segment_damage_data(mech)
                pilot_data = get_pilot_data(mech["pilot"])
                #
                # crits
                # heat["sinkCapacity"]
                # uuid
                # mass
                # designation
                # pilot
                # ammo
                # internal damage
                # armor damage


def get_meta_data(src_meta_data):
    split_data = [word.lower() for word in src_meta_data.split('\n')]
    segments = {}
    for index, word in enumerate(split_data):
        if word in segment_armor:
            segments[word.split(" ")[0]]["armor"] =  int(word.split(":")[1])
        elif word.strip(":") in segments:
            segment = word.strip(":")
            for component in split_data[index:]:
                if component not in segments:
                    index += 1
                    if component != "-Empty-":
                        segments[segment]["components"][component]["name"] = component
                else:
                    break








def get_mech_data(mech_json_data):
    return {"uuid": mech_json_data["meta"]["uuid"],
             "name": mech_json_data["meta"]["designation"],
             "heat_dissipation": mech_json_data["heat"]["sinkCapacity"],
             "weight": mech_json_data["meta"]["mass"],
             }


def get_segment_damage_data(segment_json_data):
    segments = {}
    for segment in segment_json_data["armor"]:
        segments[segment]["armor_damage"] = segment["armor_damage"]
    for segment in segment_json_data["internal"]:
        segments[segment]["internal_damage"] = segment["internal_damage"]
    return segments


def get_pilot_data(pilot_json_data):
    wounds = len([wound for wound in pilot_json_data["wounds"] if not wound == "ok"])
    return { "wounds": wounds,
    }

# build_profile = {"mech_profile": create_mech_profile(mech_data),
#                  "segments": create_segments_profile(segments_data)
#                  "components": create_components_profile(components_data),
#                  "weapons": create_weapons_profile(weapons_data)}

def create_mech_profile():
    pass



import json

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .domain.models import *


def home(request):
    user = User.objects.get(id=request.user.id)
    companies = Company.objects.filter(user=user)

    return render(request, "home.html", {"user": user, "companies": companies})


def create_mech(request):
    return render(request, "mechs/add_mech.html")


def company_view(request, pk):
    user = User.objects.get(id=request.user.id)
    company = get_object_or_404(Company, pk=pk)
    mechs = BattleMech.objects.filter(company=company)
    pilots = MechWarrior.objects.filter(company=company)

    return render(
        request,
        "company/company_view.html",
        {
            "user": user,
            "company": company,
            "mechs": mechs,
            "pilots": pilots,
        },
    )


def mech_view(request, pk):
    mech = get_object_or_404(BattleMech, pk=pk)
    return render(request, "mechs/mech_view.html", {"mech": mech})


def upload_flechs_json_file(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        json_file = request.FILES["file"]

        if not json_file.name.endswith(".json"):
            messages.warning(request, "JSON files only")
        else:
            json_data = json.load(json_file)
            sheets = json_data["sheets"]

            for sheet in sheets:
                mech_id = sheet["meta"]["uuid"]
                mech_profile = get_mech_data(sheet)
                mech = BattleMech.objects.filter(id=mech_id)

                if mech:
                    # mech.update(mech_profile)
                    pass
                else:
                    designation = mech_profile["name"].split(" ")
                    try:
                        BattleMechDesign.objects.get(
                            name=designation[0], variant=designation[1]
                        )
                    except BattleMechDesign.DoesNotExist:
                        design = BattleMechDesign.objects.create(
                            name=designation[0], variant=designation[1]
                        )
                        # design.build_mech(mech_profile)

                    mech = BattleMech.objects.create(
                        id=mech_id, company=company, meta_data=mech_profile
                    )
                    mech.build_mech(mech_profile)

    return render(request, "company/upload_mechs.html")


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

segments_dict = {
    "la": "left arm",
    "ra": "right arm",
    "rt": "right torso",
    "rtr": "rear torso right",
    "rtl": "rear torso left",
    "rtc": "rear torso center",
    "lt": "left torso",
    "ct": "center torso",
    "ll": "left leg",
    "rl": "right leg",
    "hd": "head",
}

all_segments = [
    "left arm",
    "right arm",
    "right torso",
    "left torso",
    "center torso",
    "left leg",
    "right leg",
    "head",
]
meta_items = [
    "weapons",
    "walk mp",
    "jump mp",
]
# mech_data = get_mech_data(mech)
# segment_data = get_segment_damage_data(mech)
# pilot_data = get_pilot_data(mech["pilot"])
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


def get_segment_data(src_meta_data):
    split_data = [word.lower() for word in src_meta_data.split("\n")]
    segments = {}
    print(split_data)
    for index, word in enumerate(split_data):
        if word.split(":")[0] in segment_armor:
            segment = segments_dict[word.split(" ")[0]]
            # print(segment)
            segments[segment] = dict()
            segments[segment]["name"] = segment
            segments[segment]["armor"] = int(word.split(":")[1])
            # print(segments[word.split(" ")[0]]["armor"])
        elif word.strip(":") in all_segments:
            segment = word.strip(":")
            segments[segment] = dict()
            segments[segment]["components"] = dict()
            # print(segment)
            # print(split_data[index:])
            for component in split_data[index + 1 :]:
                # print(component)
                if component.strip(":") not in all_segments:
                    index += 1
                    # print(component)
                    if component and component != "-empty-":
                        segments[segment]["components"][component] = dict()
                        segments[segment]["components"][component]["name"] = component
                else:
                    break
    # print(segments)
    return segments


def get_mech_data(mech_json_data):
    return {
        "uuid": mech_json_data["meta"]["uuid"],
        "name": mech_json_data["designation"],
        "heat_dissipation": mech_json_data["heat"]["sinkCapacity"],
        "weight": mech_json_data["meta"]["mass"],
        "segments": get_segment_data(mech_json_data["meta"]["srcMTF"]),
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
    return {
        "wounds": wounds,
    }


# build_profile = {"mech_profile": create_mech_profile(mech_data),
#                  "segments": create_segments_profile(segments_data)
#                  "components": create_components_profile(components_data),
#                  "weapons": create_weapons_profile(weapons_data)}


def create_mech_profile():
    pass

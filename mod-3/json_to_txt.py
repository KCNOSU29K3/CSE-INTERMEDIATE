import json



def main():
    with open("/home/eternal_blue/GITHUB_PROJECTS/CSE-INTERMEDIATE/mod-3/data.json", "r") as file:
        json_data = json.load(file)

    with open("./mod-3/data.txt", "x") as file:
        pass

    for i in json_data["countries"]:

        if i.get("responsesPublic") is None:
            continue

        public_responses = i["responsesPublic"]


        if public_responses[0].get("remoteEducationModalitiesHigherCode") is None:
            data = "Not Found"
        else:
            data = public_responses[0]["remoteEducationModalitiesHigherCode"]


        print(data)

        with open("./mod-3/data.txt", "a") as file:
            file.write(f'{i["countryName"]}:{data}\n')


main()
import math
import random
import json

NUMBER_OF_MESSAGES = 100
NUMBER_OF_PUBLICATIONS = 50
NUMBER_OF_SUBSCRIPTIONS = 50

OPERATORS_LIST = ["=", "!=", "<=", ">=", "<", ">"]


def compute_frequency_per_field(groups):
    lst = []
    for group in groups:
        tempList = []
        for item in group:
            it = [item[0], math.ceil((NUMBER_OF_MESSAGES / 2) * item[1] / 100)]
            tempList.append(it)
        lst.append(tempList)

    return lst


def create_groups(fieldWeights):
    groups = []
    sum = 0
    
    # We transform from a dictionary to a list of touples, after which we'll order the values based on weight
    items = [list(item) for item in list(fieldWeights.items())]
    touples = sorted(items, key = lambda x: x[1], reverse=True)

    for touple in touples:
        # if the sum is lower than 100, we create a new group
        if sum + touple[1] <= 100:
            groups.append([touple])
            sum += touple[1]

        # else if adding this field will increase the sum over 100
        # if there is any percentage left
        # we will add a new group with the remainder in it 
        # and create a new group
        elif sum + touple[1] >= 100 and sum < 100:
            if touple[1] - (100 - sum) > 0:
                randomIndex = random.randrange(0, len(groups), 1)
                groups[randomIndex].append([touple[0], touple[1] - (100 - sum)])
                groups.append([[touple[0], 100 - sum]])
            sum = 100

        # if sum is bigger than 100 and the sum of the weight is also bigger than 100
        # we will pick a random group and add the touple there
        elif sum + touple[1] > 100 and sum >= 100:
            randomIndex = random.randrange(0, len(groups), 1)
            groups[randomIndex].append(touple)
            sum += touple[1]

    return groups

            
def generate_publications(values):
    publications = []

    for i in range(0, NUMBER_OF_PUBLICATIONS):
        publication = {}
        for key, value in values.items():
            if isinstance(value, list):
                publication[key] = random.choice(value)
            else:
                randomValue = round(random.uniform(value["min"], value["max"]), 2)
                publication[key] = randomValue

        publications.append(publication)
    
    return publications


def generate_dict(values, operators):
    dictionary = {}
    dictionary["operator"] = random.choice(operators)

    dictionary["value"] = random.choice(values) if isinstance(values, list) else values
    
    return dictionary


def generate_subscriptions(groups, values):
    subscriptions = []
    smallestDomainPercentage = 90

    for i in range(0, NUMBER_OF_PUBLICATIONS):
        for group in groups:
            subscription = {}
            for key, value in group:
                if value > 0:
                    if isinstance(values[key], list):
                        if key == "make":
                            if smallestDomainPercentage > 0:
                                subscription[key] = generate_dict(values[key], ["="])
                                smallestDomainPercentage -= 1
                            else:
                                subscription[key] = generate_dict(values[key], ["!="])
                        else:
                            subscription[key] = generate_dict(values[key], ["=", "!="]) 
                    else:
                        randomValue = round(random.uniform(values[key]["min"], values[key]["max"]), 2)
                        subscription[key] = generate_dict(randomValue, OPERATORS_LIST)

                    value -= 1
            subscriptions.append(subscription)

    return subscriptions

def write_to_json(fileName, dictionary):
    with open(fileName, "w") as file:
        json.dump(dictionary, file, indent=4, separators=(',', ': '), sort_keys=True)


if __name__ == "__main__":
    subscriptions = []
    publications = []

    with open("values.json", "r") as valuesJsonFile:
        values = json.load(valuesJsonFile)

    with open("subscriptionFieldsWeights.json", "r") as subscriptionFieldsWeightsFile:
        subscriptionFieldsWeights = json.load(subscriptionFieldsWeightsFile)

    groups = compute_frequency_per_field(create_groups(subscriptionFieldsWeights))

    write_to_json("publications.json", generate_publications(values))

    write_to_json("subscriptions.json", generate_subscriptions(groups, values))

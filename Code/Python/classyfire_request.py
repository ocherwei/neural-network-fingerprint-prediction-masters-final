import urllib.request
import json

filepath = "C:\\Dev\\Data\\concatenated-Pos-GNPS-MassBank-Respect.msp.txt"
classyfire_path = "C:\\Dev\\Data\\Classyfire Taxanomy\\taxanomy_path.txt"
missing_keys_path = "C:\\Dev\\Data\\Classyfire Taxanomy\\missed_inchikeys.txt"

first_inchi_key_block_set = set()

def inchi_keys():
    inchi_key_set = set()
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("INCHIKEY: "):
                inchi_key_string = line.split(" ")[1][:-1]
                first_inchi_key_block = inchi_key_string[:14]
                if first_inchi_key_block not in first_inchi_key_block_set:
                    first_inchi_key_block_set.add(first_inchi_key_block)
                    inchi_key_set.add(inchi_key_string)
    return inchi_key_set


def write_taxa_path_and_substituents(inchikey_set):
    # store the taxonomy path for this inchikey here
    missing_taxa_keys = []

    with open(classyfire_path, 'a') as f:
        for inchikey in inchikey_set:
            taxa_path = []
            substituents = []
            try:
                url = 'http://classyfire.wishartlab.com/entities/%s.json' % inchikey
                response = urllib.request.urlopen(url)
                data = json.load(response)

                # add the top-4 taxa
                keys = ['kingdom', 'superclass', 'class', 'subclass']
                for key in keys:
                    if data[key] is not None:
                        taxa_path.append(data[key]['name'])

                # add all the intermediate taxa >level 4 but above the direct parent
                for entry in data['intermediate_nodes']:
                    taxa_path.append(entry['name'])
                # add the direct parent
                taxa_path.append(data['direct_parent']['name'])
                substituents = data.get('substituents', None)

                for path in taxa_path:
                    f.write(inchikey + "  " + path + "\n")
            except:
                print("Failed on {}".format(inchikey))
                missing_taxa_keys.append(inchikey)


def write_taxa_path(inchikey_set):
    missing_taxa_keys = []
    # store the taxonomy path for this inchikey here
    for inchikey in inchikey_set:
        taxa_path = []
        substituents = []
        try:
            url = 'http://classyfire.wishartlab.com/entities/%s.json' % inchikey
            response = urllib.request.urlopen(url)
            data = json.load(response)

            # add the top-4 taxa
            keys = ['kingdom', 'superclass', 'class', 'subclass']
            with open(classyfire_path, 'a') as f:
                for index, key in enumerate(keys):
                    if data[key] is not None:
                        f.write(str(index) + "  " + inchikey + "  " + data[key]['name'] + "\n")

                # add all the intermediate taxa >level 4 but above the direct parent
                for entry in data['intermediate_nodes']:
                    f.write("4" + "  " + inchikey + entry['name'] + "\n")

                # add the direct parent
                f.write("5" + "  " + inchikey + data["direct_parent"]['name'] + "\n")
            substituents = data.get('substituents', None)
        except:
            print("Failed on {}".format(inchikey))
            missing_taxa_keys.append(inchikey)

    return missing_taxa_keys


missing_taxa_keys = write_taxa_path(inchi_keys())
count = 0

while len(missing_taxa_keys) > 0:
    previous_missing_taxa_keys = missing_taxa_keys
    missing_taxa_keys = write_taxa_path(missing_taxa_keys)
    if len(previous_missing_taxa_keys) == len(missing_taxa_keys):
        count += 1
    if count == 10:
        break


with open(missing_keys_path, 'w') as f:
    for index, key in enumerate(missing_taxa_keys):
        f.write(str(index) + "  " + key + "\n")

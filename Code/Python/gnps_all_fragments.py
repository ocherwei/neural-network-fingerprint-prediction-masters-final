import os
import pandas as pd

all_gnps_path = "G:\\Dev\\Data\\GNPSLibraries_allSMILES.mgf"
all_gnps_fragments_path = "G:\\Dev\\Data\\ALL GNPS Fragments"

inchi_key_set = set()
first_14_inchi_key_set = set()

with open(all_gnps_path, 'r') as f:
    content = f.readlines()

# >compound Kanamycin A M+H
# >formula C18H36N4O11
# >parentmass 485.0
# >ionization [M + H]+
# >InChI InChI=1S/C18H36N4O11/c19-2-6-10(25)12(27)13(28)18(30-6)33-16-5(21)1-4(20)15(14(16)29)32-17-11(26)8(22)9(24)7(3-23)31-17/h4-18,23-29H,1-3,19-22H2/t4-,5+,6-,7-,8+,9-,10-,11-,12+,13-,14-,15+,16-,17-,18-/m1/s1
# >InChIKey N/A
# >smiles O
#
# >ms2peaks

count = 1

for index, line in enumerate(content):
    if line.startswith("INCHIKEY="):
        inchi_key_index = index
        loop_index = inchi_key_index + 1
        smiles_index = inchi_key_index - 1
        parent_mass_index = smiles_index - 6

        filepath = os.path.join(all_gnps_fragments_path, "GNPS_ALL_" + str(count) + ".ms")

        inchi_key = line[9:-1]
        print(count)

        if inchi_key != "" and content[loop_index] != "END IONS\n":
            first_14_inchi_key = inchi_key[:14]
            if first_14_inchi_key not in first_14_inchi_key_set:
                inchi_key_set.add(inchi_key)
                has_mass_below_1000 = False
                with open(filepath, 'w') as f:
                    f.write(">compound GNPS ALL " + str(count) + "\n")
                    f.write(">formula N/A\n")
                    f.write(">parentmass " + content[parent_mass_index][8:])
                    f.write(">ionization N/A\n")
                    f.write(">InChI N/A\n")
                    f.write(">InChIKey " + inchi_key + "\n")
                    f.write(">smiles " + content[smiles_index][7:])
                    f.write("\n")
                    f.write(">ms2peaks\n")
                    while content[loop_index] != "END IONS\n":
                        mass, intensity = content[loop_index].split()
                        if float(mass) <= 1000:
                            has_mass_below_1000 = True
                            f.write(mass + " " + intensity + "\n")
                        loop_index += 1
                if has_mass_below_1000:
                    count += 1
                    first_14_inchi_key_set.add(first_14_inchi_key)
                else:
                    os.remove(filepath)

print(len(inchi_key_set))

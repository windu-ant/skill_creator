import os
import re
import time


# python script to convert skills into all perspectives we need

def convert_mob_var():
    # get the list of text files
    files = os.listdir()

    # Filter the files to only include text files
    text_files = [file for file in files if file.endswith('.txt')]

    if len(text_files) == 0:
        print("No text files found in the current directory.")
        return

    # Prompt the user to choose a file
    print("!!!WARNING!!! This can overwrite your current file irreversibly. Please save a copy.")
    print("Text files found in the current directory:")
    for i, file in enumerate(text_files):
        print(f"{i+1}. {file}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to the file you want to convert: "))
            if choice < 1 or choice > len(text_files):
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    global filename
    filename = text_files[choice - 1]

    # function to calculate the damage done by a skill per beat
    def recalc_dpb():
        return ((min_dmg + max_dmg) / 2) * (1 + ((crit_chance / 100) * ((crit_multi / 100) + 1))) / skill_beats

    # set variable option because it is not set by the user until later
    option = 0

    # loop through options to set skill damage parameters
    while True:
        if option == 6:
            break
        # ask user for their skill damage/beats/crit etc
        min_dmg = int(input("What do you want the minimum damage to be? "))
        max_dmg = int(input("What do you want the maximum damage to be? "))
        skill_beats = int(input("How many beats should it take? "))
        crit_chance = int(input("What is the crit chance? "))
        crit_multi = int(input("What is the crit multiplier? (150 = x2.5, 300 = x4) "))

        # calculate damage per beat after user input
        dmg_per_beat = recalc_dpb()
        print("\nThe damage per beat is ", end ='' )
        print('%.2f' % dmg_per_beat)
        # prompt the user if they are happy with their values
        response = input("\nIs this okay? (Y/N) AVERAGES as of 2023/07/01 - T1: 1.14 - T2: 3.07 - T3: 5.60 - T4 7.00 - T5 9.67 \n")

        # if the user is happy, break out of loop
        if response.lower() == 'y':
            break
        
        # loop through options to change skill parameters until user exits with 6
        while response.lower() != '6':
            print("Which input would you like to change?")
            print("Press 1 to change the minimum damage.")
            print("Press 2 to change the maximum damage.")
            print("Press 3 to change the number of skill beats.")
            print("Press 4 to change the crit chance.")
            print("Press 5 to change the crit multiplier.")
            print("Press 6 to continue if you are satisfied.")

            option = int(input("Select an option: "))

            if option == 1:
                min_dmg = int(input("Enter the new minimum damage: "))
            elif option == 2:
                max_dmg = int(input("Enter the new maximum damage: "))
            elif option == 3:
                skill_beats = int(input("Enter the new number of skill beats: "))
            elif option == 4:
                crit_chance = int(input("Enter the new crit chance: "))
            elif option == 5:
                crit_multi = int(input("Enter the new crit multiplier: "))
            elif option == 6:
                break

            dmg_per_beat = recalc_dpb()
            print("\nThe damge per beat is ", end ='' )
            print('%.2f' % dmg_per_beat)

    print("Now for some options...\n")

    # initialize variables in case they aren't set
    skill_dep1 = '0'
    skill_dep2 = '0'
    skill_dep3 = '0'

    time.sleep(1)
    
    # prompt the user for a bunch of options that are later written to file
    energy_cost = input("How much energy should it cost? ")
    skill_tier = input("What tier is the skill? ")
    skill_dep1 = input("What is the 1st skill dependency? ")
    skill_dep_per1 = input("At what percent does that skill need to be learned? ")
    skill_dep2 = input("What is the 2nd skill dependency? or '0' for no skill. ")
    if skill_dep2 != '0':
        skill_dep_per2 = input("At what percent does that skill need to be learned? ")
        skill_dep3 = input("What is the 3rd skill dependency? or '0' for no skill. ")
        if skill_dep3 != '0':
            skill_dep_per3 = input("At what percent does that skill need to be learned? ")
    ki_absorb = input("Can this attack be kiabsorbed? (on/off) ")
    is_melee = input("Is this a melee ability? (on/off) ")
    start_fight = input("Can it start a fight? (on/off) ")
    which_race = input("Which race learns this? ")
    added_affect = input("Can it (P)aralyze, (K)nockdown, or (R)emove fly? Type your options as one string - (PKR) or '0' for none ")
    added_affect = added_affect.lower()
    abil_or_skill = input("Is this an (a)bility or (s)kill? Chooose 'a' or 's' ")
    

    # store the skill NAME 
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("NAME"):
                # Extract the value after "NAME"
                skill_name = line.split("'")[1]
                skill_name = f"'{skill_name}'"
                break
    
    # print all the variables for the skill file
    with open(filename, 'a', encoding='utf-8') as f:
        if abil_or_skill == 'a':
            f.write("\n\nsset create ability " + skill_name.replace("'", "") + "\n")
        if abil_or_skill == 's':
            f.write("\n\nsset create skill " + skill_name.replace("'", "") + "\n")
        f.write(f"sset {skill_name} code do_skilldamage\n")
        f.write("sset " + skill_name + " dammsg " + skill_name.replace("'", "") + "\n")
        f.write(f"sset {skill_name} mindamage {min_dmg}\n")
        f.write(f"sset {skill_name} maxdamage {max_dmg}\n")
        f.write(f"sset {skill_name} energy {energy_cost}\n")
        f.write(f"sset {skill_name} skilltier {skill_tier}\n")
        f.write(f"sset {skill_name} beats {skill_beats}\n")
        f.write(f"sset {skill_name} ikpercentage {crit_chance}\n")
        f.write(f"sset {skill_name} ikdifference 3\n")
        f.write(f"sset {skill_name} critmulti {crit_multi}\n")
        f.write(f"sset {skill_name} skilldep1 '{skill_dep1}'\n")
        f.write(f"sset {skill_name} skilldepper1 {skill_dep_per1}\n")
        if skill_dep2 != '0':
            f.write(f"sset {skill_name} skilldep2 '{skill_dep2}'\n")
            f.write(f"sset {skill_name} skilldepper2 {skill_dep_per2}\n")
        if skill_dep3 != '0':
            f.write(f"sset {skill_name} skilldep3 '{skill_dep3}'\n")
            f.write(f"sset {skill_name} skilldepper3 {skill_dep_per3}\n")
        f.write(f"sset {skill_name} adept 100\n")
        f.write(f"sset {skill_name} kiabsorb {ki_absorb}\n")
        f.write(f"sset {skill_name} bioabsorb off\n")
        f.write(f"sset {skill_name} minpos 7\n")
        f.write(f"sset {skill_name} ismelee {is_melee}\n")
        f.write(f"sset {skill_name} startfight {start_fight}\n")
        if added_affect != '0':
            for char in added_affect:
                if char == "p":
                    f.write(f"sset {skill_name} par on\n")
                    par_percent = input("What percentage chance to paralyze? ")
                    f.write(f"sset {skill_name} parpercentage {par_percent}\n")
                if char == "k":
                    f.write(f"sset {skill_name} knockdown on\n")
                if char == "r":
                    f.write(f"sset {skill_name} remfly on\n")
        f.write(f"sset {skill_name} addrace {which_race}\n")
        f.write(f"sset {skill_name} plrace {which_race} 100\n")

    # Define the replacements for each perspective
    replacements = {
        'Hitchar': {
            '$n': 'you',
            '$s': 'your',
            '$e': 'you',
            '$N': '$N',
            '$m': 'your',
            '`s': '',
            '`es': '',
            '`S': '',
            '`ES': '',
        },
        'Hitvict': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': 'you',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        },
        'Hitroom': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': '$N',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        }
    }

    crit_replacements = {
        'Ikchar': {
            '$n': 'you',
            '$s': 'your',
            '$e': 'you',
            '$N': '$N',
            '$m': 'your',
            '`s': '',
            '`es': '',
            '`S': '',
            '`ES': '',
        },
        'Ikvict': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': 'you',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        },
        'Ikroom': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': '$N',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        }
    }

    miss_replacements = {
        'Misschar': {
            '$n': 'you',
            '$s': 'your',
            '$e': 'you',
            '$N': '$N',
            '$m': 'your',
            '`s': '',
            '`es': '',
            '`S': '',
            '`ES': '',
        },
        'Missvict': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': 'you',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        },
        'Missroom': {
            '$n': '$n',
            '$s': '$s',
            '$e': '$e',
            '$N': '$N',
            '$m': '$m',
            '`s': 's',
            '`es': 'es',
            '`S': 'S',
            '`ES': 'ES',
        }
    }

    # function to capitalize the first word, usually in case its a variable
    def capitalize_first_word(match):
        return match.group(1) + match.group(2).capitalize()

    with open(filename, 'r', encoding='utf-8') as file:
        paragraphs = file.read().split('\n\n')  # Split the file into paragraphs

    # storage for paragraphs
    modified_paragraphs = []

    # loop through the paragraphs to find user provided info and replace with dictionaries
    for paragraph in paragraphs:
        if paragraph.startswith('DESC'):
            for perspective, replacements in replacements.items():
                modified_paragraph = paragraph.replace('DESC', perspective)
                for char, replacement in replacements.items():
                    modified_paragraph = modified_paragraph.replace(char, replacement)

                modified_paragraph = re.sub(r'({}\s+)(\w+)'.format(perspective), capitalize_first_word, modified_paragraph)
                modified_paragraph = re.sub(r'([.?!]\s*)(\w+)', capitalize_first_word, modified_paragraph)

                modified_paragraphs.append("sset " + skill_name + " " + modified_paragraph)

        if paragraph.startswith('CRITICAL'):
            for perspective, replacements in crit_replacements.items():
                modified_paragraph = paragraph.replace('CRITICAL', perspective)
                for char, replacement in replacements.items():
                    modified_paragraph = modified_paragraph.replace(char, replacement)

                modified_paragraph = re.sub(r'({}\s+)(\w+)'.format(perspective), capitalize_first_word, modified_paragraph)
                modified_paragraph = re.sub(r'([.?!]\s*)(\w+)', capitalize_first_word, modified_paragraph)

                modified_paragraphs.append("sset " + skill_name + " " + modified_paragraph)

        if paragraph.startswith('MISS'):
            for perspective, replacements in miss_replacements.items():
                modified_paragraph = paragraph.replace('MISS', perspective)
                for char, replacement in replacements.items():
                    modified_paragraph = modified_paragraph.replace(char, replacement)

                modified_paragraph = re.sub(r'({}\s+)(\w+)'.format(perspective), capitalize_first_word, modified_paragraph)
                modified_paragraph = re.sub(r'([.?!]\s*)(\w+)', capitalize_first_word, modified_paragraph)

                modified_paragraphs.append("sset " + skill_name + " " + modified_paragraph)
    
    # Create additional modified paragraphs if "CRITICAL" not found
    if not any(paragraph.startswith('CRITICAL') for paragraph in paragraphs):
        for paragraph in paragraphs:
            if paragraph.startswith('DESC'):
                for perspective, replacements in crit_replacements.items():
                    modified_paragraph = paragraph.replace('DESC', perspective)
                    for char, replacement in replacements.items():
                        modified_paragraph = modified_paragraph.replace(char, replacement)

                    modified_paragraph = re.sub(r'({}\s+)(\w+)'.format(perspective), capitalize_first_word, modified_paragraph)
                    modified_paragraph = re.sub(r'([.?!]\s*)(\w+)', capitalize_first_word, modified_paragraph)

                    modified_paragraphs.append("sset " + skill_name + " " + modified_paragraph + " &R-CRITICAL HIT-&D")
    
    # create paragraph if MISS not found
    if not any(paragraph.startswith('MISS') for paragraph in paragraphs):
        modified_paragraphs.append(f"sset {skill_name} &HMisschar You missed $N with your {skill_name}")
        modified_paragraphs.append(f"sset {skill_name} &Missvict $n misses you with $s {skill_name}")
        modified_paragraphs.append(f"sset {skill_name} &HMisschar $n missed $N with $s {skill_name}")
                    

    # Append the new paragraphs to the list of paragraphs
    paragraphs.extend(modified_paragraphs)

    # Write all the paragraphs back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(paragraphs))

    """
    # Find the paragraph that contains "DESC"
    for i, paragraph in enumerate(paragraphs):
        if "DESC" in paragraph:
            for perspective, replacements in replacements.items():
                modified_paragraph = paragraph.replace('DESC', perspective)
                for char, replacement in replacements.items():
                    modified_paragraph = modified_paragraph.replace(char, replacement)

                modified_paragraph = re.sub(r'({}\s+)(\w+)'.format(perspective), capitalize_first_word, modified_paragraph)

                # Append the new paragraph to the list of paragraphs
                paragraphs.append(modified_paragraph)

    # Write all the paragraphs back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(paragraphs))
    """
    
convert_mob_var()
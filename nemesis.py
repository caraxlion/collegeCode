# Caroline Richards, csrichar@usc.edu
# ITP 116 MW 10am
# Final Project - Anonymous Reporting
# This program will create an anonymous reporting and services system
# for data collection

import sys
import mysql.connector
import webbrowser
from pandas import DataFrame
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium

def welcome():
    print("Welcome to Nemesis Anonymous Reporting!")
    print("_ * " * 10)


def create_database():
    nem_db = mysql.connector.connect(
        host="localhost",
        user="birdie",
        passwd="1W4ntT0Fly4w4y!",
        database="nemesisdatabase"
    )
    return nem_db

def create_cursor(nem_db):
    mycursor = nem_db.cursor()
    return mycursor

# mycursor.execute("CREATE DATABASE nemesisdatabase")


def main_menu():
    print("Nemesis Services")
    print("1. Make an Anonymous Report")
    print("2. Submit a Fileable Report")
    print("3. Find Resources")
    print("4. View Campus Statistics")
    print("5. View a Map of Campus Reports")
    print("6. Exit")
    selection = input("What can we do for you? ")
    print("_ * " * 10)
    return selection


def choice_error():
    print("Oops! That is not one our options.")
    print("Please input a number that is present in the menu.")


def choice_selector(choice, report, mycursor, nemesis, count):
    if choice == 1:
        new_report = anon_report(report, mycursor, nemesis, count)
        if new_report == 0:
            run_menu(nemesis, mycursor, count)
        data_tup = add_report(new_report, count)
        data_dic = collect_data(data_tup)
    elif choice == 2:
        x = file_report()
        if x == 0:
            run_menu(nemesis, mycursor, count)
    elif choice == 3:
        x = find_resource()
        if x == 0:
            run_menu(nemesis, mycursor, count)
    elif choice == 4:
        data_tup = add_report(report, count)
        data_dic = collect_data(data_tup)
        campus_stats(data_dic)
    elif choice == 5:
        data_tup = add_report(report, count)
        data_dic = collect_data(data_tup)
        map_campus(data_dic)
    elif choice == 6:
        sys.exit()


def collect_data(data_tup):
    type = ['Discrimination', 'Harassment', "Microagression", 'Assault',
            'Graffiti, Poster, or other tangible display']
    discrim = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious':0, 'Sexual':0}
    harass = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious': 0, 'Sexual': 0}
    micro = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious': 0, 'Sexual': 0}
    assa = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious': 0, 'Sexual': 0}
    graff = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious': 0, 'Sexual': 0}
    if data_tup[0] == type[0]:
        for key in discrim:
            if data_tup[1] == discrim[key]:
                discrim[key] += data_tup[1][key]
    elif data_tup[0] == type[1]:
        for key in harass:
            if data_tup[1] == harass[key]:
                harass[key] += data_tup[1][key]
    elif data_tup[0] == type[2]:
        for key in micro:
            if data_tup[1] == micro[key]:
                micro[key] += data_tup[1][key]
    elif data_tup[0] == type[3]:
        for key in assa:
            if data_tup[1] == assa[key]:
                assa[key] += data_tup[1][key]
    elif data_tup[0] == type[4]:
        for key in graff:
            if data_tup[1] == graff[key]:
                graff[key] += data_tup[1][key]
    data_sets = {'discrimination': discrim, 'harassment': harass, 'microagression': micro, 'assault': assa, 'graffiti, Poster, or other tangible display': graff}
    return data_sets




def initialize_report(mycursor):
    sections = {'type', 'category', 'involved', 'campus', 'location', 'description'}
    report = {}
    for i in sections:
        report[i] = None

    #mycursor.execute("CREATE TABLE Reports (id int PRIMARY KEY AUTO_INCREMENT, type VARCHAR(50) NOT NULL, category VARCHAR(50), involved VARCHAR(100) NOT NULL, campus VARCHAR(25) NOT NULL, location VARCHAR(50) NOT NULL, description VARCHAR(350) NOT NULL)")
    return report

def add_report(report, count):
    groups = {'type':['Discrimination', 'Harassment', "Microagression", 'Assault', 'Graffiti, Poster, or other tangible display'],
            'category': ['Ableist', 'Anti LGBT', 'Racial', 'Religious', 'Sexual']}
    type_list = list(groups['type'])
    for i in range(len(type_list)):
        if report['type'] == type_list[i]:
            ty = type_list[i]
            cat_list = list(groups['category'])
            for i in range(len(cat_list)):
                if report['category'] == cat_list[i]:
                    cat = cat_list[i]
                    count['cat'] += 1
                    tup = (ty, cat, count)
                    return tup
                else:
                    i += 1

        else:
            i += 1




def anon_report(report, mycursor, nemesis, count):
    print("Nemesis Anonymous Reporting Service")
    report_menu()
    choice = input("What type of report will you be submitting? ")
    print("_ * " * 3)
    # choice.isnumeric() is False or ?? Help
    try:
        choice = int(choice)
    except:
        choice_error()
        report_menu()
        choice = input("What type of report will you be submitting? ")
    while choice in range(1, 6):
        report['type'] = report_type(choice, report)
        if report['type'] == 0:
            run_menu(nemesis, mycursor, count)
        selection = category_menu(report)
        report['category'] = type_category(selection, report)
    involved = []
    add = "Y"
    while add == "Y":
        indi = indivduals_involved(report)
        involved.append(indi)
        add = add_individuals()
    print("_ * " * 3)
    report['involved'] = involved
    # find out if its on or off campus and save
    # get the location of the incident and save
    campus = on_or_off()
    if campus == 'on':
        report['campus'] = "on"
        loc = campus_loc()
        report['location'] = loc
    elif campus == 'off':
        report['campus'] = "off"
        loc = off_campus_loc()
        report['location'] = loc
    # get the description and save it
    report['description'] = description(report)
    # ask about submission
    submit = y_n_submit()
    if submit == 'Y':
        submission(report, mycursor, nemesis, count)
    req = view_resource()
    if req == 'Y':
        print("_ * " * 10)
        find_resource()
    else:
        print("_ * " * 10)
        run_menu(nemesis, mycursor, count)
    return report


def report_menu():
    print("Type of Report")
    print("1. Discrimination")
    print("2. Harassment")
    print("3. Microagression")
    print("4. Assault")
    print("5. Graffiti, Poster, or other tangible display")
    print("6. Return to Services Menu")


def report_type(choice, report):
    if choice == 1:
        report['type'] = "discrimination"
    elif choice == 2:
        report['type'] = "harassment"
    elif choice == 3:
        report['type'] = "microagression"
    elif choice == 4:
        report['type'] = "assault"
    elif choice == 5:
        report['type'] = "graffiti, poster, or other tangible display"
    elif choice == 6:
        return 0
    else:
        choice_error()
        report_menu()
    print("You wish to submit a", report['type'], "report.")
    return report


def category_menu(report):
    type = report['type']
    print("Type of", type )
    print("1. Ableist")
    print("2. Anti LGBT+")
    print("3. Racial")
    print("4. Religious")
    print("5. Sexual")
    selection = input("What category of", type, "are you reporting? ")
    print("_ * " * 3)
    return selection


def type_category(choice, report):
    if choice == 1:
        num = "ableist"
    elif choice == 2:
        num = "anti LGBT+"
    elif choice == 3:
        num = "racial"
    elif choice == 4:
        num = "religious"
    elif choice == 5:
        num = "sexual"
    else:
        choice_error()
        report_menu()
    report['category'] = num
    print("This was a", report['category'], "incident." )
    return report


def indivduals_involved(report):
    print("Individuals Involved:")
    print("1. Students")
    print("2. Staff")
    print("3. Faculty")
    print("4. Coach/Coaching Staff")
    print("5. Campus Guests")
    print("6. Non-university affiliates")
    print("7. Unknown")
    selection = input("Please select the best description of the individuals involved? ")
    print("There were", selection, "involved.")
    return selection


def add_individuals():
    y_n = input("Do you want to select an additional type of individual involved (Y/N? ")
    y_n = y_n.upper()
    while y_n != "Y" or y_n != "N":
        print("Oops! That is not one our options.")
        y_n = input("Do you want to select an additional type of individual involved (Y/N? ")
    return y_n


def on_or_off():
    ans = input("Did this incident occur on or off the university campus (on/off)? ")
    ans = ans.lower()
    while ans.isalpha() is False or ans != "on" or ans != "off":
        print("Oops! That is not one our options.")
        ans = input("Did this incident occur on or off the university campus (on/off)?" )
    return ans


def campus_loc():
    print("Please provide the closest on-campus location: ")
    loc = input("Location: ")
    # check the location on the text file
    inputFile = open("on-campus.txt", "r")
    contents = []
    for line in inputFile:
        contents.append(line)
    inputFile.close()
    cont = len(contents)
    for i in range(cont):
        if loc == contents[i]:
            campus_location = str(contents[i])
            return campus_location
        while i <= range(cont):
            if i < range(cont):
                i += 1
            else:
                print("Looks like that is not a recognized campus location.")
                off_campus_loc()



def off_campus_loc():
    print("Please provide the best description of the off-campus location: ")
    loc = input("Location: ")
    return loc


def description(report):
    section = report['type'].title()
    len_des = 352
    while len_des > 350:
        print("Please provide a brief description of the", section, "incident (max 350 char): ")
        description = input("")
        len_des = len(description)
        if len_des <= 350:
            print("_ * " * 3)
            return description
        else:
            print("That entry is too long. Try shortening it by exculding minute details.")


def y_n_submit():
    y_n = input("Do you want to submit this report (Y/N)? ")
    y_n = y_n.upper()
    while y_n.isalpha() is False or y_n != 'Y' or y_n != 'N':
        print("Oops! That is not one our options.")
        y_n = input("Do you want to submit this report (Y/N)? ")
    return y_n


def submission(report, mycursor, nemesis, count):
    # submit the report dictionary to a database
    # 'type', 'category', 'involved', 'campus', 'location', 'description'
    sections = list(report.values())
    mycursor.execute("INSERT INTO Reports (type, category, involved, campus, location, description) VALUES (%s, %s, %s, %s, %s, %s)",
                     sections[0], sections[1], sections[2], sections[3], sections[4], sections[5])
    nemesis.commit()
    print("Your submission has been recorded!")
    print("_ * " * 3)
    run_menu(nemesis, mycursor, count)
    print()


def view_resource():
    y_n = input("Would you like to view available resources (Y/N)? ")
    y_n = y_n.upper()
    while y_n.isalpha() is False or y_n != 'Y' or y_n != 'N':
        print("Oops! That is not one our options.")
        y_n = input("Would you like to view available resources (Y/N)? ")
        print("_ * " * 3)
    return y_n


def file_report():
    print("Which university reporting service would you like to use?")
    print("1. Trojans Care 4 Trojans")
    print("2. Relationship and Sexual Violence Prevention Services")
    choice = int("Your selection (1 or 2): ")
    if choice == 1:
        webbrowser.open("https://campussupport.usc.edu/trojans-care-4-trojans/")
    elif choice == 2:
        webbrowser.open("https://sites.google.com/usc.edu/rsvpclientservices/seek-care/talk-to-an-advocate")
    print("_ * " * 3)
    req = view_resource()
    if req == 'Y':
        print("_ * " * 10)
        find_resource()
    else:
        print("_ * " * 10)
        return 0



def find_resource():
    resource_menu()
    selection = int(input("What kind of resources are you looking for? "))
    while selection < 1 or selection > 6:
        choice_error()
        selection = resource_menu()
    if selection == 1:
        uni_systems()
    elif selection == 2:
        uni_hotlines()
    elif selection == 3:
        uni_clubs()
    elif selection == 4:
        local_hotlines()
    elif selection == 5:
        nat_hotlines()
    else:
        return 0
    print()


def resource_menu():
    print("Nemesis Resources")
    print("1. University Reporting Systems")
    print("2. University Hotlines")
    print("3. University Clubs")
    print("4. Local Hotlines")
    print("5. National Hotlines")
    print("6. Return Services Menu")
    print("_ * " * 3)


def uni_systems():
    print("Here are our University Reporting Systems resources:")
    print("* Trojans Care 4 Trojans (TC4T)")
    print("\t https://campussupport.usc.edu/trojans-care-4-trojans/")
    print("* Relationship and Sexual Violence Prevention Services")
    print("\t (213) 740-4900")
    print("\t https://sites.google.com/usc.edu/rsvpclientservices/seek-care")
    print("* Title IX Office")
    print("\t (213) 740-5086")
    print("_ * " * 3)
    find_resource()


def uni_hotlines():
    print("Here are our University Hotline resources:")
    print("Department of Public Safety")
    print("\t (213) 740-4321")
    print("* Help & Hotline (USC Office of Culture, Ethics, and Compliance)")
    print("\t (213) 740-2500 or (800) 348-7454")
    print("* USC Student Health line")
    print("\t (213) 740-9355")
    print("* Needlestick Hotline for bloodborne pathogen exposure")
    print("\t (213) 740-9355 {during business hours}")
    print("\t (323) 442-7900 {leave a message}")
    print("* Relationship and Sexual Violence Prevention Services")
    print("\t (213) 740-9355")
    print("\t (213) 740-4900")
    print("* Campus Support and Intervention")
    print("\t (213) 740-0411")
    print("* COVID-19 Hotline - (213) 740-6291")
    print("_ * " * 3)
    find_resource()


def uni_clubs():
    print("Here are our University Club resources:")
    inputFile = open("uni_clubs.txt", "r")
    contents = []
    for line in inputFile:
        club = line.split(",")
        contents.append(club)
    inputFile.close()
    for i in range(len(contents)):
        print("*", contents[i][0])
        print("\t Instagram:", contents[i][1])
        print("\t", contents[i][2])
    print("_ * " * 3)
    find_resource()



def local_hotlines():
    print("Here are our Local Los Angeles Hotline resources:")
    print("Break the Cycle - (424) 209-2532")
    print("California Youth Crisis Line - 1 (800) 843-5200")
    print("Center for Pacific Asian Family - (800) 339-3940")
    print("Child Abuse Hotline - (800) 540-4000")
    print("Coalition to Abolish Slavery & Trafficking - (888) 539-2373")
    print("Cocaine Anonymous Hotline - 1 (888) 714-8341")
    print("Didi Hirsch Suicide Prevention Hotline - (877) 727-4747")
    print("East LA Women's Center - (800) 585-6231")
    print("Elder/Dependent Abuse Hotline - 1 (877) 477-3646")
    print("Family Advocate w/ Dept. of Mental Health - (213) 738-3945")
    print("Homeless Assistance - (310) 399-6878")
    print("Jenesse Center - (800) 479-7328")
    print("Los Angeles County Department of Mental Health - (800) 854-7771")
    print("Los Angeles Gay and Lesbian Center - (323) 993-7400")
    print("Rainbow Services - (310) 547-9343")
    print("Reporting Emergencies or Graffiti - (800) 675-4357")
    print("SMART Systemwide Mental Assessment Response Team - (213) 996-1300")
    print("The Soldiers Project - (877) 576-5343")
    print("Suicide Prevention Hotline - (310) 391-1253")
    print("The Trevor Project - (866) 488-7386")
    print("TYY-hearing impaired - (562) 651-2549")
    print("_ * " * 3)
    find_resource()


def nat_hotlines():
    print("Here are our National Hotline resources:")
    print("National Mental Health Hotline – (866) 903-3787")
    print("National Domestic Violence Hotline – 1 (800) 799-7233")
    print("National Teen Dating Abuse Hotline – 1 (866) 331-9474")
    print("StrongHearts Native Helpline – 1 (844) 762-8483")
    print("Gay, Lesbian, Bisexual and Transgender National Hotline – 1 (888) 843-4564")
    print("RAINN National Sexual Assault Hotline – 1 (800) 656-4673")
    print("DOD Safe Helpline for Sexual Assault – 1 (877) 995-5247")
    print("National Human Trafficking Hotline – 1 (888) 373-7888")
    print("National Suicide Prevention Lifeline – 1 (800) 273-8255")
    print("_ * " * 3)
    find_resource()



def campus_stats(data_dicts):
    print("Nemesis Anonymous Reporting Statistics")
    report_menu()
    selection = input("What category would you like to view the data on? ")
    while selection.isnumeric() is False or selection not in range(1, 6):
        choice_error()
        report_menu()
        selection = input("What category would you like to view the data on? ")
    print("_ * " * 3)
    deploy_statistics(selection, data_dicts)


def deploy_statistics(choice, data_dicts):
    root = tk.Tk()
    for key in data_dicts:
        if key == choice:
            category = str(key)
            stat_dict = data_dicts[category]
            stat_cats = list(stat_dict.keys())
            stat_vals = list(stat_dict.values())
            data2 = {category: stat_cats, 'total': stat_vals}
            df0 = DataFrame(data2, columns=[category, 'total'])
            print(df0)
            figure0 = plt.Figure(figsize=(6, 5), dpi=100)
            ax0 = figure0.add_subplot(111)
            bar_chart = FigureCanvasTkAgg(figure0, root)
            bar_chart.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
            category = choice.title()
            df0 = df0[[category, 'total']].groupby(category).sum()
            df0.plot(kind='bar', legend=True, ax=ax0, color='r')
            ax0.set_title('Data On', choice.title())
    root.mainloop()
    print("_ * " * 3)


def map_campus(data_dicts):
    print("Nemesis Anonymous Reporting Map of Campus Reports")
    report_menu()
    selection = input("What category would you like to view the data on? ")
    while selection.isnumeric() is False or selection not in range(1, 6):
        choice_error()
        report_menu()
        selection = input("What category would you like to view the data on? ")
    deploy_map(selection, data_dicts)


def deploy_map(choice, data_dicts):
    map = folium.Map(location=[34.0205, -118.2856])
    map

def run_menu(nem_db, mycursor, count):
    nums = [1, 2, 3, 4, 5, 6]
    choice = main_menu()
    while choice.isnumeric() is False or int(choice) not in nums:
        choice_error()
        choice = main_menu()
    report = initialize_report(mycursor)
    choice = int(choice)
    choice_selector(choice, report, mycursor, nem_db, count)


def main():
    welcome()
    count = {'Ableist': 0, 'Anti LGBT': 0, 'Racial': 0, 'Religious':0, 'Sexual':0}
    nem_db = create_database()
    mycursor = create_cursor(nem_db)
    run_menu(nem_db, mycursor, count)


main()
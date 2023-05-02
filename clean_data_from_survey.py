import csv
import re
import pandas as pd

# csv output of the survey results
csv_source = '<file_path>'

csv_dictionary = { }

# exclude empty rows or repeated attempts at completing the survey
with open(csv_source, newline='') as csvfile:
    get_file = csv.reader(csvfile)
    for row in get_file:
        row_len = len(row)
        if len(row) != 0:
            try:
                test_try = int(row[0]) + 1
                csv_dictionary[int(row[0])] = row
            except:
                if 'headers' not in csv_dictionary:
                    csv_dictionary['headers'] = row
                else:
                    pass

raw_survey_dictionary = { }

# create a new dictonary, changing lists to dictionaries with keys and values
for key, value in csv_dictionary.items():
    length_dict = len(csv_dictionary[key])
    if key != 'headers':
        raw_survey_dictionary[key] = { }
        for i in range(length_dict):
            raw_survey_dictionary[key][i] = value[i]

def use_perc(percent):
    m = re.search("\d\d?\d?%", percent)
    if m:
        n = re.search("\d+", m.group())
        return int(n.group())/10
    else:
        return 0

def use_education(ed_level):
    if ed_level == 'Less than high school':
        points = 0
    elif ed_level == 'High school grad':
        points = 1
    elif ed_level == 'Some college':
        points = 2
    elif ed_level == '2 year degree':
        points = 3
    elif ed_level == '4 year degree':
        points = 4
    elif ed_level == 'Professional/MA degree':
        points = 5
    else:
        points = 6
    return points

def int_creator(value):
    try:
        value = int(value)
    except:
        value = 0
    return value

def years_twenty(input):
    n = re.search("\d+", input)
    try:
        years = int(n.group())
    except:
        years = 0
    return years

def comf_int(comf_value):
    if comf_value == 'Anyone':
        comf_points = 3
    elif comf_value == 'Most people':
        comf_points = 2
    elif comf_value == 'Some people':
        comf_points = 1
    else:
        comf_points = 0
    return comf_points

def prof_int(prof_value):
    if prof_value == 'Fluent':
        prof_points = 4
    elif prof_value == 'Advanced':
        prof_points = 3
    elif prof_value == 'Conversational / Functional':
        prof_points = 2
    elif prof_value == 'Primitive':
        prof_points = 1
    else:
        prof_points = 0
    return prof_points

def persp_int(persp_value):
    if persp_value == 'Strongly agree':
        persp_points = 6
    elif persp_value == 'Agree':
        persp_points = 5
    elif persp_value == 'Somewhat agree':
        persp_points = 4
    elif persp_value == 'Neither disagree or agree':
        persp_points = 3
    elif persp_value == 'Somewhat disagree':
        persp_points = 2
    elif persp_value == 'Disagree':
        persp_points = 1
    else:
        persp_points = 0
    return persp_points


def create_entry(part_id, clean, raw):

    for key, value in raw.items():
        clean[key] = { }

        clean[key]['token'] = value[5]
        clean[key]['start'] = value[6]
        clean[key]['end'] = value[7]
        clean[key]['ip'] = value[8]
        clean[key]['name'] = value[9]
        clean[key]['gender'] = value[12]
        clean[key]['age'] = value[14]

        clean[key]['id_deaf'] = value[15]
        clean[key]['id_hoh'] = value[16]
        clean[key]['id_other'] = value[17]

        clean[key]['deaf_family_no'] = value[18]
        clean[key]['deaf_parents'] = value[19]
        clean[key]['deaf_relatives'] = value[20]

        clean[key]['job_now_recently'] = value[46]
        clean[key]['job_sign_lang'] = value[47]
        clean[key]['job_sign_lang_other'] = value[48]

        if value[49] == 'Yes':
            clean[key]['hear_level'] = 0
        if value[50] == 'Yes':
            clean[key]['hear_level'] = 1
        if value[51] == 'Yes':
            clean[key]['hear_level'] = 2
        if value[52] == 'Yes':
            clean[key]['hear_level'] = 3
        if value[53] == 'Yes':
            clean[key]['hear_level'] = 4

            clean[key]['hear_level_other'] = value[54]

        if value[55] == 'No':
            clean[key]['ha_ci_weekly'] = 0
        else:
            clean[key]['ha_ci_weekly'] = 1
        clean[key]['ha_ci_weekly_other'] = value[56]
        print('hey')
        print(value[57])
        clean[key]['ha_ci_years_use'] = years_twenty(value[57])

        clean[key]['oppressed_asl_use'] = value[128]

        #USE
        clean[key]['use_one_you_student_eng'] = value[44]
        if clean[key]['use_one_you_student_eng'] == 'Yes':
            clean[key]['use_one_you_student_eng'] = [clean[key]['use_one_you_student_eng'], 1]
        else:
            clean[key]['use_one_you_student_eng'] = [clean[key]['use_one_you_student_eng'], 0]
        clean[key]['you_student_other'] = value[42]

        daily = 'Daily oralmost daily'
        week = 'About once or a few days a week'
        month = 'At least once a month'
        apply = "Doesn't apply"

        clean[key]['use_three_often_express_yourself_asl'] = value[58]
        if clean[key]['use_three_often_express_yourself_asl'] == daily:
            clean[key]['use_three_often_express_yourself_asl'] = [daily, 3]
        elif clean[key]['use_three_often_express_yourself_asl'] == week:
            clean[key]['use_three_often_express_yourself_asl'] = [week, 2]
        elif clean[key]['use_three_often_express_yourself_asl'] == month:
            clean[key]['use_three_often_express_yourself_asl'] = [month, 1]
        else:
            clean[key]['use_three_often_express_yourself_asl'] = [clean[key]['use_three_often_express_yourself_asl'], 0]

        clean[key]['use_three_often_express_yourself_eng'] = value[59]
        if clean[key]['use_three_often_express_yourself_eng'] == daily:
            clean[key]['use_three_often_express_yourself_eng'] = [daily, 3]
        elif clean[key]['use_three_often_express_yourself_eng'] == week:
            clean[key]['use_three_often_express_yourself_eng'] = [week, 2]
        elif clean[key]['use_three_often_express_yourself_eng'] == month:
            clean[key]['use_three_often_express_yourself_eng'] = [month, 1]
        else:
            clean[key]['use_three_often_express_yourself_eng'] = [clean[key]['use_three_often_express_yourself_eng'], 0]

        clean[key]['use_three_often_express_yourself_mix'] = value[60]
        if clean[key]['use_three_often_express_yourself_mix'] == daily:
            clean[key]['use_three_often_express_yourself_mix'] = [daily, 3]
        elif clean[key]['use_three_often_express_yourself_mix'] == week:
            clean[key]['use_three_often_express_yourself_mix'] = [week, 2]
        elif clean[key]['use_three_often_express_yourself_mix'] == month:
            clean[key]['use_three_often_express_yourself_mix'] = [month, 1]
        else:
            clean[key]['use_three_often_express_yourself_mix'] = [clean[key]['use_three_often_express_yourself_mix'], 0]

        clean[key]['use_three_often_read_home'] = value[61]
        if clean[key]['use_three_often_read_home'] == daily:
            clean[key]['use_three_often_read_home'] = [daily, 3]
        elif clean[key]['use_three_often_read_home'] == week:
            clean[key]['use_three_often_read_home'] = [week, 2]
        elif clean[key]['use_three_often_read_home'] == month:
            clean[key]['use_three_often_read_home'] = [month, 1]
        else:
            clean[key]['use_three_often_read_home'] = [clean[key]['use_three_often_read_home'], 0]

        clean[key]['use_three_often_write_home'] = value[62]
        if clean[key]['use_three_often_write_home'] == daily:
            clean[key]['use_three_often_write_home'] = [daily, 3]
        elif clean[key]['use_three_often_write_home'] == week:
            clean[key]['use_three_often_write_home'] = [week, 2]
        elif clean[key]['use_three_often_write_home'] == month:
            clean[key]['use_three_often_write_home'] = [month, 1]
        else:
            clean[key]['use_three_often_write_home'] = [clean[key]['use_three_often_write_home'], 0]

        clean[key]['use_three_often_read_work'] = value[63]
        if clean[key]['use_three_often_read_work'] == daily:
            clean[key]['use_three_often_read_work'] = [daily, 3]
        elif clean[key]['use_three_often_read_work'] == week:
            clean[key]['use_three_often_read_work'] = [week, 2]
        elif clean[key]['use_three_often_read_work'] == month:
            clean[key]['use_three_often_read_work'] = [month, 1]
        elif clean[key]['use_three_often_read_work'] == apply:
            clean[key]['use_three_often_read_work'] = [apply, 10]
        else:
            clean[key]['use_three_often_read_work'] = [clean[key]['use_three_often_read_work'], 0]

        clean[key]['use_three_often_write_work'] = value[64]
        if clean[key]['use_three_often_write_work'] == daily:
            clean[key]['use_three_often_write_work'] = [daily, 3]
        elif clean[key]['use_three_often_write_work'] == week:
            clean[key]['use_three_often_write_work'] = [week, 2]
        elif clean[key]['use_three_often_write_work'] == month:
            clean[key]['use_three_often_write_work'] = [month, 1]
        elif clean[key]['use_three_often_write_work'] == apply:
            clean[key]['use_three_often_write_work'] = [apply, 10]
        else:
            clean[key]['use_three_often_write_work'] = [clean[key]['use_three_often_write_work'], 0]

        clean[key]['use_one_lang_most_people'] = value[65]
        if clean[key]['use_one_lang_most_people'] == 'ASL':
            clean[key]['use_one_lang_most_people_asl'] = 1
            clean[key]['use_one_lang_most_people_eng'] = 0
            clean[key]['use_one_lang_most_people_mix'] = 0
        elif clean[key]['use_one_lang_most_people'] == 'SEE (or similar)':
            clean[key]['use_one_lang_most_people_asl'] = 0
            clean[key]['use_one_lang_most_people_eng'] = 0
            clean[key]['use_one_lang_most_people_mix'] = 1
        elif clean[key]['use_one_lang_most_people'] == 'Other':
            clean[key]['use_one_lang_most_people_asl'] = 0
            clean[key]['use_one_lang_most_people_eng'] = 0
            clean[key]['use_one_lang_most_people_mix'] = 0
        else:
            clean[key]['use_one_lang_most_people_asl'] = 0
            clean[key]['use_one_lang_most_people_eng'] = 1
            clean[key]['use_one_lang_most_people_mix'] = 0

        clean[key]['use_one_lang_most_people_other'] = value[66]

        clean[key]['use_one_news_asl'] = value[71]
        if clean[key]['use_one_news_asl'] == 'Yes':
            clean[key]['use_one_news_asl'] = ['Yes', 1]
        else:
            clean[key]['use_one_news_asl'] = ['No', 0]
        clean[key]['use_one_news_eng'] = value[72]
        if clean[key]['use_one_news_eng'] == 'Yes':
            clean[key]['use_one_news_eng'] = ['Yes', 1]
        else:
            clean[key]['use_one_news_eng'] = ['No', 0]
        clean[key]['use_one_news_other'] = value[73]

        clean[key]['use_ten_average_friends_asl'] = use_perc(value[74])
        clean[key]['use_ten_average_friends_spoken_eng'] = use_perc(value[75])
        clean[key]['use_ten_average_friends_mix'] = use_perc(value[76])
        clean[key]['use_ten_average_friends_other'] = use_perc(value[77])
        clean[key]['use_ten_average_friends_not_apply'] = use_perc(value[78])

        clean[key]['use_ten_average_family_asl'] = use_perc(value[79])
        clean[key]['use_ten_average_family_spoken_eng'] = use_perc(value[80])
        clean[key]['use_ten_average_family_mix'] = use_perc(value[81])
        clean[key]['use_ten_average_family_other'] = use_perc(value[82])
        clean[key]['use_ten_average_family_not_apply'] = use_perc(value[83])

        clean[key]['use_ten_average_sch_work_asl'] = use_perc(value[84])
        clean[key]['use_ten_average_sch_work_spoken_eng'] = use_perc(value[85])
        clean[key]['use_ten_average_sch_work_mix'] = use_perc(value[86])
        clean[key]['use_ten_average_sch_work_other'] = use_perc(value[87])
        clean[key]['use_ten_average_sch_work_not_apply'] = use_perc(value[88])

        clean[key]['use_ten_average_talk_asl'] = use_perc(value[89])
        clean[key]['use_ten_average_talk_spoken_eng'] = use_perc(value[90])
        clean[key]['use_ten_average_talk_mix'] = use_perc(value[91])
        clean[key]['use_ten_average_talk_other'] = use_perc(value[92])
        clean[key]['use_ten_average_talk_not_apply'] = use_perc(value[93])

        clean[key]['use_ten_average_count_asl'] = use_perc(value[94])
        clean[key]['use_ten_average_count_spoken_eng'] = use_perc(value[95])
        clean[key]['use_ten_average_count_mix'] = use_perc(value[96])
        clean[key]['use_ten_average_count_other'] = use_perc(value[97])
        clean[key]['use_ten_average_count_not_apply'] = use_perc(value[98])

        #HISTORY
        clean[key]['hist_four_know_mother_asl'] = value[21]
        if clean[key]['hist_four_know_mother_asl'] == 'Fluent':
            clean[key]['hist_four_know_mother_asl'] = ['Fluent', 4]
        elif clean[key]['hist_four_know_mother_asl'] == 'Advanced':
            clean[key]['hist_four_know_mother_asl'] = ['Advanced', 3]
        elif clean[key]['hist_four_know_mother_asl'] == 'Conversational':
            clean[key]['hist_four_know_mother_asl'] = ['Conversational', 2]
        elif clean[key]['hist_four_know_mother_asl'] == 'Primitive':
            clean[key]['hist_four_know_mother_asl'] = ['Primitive', 1]
        else:
            clean[key]['hist_four_know_mother_asl'] = ["Doesn't apply", 0]

        clean[key]['hist_four_know_mother_eng'] = value[22]
        if clean[key]['hist_four_know_mother_eng'] == 'Fluent':
            clean[key]['hist_four_know_mother_eng'] = ['Fluent', 4]
        elif clean[key]['hist_four_know_mother_eng'] == 'Advanced':
            clean[key]['hist_four_know_mother_eng'] = ['Advanced', 3]
        elif clean[key]['hist_four_know_mother_eng'] == 'Conversational':
            clean[key]['hist_four_know_mother_eng'] = ['Conversational', 2]
        elif clean[key]['hist_four_know_mother_eng'] == 'Primitive':
            clean[key]['hist_four_know_mother_eng'] = ['Primitive', 1]
        else:
            clean[key]['hist_four_know_mother_eng'] = ["Doesn't apply", 0]

        clean[key]['hist_four_know_father_asl'] = value[23]
        if clean[key]['hist_four_know_father_asl'] == 'Fluent':
            clean[key]['hist_four_know_father_asl'] = ['Fluent', 4]
        elif clean[key]['hist_four_know_father_asl'] == 'Advanced':
            clean[key]['hist_four_know_father_asl'] = ['Advanced', 3]
        elif clean[key]['hist_four_know_father_asl'] == 'Conversational':
            clean[key]['hist_four_know_father_asl'] = ['Conversational', 2]
        elif clean[key]['hist_four_know_father_asl'] == 'Primitive':
            clean[key]['hist_four_know_father_asl'] = ['Primitive', 1]
        else:
            clean[key]['hist_four_know_father_asl'] = ["Doesn't apply", 0]

        clean[key]['hist_four_know_father_eng'] = value[24]
        if clean[key]['hist_four_know_father_eng'] == 'Fluent':
            clean[key]['hist_four_know_father_eng'] = ['Fluent', 4]
        elif clean[key]['hist_four_know_father_eng'] == 'Advanced':
            clean[key]['hist_four_know_father_eng'] = ['Advanced', 3]
        elif clean[key]['hist_four_know_father_eng'] == 'Conversational':
            clean[key]['hist_four_know_father_eng'] = ['Conversational', 2]
        elif clean[key]['hist_four_know_father_eng'] == 'Primitive':
            clean[key]['hist_four_know_father_eng'] = ['Primitive', 1]
        else:
            clean[key]['hist_four_know_father_eng'] = ["Doesn't apply", 0]

        clean[key]['hist_eight_know_parents_asl'] = clean[key]['hist_four_know_mother_asl'][1] + clean[key]['hist_four_know_father_asl'][1]
        clean[key]['hist_eight_know_parents_eng'] = clean[key]['hist_four_know_mother_eng'][1] + clean[key]['hist_four_know_father_eng'][1]


        clean[key]['hist_one_you_mom_asl'] = int_creator(value[25])
        clean[key]['hist_one_you_mom_mix'] = int_creator(value[26])
        clean[key]['hist_one_you_mom_eng'] = int_creator(value[27])
        clean[key]['hist_one_you_mom_not_apply'] = int_creator(value[28])
        clean[key]['hist_one_you_dad_asl'] = int_creator(value[29])
        clean[key]['hist_one_you_dad_mix'] = int_creator(value[30])
        clean[key]['hist_one_you_dad_eng'] = int_creator(value[31])
        clean[key]['hist_one_you_dad_not_apply'] = int_creator(value[32])

        clean[key]['hist_one_parents_mom_asl'] = int_creator(value[33])
        clean[key]['hist_one_parents_mom_mix'] = int_creator(value[34])
        clean[key]['hist_one_parents_mom_eng'] = int_creator(value[35])
        clean[key]['hist_one_parents_mom_not_apply'] = int_creator(value[36])
        clean[key]['hist_one_parents_dad_asl'] = int_creator(value[37])
        clean[key]['hist_one_parents_dad_mix'] = int_creator(value[38])
        clean[key]['hist_one_parents_dad_eng'] = int_creator(value[39])
        clean[key]['hist_one_parents_dad_not_apply'] = int_creator(value[40])

        you_use = clean[key]['hist_one_you_mom_asl'] + clean[key]['hist_one_you_dad_asl']
        parents_use = clean[key]['hist_one_parents_mom_asl'] + clean[key]['hist_one_parents_dad_asl']
        clean[key]['hist_four_you_parents_asl'] = you_use + parents_use

        you_use = clean[key]['hist_one_you_mom_eng'] + clean[key]['hist_one_you_dad_eng']
        parents_use = clean[key]['hist_one_parents_mom_eng'] + clean[key]['hist_one_parents_dad_eng']
        clean[key]['hist_four_you_parents_eng'] = you_use + parents_use

        you_use = clean[key]['hist_one_you_mom_mix'] + clean[key]['hist_one_you_dad_mix']
        parents_use = clean[key]['hist_one_parents_mom_mix'] + clean[key]['hist_one_parents_dad_mix']
        clean[key]['hist_four_you_parents_mix'] = you_use + parents_use

        clean[key]['hist_six_highest_edu_you_eng'] = use_education(value[41])
        clean[key]['highest_edu_mom'] = use_education(value[42])
        clean[key]['highest_edu_dad'] = use_education(value[43])

        clean[key]['hist_seven_age_learned_asl'] = value[99]
        if clean[key]['hist_seven_age_learned_asl'] == 'Since birth':
            clean[key]['hist_seven_age_learned_asl'] = 7
        else:
            try:
                clean[key]['hist_seven_age_learned_asl'] = 7 - years_twenty(value[99])
            except:
                clean[key]['hist_seven_age_learned_asl'] = 0

        clean[key]['hist_seven_age_learned_spoken_eng'] = value[100]
        if clean[key]['hist_seven_age_learned_spoken_eng'] == 'Since birth':
            clean[key]['hist_seven_age_learned_spoken_eng'] = 7
        else:
            try:
                clean[key]['hist_seven_age_learned_spoken_eng'] = 7 - years_twenty(value[100])
            except:
                clean[key]['hist_seven_age_learned_spoken_eng'] = 0

        clean[key]['hist_seven_age_learned_mix'] = value[101]
        if clean[key]['hist_seven_age_learned_mix'] == 'Since birth':
            clean[key]['hist_seven_age_learned_mix'] = 7
        else:
            try:
                clean[key]['hist_seven_age_learned_mix'] = 7 - years_twenty(value[101])
            except:
                clean[key]['hist_seven_age_learned_mix'] = 0

        clean[key]['hist_one_read_age_eight_eng'] = value[102]
        if clean[key]['hist_one_read_age_eight_eng'] == 'Yes, I could read English before the age of 8.':
            clean[key]['hist_one_read_age_eight_eng'] = [clean[key]['hist_one_read_age_eight_eng'], 1]
        else:
            clean[key]['hist_one_read_age_eight_eng'] = [clean[key]['hist_one_read_age_eight_eng'], 0]

        clean[key]['hist_one_read_age_eight_other'] = value[103]

        clean[key]['hist_thirteen_years_solo_mainstream_eng'] = years_twenty(value[104])
        clean[key]['hist_thirteen_years_deci_mainstream_eng'] = years_twenty(value[105])
        clean[key]['hist_thirteen_years_many_mainstream_eng'] = years_twenty(value[106])

        clean[key]['hist_twenty_years_family_asl'] = years_twenty(value[107])
        clean[key]['hist_twenty_years_family_spoken_eng'] = years_twenty(value[108])
        clean[key]['hist_twenty_years_family_mix'] = years_twenty(value[109])

        clean[key]['hist_twenty_years_class_asl'] = years_twenty(value[110])
        clean[key]['hist_twenty_years_class_spoken_eng'] = years_twenty(value[111])
        clean[key]['hist_twenty_years_class_mix'] = years_twenty(value[112])

        clean[key]['hist_twenty_years_work_asl'] = years_twenty(value[113])
        clean[key]['hist_twenty_years_work_spoken_eng'] = years_twenty(value[114])
        clean[key]['hist_twenty_years_work_mix'] = years_twenty(value[115])

        #PROFICIENCY
        clean[key]['prof_three_comf_see_asl'] = comf_int(value[67])
        clean[key]['prof_three_comf_see_written_eng'] = comf_int(value[68])
        clean[key]['prof_three_comf_see_spoken_eng'] = comf_int(value[69])
        clean[key]['prof_three_comf_see_mix'] = comf_int(value[70])

        clean[key]['prof_four_understand_asl'] = prof_int(value[116])
        clean[key]['prof_four_express_asl'] = prof_int(value[117])
        clean[key]['prof_four_read_eng'] = prof_int(value[118])
        clean[key]['prof_four_write_eng'] = prof_int(value[119])
        clean[key]['prof_four_understand_spoken_eng'] = prof_int(value[120])
        clean[key]['prof_four_express_spoken_eng'] = prof_int(value[121])

        #PERSPECTIVES
        clean[key]['att_seven_feel_myself_asl'] = persp_int(value[122])
        clean[key]['att_seven_feel_myself_eng'] = persp_int(value[123])

        clean[key]['att_seven_ident_culture_asl'] = persp_int(value[124])
        clean[key]['att_seven_ident_culture_eng'] = persp_int(value[125])

        clean[key]['att_seven_imp_fluent_asl'] = persp_int(value[126])
        clean[key]['att_seven_imp_fluent_eng'] = persp_int(value[127])

    return clean


clean_survey_dictionary = { }

new_survey_dictionary = create_entry(1, clean_survey_dictionary, raw_survey_dictionary)

def dominance_score(dictionary):

    dom_dict = { }

    for key, value in dictionary.items():
        dom_dict[key] = { }

        dom_dict[key]['token'] = dictionary[key]['token']
        dom_dict[key]['gender'] = dictionary[key]['gender']
        dom_dict[key]['age'] = dictionary[key]['age']
        dom_dict[key]['id_deaf'] = dictionary[key]['id_deaf']
        dom_dict[key]['id_hoh'] = dictionary[key]['id_hoh']
        dom_dict[key]['deaf_family_no'] = dictionary[key]['deaf_family_no']
        dom_dict[key]['deaf_parents'] = dictionary[key]['deaf_parents']
        dom_dict[key]['deaf_relatives'] = dictionary[key]['deaf_relatives']
        dom_dict[key]['highest_edu_mom'] = dictionary[key]['highest_edu_mom']
        dom_dict[key]['highest_edu_dad'] = dictionary[key]['highest_edu_dad']
        dom_dict[key]['job_now_recently'] = dictionary[key]['job_now_recently']
        dom_dict[key]['job_sign_lang'] = dictionary[key]['job_sign_lang']
        dom_dict[key]['job_sign_lang_other'] = dictionary[key]['job_sign_lang_other']
        dom_dict[key]['hear_level'] = dictionary[key]['hear_level']
        dom_dict[key]['ha_ci_weekly'] = dictionary[key]['ha_ci_weekly']
        dom_dict[key]['ha_ci_weekly_other'] = dictionary[key]['ha_ci_weekly_other']
        dom_dict[key]['ha_ci_years_use'] = dictionary[key]['ha_ci_years_use']
        dom_dict[key]['oppressed_asl_use'] = dictionary[key]['oppressed_asl_use']

        #USE_ASL
        dom_dict[key]['use_three_often_express_yourself_asl'] = dictionary[key]['use_three_often_express_yourself_asl'][1]
        dom_dict[key]['use_one_lang_most_people_asl'] = dictionary[key]['use_one_lang_most_people_asl']
        dom_dict[key]['use_one_news_asl'] = dictionary[key]['use_one_news_asl'][1]
        dom_dict[key]['use_ten_average_friends_asl'] = dictionary[key]['use_ten_average_friends_asl']
        dom_dict[key]['use_ten_average_family_asl'] = dictionary[key]['use_ten_average_family_asl']
        dom_dict[key]['use_ten_average_sch_work_asl'] = dictionary[key]['use_ten_average_sch_work_asl']
        dom_dict[key]['use_ten_average_talk_asl'] = dictionary[key]['use_ten_average_talk_asl']
        dom_dict[key]['use_ten_average_count_asl'] = dictionary[key]['use_ten_average_count_asl']
        #USE_ENG
        dom_dict[key]['use_one_lang_most_people_eng'] = dictionary[key]['use_one_lang_most_people_eng']
        dom_dict[key]['use_three_often_express_yourself_eng'] = dictionary[key]['use_three_often_express_yourself_eng'][1]
        dom_dict[key]['use_one_news_eng'] = dictionary[key]['use_one_news_eng'][1]
        dom_dict[key]['use_ten_average_friends_spoken_eng'] = dictionary[key]['use_ten_average_friends_spoken_eng']
        dom_dict[key]['use_ten_average_family_spoken_eng'] = dictionary[key]['use_ten_average_family_spoken_eng']
        dom_dict[key]['use_ten_average_sch_work_spoken_eng'] = dictionary[key]['use_ten_average_sch_work_spoken_eng']
        dom_dict[key]['use_ten_average_talk_spoken_eng'] = dictionary[key]['use_ten_average_talk_spoken_eng']
        dom_dict[key]['use_ten_average_count_spoken_eng'] = dictionary[key]['use_ten_average_count_spoken_eng']

        dom_dict[key]['hist_eight_know_parents_asl'] = dictionary[key]['hist_eight_know_parents_asl']
        dom_dict[key]['hist_four_you_parents_asl'] = dictionary[key]['hist_four_you_parents_asl']
        dom_dict[key]['hist_seven_age_learned_asl'] = dictionary[key]['hist_seven_age_learned_asl']
        dom_dict[key]['hist_twenty_years_family_asl'] = dictionary[key]['hist_twenty_years_family_asl']
        dom_dict[key]['hist_twenty_years_class_asl'] = dictionary[key]['hist_twenty_years_class_asl']
        dom_dict[key]['hist_twenty_years_work_asl'] = dictionary[key]['hist_twenty_years_work_asl']

        dom_dict[key]['hist_eight_know_parents_eng'] = dictionary[key]['hist_eight_know_parents_eng']
        dom_dict[key]['hist_four_you_parents_eng'] = dictionary[key]['hist_four_you_parents_eng']
        dom_dict[key]['hist_seven_age_learned_spoken_eng'] = dictionary[key]['hist_seven_age_learned_spoken_eng']
        dom_dict[key]['hist_twenty_years_family_spoken_eng'] = dictionary[key]['hist_twenty_years_family_spoken_eng']
        dom_dict[key]['hist_thirteen_years_solo_mainstream_eng'] = dictionary[key]['hist_thirteen_years_solo_mainstream_eng']
        dom_dict[key]['hist_thirteen_years_deci_mainstream_eng'] = dictionary[key]['hist_thirteen_years_deci_mainstream_eng']
        dom_dict[key]['hist_thirteen_years_many_mainstream_eng'] = dictionary[key]['hist_thirteen_years_many_mainstream_eng']

        #ENG_ADD
        dom_dict[key]['adh_one_ha_ci_weekly_eng'] = dictionary[key]['ha_ci_weekly']
        dom_dict[key]['adh_ten_ha_ci_years_use_eng'] = dictionary[key]['ha_ci_years_use']
        dom_dict[key]['add_one_you_student_eng'] = dictionary[key]['use_one_you_student_eng'][1]
        dom_dict[key]['add_six_home_eng'] = dictionary[key]['use_three_often_read_home'][1] + dictionary[key]['use_three_often_write_home'][1]
        dom_dict[key]['add_three_often_read_home'] = dictionary[key]['use_three_often_read_home'][1]
        dom_dict[key]['add_three_often_write_home'] = dictionary[key]['use_three_often_write_home'][1]
        dom_dict[key]['add_six_work_eng'] = dictionary[key]['use_three_often_read_work'][1] + dictionary[key]['use_three_often_write_work'][1]
        dom_dict[key]['add_three_often_read_work'] = dictionary[key]['use_three_often_read_work'][1]
        dom_dict[key]['add_three_often_write_work'] = dictionary[key]['use_three_often_write_work'][1]
        dom_dict[key]['add_six_highest_edu_you_eng'] = dictionary[key]['hist_six_highest_edu_you_eng']
        dom_dict[key]['add_one_read_age_eight_eng'] = dictionary[key]['hist_one_read_age_eight_eng'][1]
        dom_dict[key]['add_three_comf_see_written_eng'] = dictionary[key]['prof_three_comf_see_written_eng']
        dom_dict[key]['add_four_read_eng'] = dictionary[key]['prof_four_read_eng']
        dom_dict[key]['add_four_write_eng'] = dictionary[key]['prof_four_write_eng']


        dom_dict[key]['hist_twenty_years_class_spoken_eng'] = dictionary[key]['hist_twenty_years_class_spoken_eng']
        dom_dict[key]['hist_twenty_years_work_spoken_eng'] = dictionary[key]['hist_twenty_years_work_spoken_eng']
        dom_dict[key]['prof_three_comf_see_asl'] = dictionary[key]['prof_three_comf_see_asl']
        dom_dict[key]['prof_four_understand_asl'] = dictionary[key]['prof_four_understand_asl']
        dom_dict[key]['prof_four_express_asl'] = dictionary[key]['prof_four_express_asl']

        dom_dict[key]['prof_three_comf_see_spoken_eng'] = dictionary[key]['prof_three_comf_see_spoken_eng']
        dom_dict[key]['prof_four_understand_spoken_eng'] = dictionary[key]['prof_four_understand_spoken_eng']
        dom_dict[key]['prof_four_express_spoken_eng'] = dictionary[key]['prof_four_express_spoken_eng']

        dom_dict[key]['att_seven_feel_myself_asl'] = dictionary[key]['att_seven_feel_myself_asl']
        dom_dict[key]['att_seven_ident_culture_asl'] = dictionary[key]['att_seven_ident_culture_asl']
        dom_dict[key]['att_seven_imp_fluent_asl'] = dictionary[key]['att_seven_imp_fluent_asl']
        dom_dict[key]['att_seven_ident_culture_asl'] = dictionary[key]['att_seven_ident_culture_asl']

        dom_dict[key]['att_seven_feel_myself_eng'] = dictionary[key]['att_seven_feel_myself_eng']
        dom_dict[key]['att_seven_ident_culture_eng'] = dictionary[key]['att_seven_ident_culture_eng']
        dom_dict[key]['att_seven_imp_fluent_eng'] = dictionary[key]['att_seven_imp_fluent_eng']
        dom_dict[key]['att_seven_ident_culture_eng'] = dictionary[key]['att_seven_ident_culture_eng']

        dom_dict[key]['use_three_often_express_yourself_mix'] = dictionary[key]['use_three_often_express_yourself_mix'][1]
        dom_dict[key]['use_one_lang_most_people_mix'] = dictionary[key]['use_one_lang_most_people_mix']
        dom_dict[key]['use_ten_average_friends_mix'] = dictionary[key]['use_ten_average_friends_mix']
        dom_dict[key]['use_ten_average_family_mix'] = dictionary[key]['use_ten_average_family_mix']
        dom_dict[key]['use_ten_average_sch_work_mix'] = dictionary[key]['use_ten_average_sch_work_mix']
        dom_dict[key]['use_ten_average_talk_mix'] = dictionary[key]['use_ten_average_talk_mix']
        dom_dict[key]['use_ten_average_count_mix'] = dictionary[key]['use_ten_average_count_mix']
        dom_dict[key]['hist_four_you_parents_mix'] = dictionary[key]['hist_four_you_parents_mix']
        dom_dict[key]['hist_seven_age_learned_mix'] = dictionary[key]['hist_seven_age_learned_mix']
        dom_dict[key]['hist_twenty_years_family_mix'] = dictionary[key]['hist_twenty_years_family_mix']
        dom_dict[key]['hist_twenty_years_class_mix'] = dictionary[key]['hist_twenty_years_class_mix']
        dom_dict[key]['hist_twenty_years_work_mix'] = dictionary[key]['hist_twenty_years_work_mix']
        dom_dict[key]['prof_three_comf_see_mix'] = dictionary[key]['prof_three_comf_see_mix']

    return dom_dict

export_csv_dict = dominance_score(new_survey_dictionary)

pd.DataFrame.from_dict(export_csv_dict, orient='index').to_csv('/Users/dave/LingUT/Dissertation/limeresult/blp_output_2.csv')

from scipy.stats import t, norm
import random

from mylib.mycolors import hsv_to_rgb

class Student:
    def __init__(self, ID, sex, teacher, status, SOL_score):
        self.ID_Number = ID
        self.Sex = sex
        self.Teacher = teacher
        self.Status = status
        self.SOL_score = SOL_score


def average_SOL_score(students):
    return sum(student.SOL_score for student in students) / len(students)


def sample_standard_deviation_SOL_score(students):
    mean = average_SOL_score(students)
    sum_diff_squares = sum((mean - s.SOL_score)**2 for s in students)
    variance = sum_diff_squares / (len(students) - 1)
    std_dev = variance ** 0.5
    return std_dev


def read_in_students_from_csv():
    students = []
    lines = open('SOL_scores_by_sex.csv', 'r').read().splitlines()
    for line in lines[1:]:
        tokens = line.split(',')
        ID = int(tokens[0])
        sex = tokens[1]
        teacher = tokens[2]
        status = tokens[3]
        SOL_score = int(tokens[4])
        students.append(Student(ID, sex, teacher, status, SOL_score))
    return students


def get_students_which_meet_conditions(students, *conditions):
    valid_students = []
    for student in students:
        if all(condition(student) for condition in conditions):
            valid_students.append(student)
    return valid_students


def is_student_meets_conditions(student, *conditions):
    return all(condition(student) for condition in conditions)


def generate_report_for_population_proportion(population_proportion, students, *conditions, sample_size=30, alpha=0.01, title=None, min_N=10):
    if title is not None:
        print(title)
        print("-" * len(title))

    sample = random.sample(students, sample_size)
    students_of_interest = get_students_which_meet_conditions(sample, *conditions)
    sample_proportion = len(students_of_interest) / len(sample)
    x = len(students_of_interest)
    if x < min_N or sample_size - x < min_N:
        print(f"Insufficient sample size. Only {x} of {sample_size} met condition.")
        print("\n\n\n")
        return

    print("IDs of sampled students:", [student.ID_Number for student in students_of_interest])

    Z = (sample_proportion - population_proportion) / (population_proportion * (1 - population_proportion) / sample_size) ** 0.5
    p_value = 2 * (1 - norm.cdf(abs(Z)))

    print("Null Hypothesis: x̄ = μ")
    print("Alternative Hypothesis: x̄ ≠ μ")
    print("Sample size =", sample_size)
    print("x =", x)
    print("π =", population_proportion)
    print("p =", sample_proportion)
    print("Z score =", Z)
    print("P Value =", p_value)
    print("Alpha =", alpha)
    if p_value < alpha:
        print("Because the p-value is less than alpha, we reject the null hypothesis "
              "in favor of the alternative hypothesis.")
    else:
        print("Because the p-value is not less than alpha, we fail to reject the null hypothesis.")
    print("\n\n\n")


def generate_report_for_population_average(population_mean, students, *conditions, sample_size=30, alpha=0.01, title=None, min_N=30):
    if title is not None:
        print(title)
        print("-" * len(title))

    students_of_interest = random.sample(get_students_which_meet_conditions(students, *conditions), sample_size)
    n = len(students_of_interest)
    if n < min_N:
        print(f"Insufficient sample size ({n}).")
        print("\n\n\n")
        return

    print("IDs of sampled students:", [student.ID_Number for student in students_of_interest])

    sample_mean = average_SOL_score(students_of_interest)
    sample_std_dev = sample_standard_deviation_SOL_score(students_of_interest)
    t_statistic = (sample_mean - population_mean) / (sample_std_dev / n ** 0.5)
    p_value = 2 * t.sf(abs(t_statistic), df=n-1)

    print("Null Hypothesis: x̄ = μ")
    print("Alternative Hypothesis: x̄ ≠ μ")
    print("n =", n)
    print("μ =", population_mean)
    print("x̄ =", sample_mean)
    print("Sx =", sample_std_dev)
    print("T statistic =", t_statistic)
    print("P Value =", p_value)
    print("Alpha =", alpha)
    if p_value < alpha:
        print("Because the p-value is less than alpha, we reject the null hypothesis in favor of the alternative hypothesis.")
    else:
        print("Because the p-value is not less than alpha, we fail to reject the null hypothesis.")
    print("\n\n\n")


def validate_data(students):
    num_students = len(students)

    num_esl_students = len(get_students_which_meet_conditions(students, is_esl))
    num_gifted_students = len(get_students_which_meet_conditions(students, is_gifted))
    num_remedial_students = len(get_students_which_meet_conditions(students, is_remedial))
    num_normal_students = len(get_students_which_meet_conditions(students, is_normal))
    assert num_students == num_esl_students + num_remedial_students + num_gifted_students + num_normal_students

    num_males = len(get_students_which_meet_conditions(students, is_male))
    num_females = len(get_students_which_meet_conditions(students, is_female))
    assert num_students == num_males + num_females

    num_low_score_students = len(get_students_which_meet_conditions(students, scored_below_400))
    num_mid_score_students = len(get_students_which_meet_conditions(students, scored_between_400_and_499))
    num_high_score_students = len(get_students_which_meet_conditions(students, scored_above_499))
    assert num_students == num_low_score_students + num_mid_score_students + num_high_score_students


all_students = lambda s: True
is_male = lambda s: s.Sex == 'M'
is_female = lambda s: s.Sex == 'F'

is_esl = lambda s: s.Status == 'ESL'
is_remedial = lambda s: s.Status == 'Remedial'
is_gifted = lambda s: s.Status == 'Gifted'
is_normal = lambda s: s.Status == ''

scored_below_400 = lambda s: s.SOL_score < 400
scored_between_400_and_499 = lambda s: 400 <= s.SOL_score <= 499
scored_above_499 = lambda s: s.SOL_score > 499


def main():
    random.seed(0)
    students = read_in_students_from_csv()
    validate_data(students)

    # The overall state average math SOL score is 467.78.
    generate_report_for_population_average(467.78, students, all_students, alpha=0.01, title='Overall Average Math Score')

    # The state average for ESL students is 404.56
    generate_report_for_population_average(404.56, students, is_esl, alpha=0.01, title='Average for ESL Students')

    # The state average for remedial students is 419.31
    generate_report_for_population_average(419.31, students, is_remedial, alpha=0.01, title='Average for Remedial Students')

    # The state average for gifted students is 562.39
    generate_report_for_population_average(562.39, students, is_gifted, alpha=0.01, title='Average for Gifted Students')

    # The proportion of all students statewide who score 399 or below is 8.47%
    generate_report_for_population_proportion(0.0847, students, scored_below_400, alpha=0.01, title='Proportion less than 400')

    # The proportion of all students statewide who score between 400 - 499 is 61.05%
    generate_report_for_population_proportion(0.6105, students, scored_between_400_and_499, alpha=0.01, title='Proportion in range [400, 500)')

    # The proportion of all students statewide who score between 500 - 600 is 30.48%
    generate_report_for_population_proportion(0.3048, students, scored_above_499, alpha=0.01, title='Proportion greater than or equal to 500')

    # The state average score for males is 470.56.
    generate_report_for_population_average(470.56, students, is_male, alpha=0.01, title='Average Male SOL Score')
    # The state average score for females is 465.22.
    generate_report_for_population_average(465.22, students, is_female, alpha=0.01, title='Average Female SOL Score')


if __name__ == '__main__':
    main()


'''
From the project specs:
The overall state average math SOL score is 467.78.
The state average for ESL students is 404.56
The state average for remedial students is 419.31.
The state average for gifted students is 562.39

The proportion of all students statewide who score 399 or below is 8.47%
The proportion of all students statewide who score between 400 - 499 is 61.05%
The proportion of all students statewide who score between 500 - 600 is 30.48%

The state average score for males is 470.56.
The state average score for females is 465.22.
'''

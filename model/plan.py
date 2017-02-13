import datetime
import yaml
from enum import Enum, unique
from model.weekly_plan import WeeklyPlan
from model.workout import Workout, WorkoutType, Intensity


@unique
class RaceDistance(Enum):
    MARATHON = 1,
    HALF_MARATHON = 2,
    KM_10 = 3


class Plan:
    def __init__(self, race_date, race_distance, time_target, shape_level, weekly_training_days):
        self.race_date = race_date
        self.race_day = self.race_date.weekday
        self.race_distance = race_distance
        self.time_target = time_target
        self.shape_level = shape_level
        self.weekly_training_days = weekly_training_days
        self.full_weeks_till_race = self.calculate_full_weeks_till_race()
        self.weekly_plan_list = list()
        self.validate_goal_is_reachable()
        for week_number in range(0, self.full_weeks_till_race, 1):
            self.weekly_plan_list.append(WeeklyPlan(week_number))

    def create(self):
        self.insert_b_level_races_or_tests()
        self.set_recovery_week()
        self.insert_volume_workouts()
        self.insert_first_quality_workouts()
        self.insert_second_quality_workouts()
        self.insert_lite_volume_workouts()

    def calculate_full_weeks_till_race(self):
        today = datetime.date.today()
        if today.weekday() == 0:
            first_sunday_from_today = today + datetime.timedelta(days=6)
        elif today.weekday() == 1:
            first_sunday_from_today = today + datetime.timedelta(days=5)
        elif today.weekday() == 2:
            first_sunday_from_today = today + datetime.timedelta(days=4)
        elif today.weekday() == 3:
            first_sunday_from_today = today + datetime.timedelta(days=3)
        elif today.weekday() == 4:
            first_sunday_from_today = today + datetime.timedelta(days=2)
        elif today.weekday() == 5:
            first_sunday_from_today = today + datetime.timedelta(days=1)
        else:
            first_sunday_from_today = today
        return (self.race_date - first_sunday_from_today).days // 7

    def validate_goal_is_reachable(self):
        pass

    def insert_b_level_races_or_tests(self):
        if self.race_distance is RaceDistance.MARATHON:
            self.add_marathon_b_races()
        elif self.race_distance.value is RaceDistance.HALF_MARATHON:
            self.add_half_marathon_b_races()

    def insert_volume_workouts(self):
        with open('resources/weekly-volume-workout-distances.yaml', 'r') as stream:
            distances = yaml.load(stream)[self.race_distance.name.lower()]
            for i in range(1, self.full_weeks_till_race):
                if self.weekly_plan_list[i].is_with_b_level_race is True:
                    continue
                volume_workout = Workout(name='Volume', workout_type=WorkoutType.VOLUME, intensity=Intensity.AEROBIC,
                                         day_in_week=5, duration=1, length=distances[i])
                self.weekly_plan_list[i].add_workout(volume_workout)

    def insert_first_quality_workouts(self):
        pass

    def insert_second_quality_workouts(self):
        pass

    def insert_lite_volume_workouts(self):
        pass

    def add_marathon_b_races(self):
        last_b_race_weekly_plan = self.weekly_plan_list[5]
        last_b_race_weekly_plan.add_workout(Workout(name='Last B level race', workout_type=WorkoutType.RACE_OR_TEST,
                                                    intensity=Intensity.VERY_INTENSE, day_in_week=5, duration=None,
                                                    length=21))
        last_b_race_weekly_plan.is_with_b_level_race = True
        last_b_race_weekly_plan.is_recovery_week = False

        before_pressure_raise_b_race_weekly_plan = self.weekly_plan_list[11]
        before_pressure_raise_b_race_weekly_plan.add_workout(Workout(
            name='Before tense B level race', workout_type=WorkoutType.RACE_OR_TEST, intensity=Intensity.VERY_INTENSE,
            day_in_week=5, duration=None, length=21))
        before_pressure_raise_b_race_weekly_plan.is_with_b_level_race = True
        before_pressure_raise_b_race_weekly_plan.is_recovery_week = False

        if self.full_weeks_till_race > 17:
            baseline_b_race_weekly_plan = self.weekly_plan_list[17]
            baseline_b_race_weekly_plan.add_workout(Workout(
                name='Baseline B level race', workout_type=WorkoutType.RACE_OR_TEST, intensity=Intensity.VERY_INTENSE,
                day_in_week=5, duration=None, length=21))
            baseline_b_race_weekly_plan.is_with_b_level_race = True
            baseline_b_race_weekly_plan.is_recovery_week = False

    def add_half_marathon_b_races(self):
        last_b_race_weekly_plan = self.weekly_plan_list[5]
        last_b_race_weekly_plan.add_workout(Workout(name='Last B level race', workout_type=WorkoutType.RACE_OR_TEST,
                                                    intensity=Intensity.VERY_INTENSE, day_in_week=5, duration=None,
                                                    length=15))
        last_b_race_weekly_plan.is_with_b_level_race = True
        last_b_race_weekly_plan.is_recovery_week = False

        before_pressure_raise_b_race_weekly_plan = self.weekly_plan_list[11]
        before_pressure_raise_b_race_weekly_plan.add_workout(Workout(
            name='Before tense B level race', workout_type=WorkoutType.RACE_OR_TEST, intensity=Intensity.VERY_INTENSE,
            day_in_week=5, duration=None, length=15))
        before_pressure_raise_b_race_weekly_plan.is_with_b_level_race = True
        before_pressure_raise_b_race_weekly_plan.is_recovery_week = False

        if self.full_weeks_till_race > 17:
            baseline_b_race_weekly_plan = self.weekly_plan_list[17]
            baseline_b_race_weekly_plan.add_workout(Workout(
                name='Baseline B level race', workout_type=WorkoutType.RACE_OR_TEST, intensity=Intensity.VERY_INTENSE,
                day_in_week=5, duration=None, length=10))
            baseline_b_race_weekly_plan.is_with_b_level_race = True
            baseline_b_race_weekly_plan.is_recovery_week = False

    def set_recovery_week(self):
        for i in range(6, self.full_weeks_till_race, 3):
            self.weekly_plan_list[i].is_recovery_week = True

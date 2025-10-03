from datetime import time

schedule_a = {
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=20): "Period 2",
    time(hour=10, minute=15): "Brunch",
    time(hour=10, minute=30): "Period 3",
    time(hour=11, minute=30): "Period 4",
    time(hour=12, minute=25): "Lunch",
    time(hour=12, minute=55): "Period 5",
    time(hour=12+1, minute=50): "Period 6",
    time(hour=12+2, minute=45): "Period 7",
    time(hour=12+3, minute=40): "After School"
}

schedule_b = {
    time(hour=0, minute=0): "Before School",
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=10): "Period 2",
    time(hour=9, minute=55): "Brunch",
    time(hour=10, minute=10): "Period 3",
    time(hour=11, minute=00): "Period 4",
    time(hour=11, minute=45): "Lunch",
    time(hour=12, minute=15): "Period 5",
    time(hour=12+1, minute=00): "Period 6",
    time(hour=12+1, minute=45): "Period 7",
    time(hour=12+2, minute=30): '"Collaboration" period or something',
    time(hour=12+3, minute=45): "After School"
}

pride_1 = {
    time(hour=0, minute=0): "Before School",
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=15): "Period 2",
    time(hour=10, minute=5): "Brunch",
    time(hour=10, minute=20): "Period 3",
    time(hour=11, minute=15): "Period 4",
    time(hour=12, minute=5): "PRIDE",
    time(hour=12, minute=40): "Lunch",
    time(hour=12+1, minute=10): "Period 5",
    time(hour=12+2, minute=00): "Period 6",
    time(hour=12+2, minute=50): "Period 7",
    time(hour=12+3, minute=40): "After School"
}

pride_2 = {
    time(hour=0, minute=0): "Before School",
    time(hour=8, minute=30): "Period 1",
    time(hour=9, minute=15): "Period 2",
    time(hour=10, minute=5): "Brunch",
    time(hour=10, minute=20): "Period 3",
    time(hour=11, minute=15): "Period 4",
    time(hour=12, minute=5): "Lunch",
    time(hour=12, minute=35): "Period 5",
    time(hour=12+1, minute=25): "Period 6",
    time(hour=12+2, minute=15): "Period 7",
    time(hour=12+3, minute=5): "PRIDE",
    time(hour=12+3, minute=40): "After School"
}

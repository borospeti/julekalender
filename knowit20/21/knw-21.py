#!/usr/bin/env python3

from queue import PriorityQueue

class Patient:
    def __init__(self, name, severity, arrival):
        self.name = name
        self.severity = severity
        self.arrival = arrival

    def __lt__(self, other):
        return (self.severity < other.severity
                or (self.severity == other.severity and self.arrival < other.arrival)
                or (self.severity == other.severity and self.arrival == other.arrival and self.name < other.name))

    def __eq__(self, other):
        return self.severity == other.severity and self.arrival == other.arrival and self.name == other.name

    def __str__(self):
        return f'{self.name}({self.severity},{self.arrival})'

class Hospital:
    def __init__(self):
        self.events = []
        self.time = 0
        self.waiting = PriorityQueue()
        self.treated = 0

    def enqueue(self, name, severity):
        self.waiting.put(Patient(name, severity, self.time))
        self.time += 1

    def treat(self):
        patient = self.waiting.get_nowait()
        if patient.name == 'Claus':
            print(self.treated)
        self.treated += 1

    def load(self, filename):
        with open(filename) as f:
            self.events = [line.strip() for line in f.readlines()]

    def process(self):
        for event in self.events:
            if event.startswith('---'):
                self.treat()
            else:
                name, sev = event.split(',')
                self.enqueue(name, int(sev))
        while not self.waiting.empty():
            self.treat()


hospital = Hospital()
hospital.load('input.txt')
hospital.process()

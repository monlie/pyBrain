# distutils: language = c++
from libcpp.queue cimport priority_queue


cdef class TimeManager:
    cdef priority_queue[double]* time_queue
    cdef double cur_time

    def __cinit__(self, double t=-1000.0):
        self.cur_time = t
        self.time_queue = new priority_queue[double]()

    def __dealloc(self):
        del self.time_queue

    def add_simulation(self, double t):
        if t < self.cur_time:
            raise ValueError("you cannot travel to the past bro")
        self.time_queue.push(t)

    def get_time_difference(self, double t):
        if t < self.cur_time:
            raise ValueError("you cannot travel to the past bro")
        if self.time_queue.empty():
            return t - self.cur_time
        cdef double top = self.time_queue.top()
        return t - self.cur_time if t < top else t - top

    def update(self, double t):
        if t < self.cur_time:
            raise ValueError("you cannot travel to the past bro")
        cdef double top
        if not self.time_queue.empty():
            top = self.time_queue.top()
            if t >= top:
                self.time_queue.pop()
                self.cur_time = top

#!/usr/bin/env python
"""Python class for reading data from rosbag files into Matlab"""

__author__ = "Daniel Koch <daniel.koch@byu.edu>"
__version__ = 0.1

import rosbag
import yaml

class PyBag:
    """Class for extracting data from rosbag files"""

    def __init__(self, path):
        self.bag = rosbag.Bag(path, 'r')

    def __exit(self):
        self.bag.close()

    def info(self):
        return yaml.load(self.bag._get_yaml_info())

    def topics(self):
        """Return a list of all topics in the bag"""
        return self.bag.get_type_and_topic_info()[1].keys()

    def types(self):
        """Return a list of the message type of all topics in the bag"""
        return [ var[0] for var in self.bag.get_type_and_topic_info()[1].values() ]

    def start_time(self):
        """Return the timestamp of the first message in the bag"""
        return self.bag.get_start_time()

    def end_time(self):
        """Return the timestamp of the last message in the bag"""
        return self.bag.get_end_time()

    def data(self):
        """Return the data from all messages in the bag as a nested dict"""
        data_dict = {}
        for topic, msg, t in self.bag.read_messages():
            if not topic in data_dict:
                data_dict[self.topic_to_field(topic)] = self.initialize_topic(msg)
            self.extract_msg_data(msg, data_dict[self.topic_to_field(topic)])
        return data_dict

    def initialize_topic(self, msg):
        """Recursively intialize the data structure from a message"""
        if not hasattr(msg, '__slots__'):
            return []
        else:
            recurse_dict = {}
            for slot in getattr(msg, '__slots__'):
                recurse_dict[slot] = self.initialize_topic(getattr(msg, slot))
            return recurse_dict

    def extract_msg_data(self, msg, data):
        """Recursively extract data from a message"""
        if not hasattr(msg, '__slots__'):
            data.append(msg)
        else:
            for slot in getattr(msg, '__slots__'):
                self.extract_msg_data(getattr(msg, slot), data[slot])

    def topic_to_field(self, topic):
        """Convert a topic name to a valid variable name"""
        return topic[1:].replace('/','_')

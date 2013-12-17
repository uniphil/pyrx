import sys
import timeit

original_stdout = sys.stdout

normal_setup = '''
import os
import sys
import pyrx
f = open(os.devnull, 'w')
sys.stdout = f
rx = pyrx.Factory({"register_core_types": True})
sch = {'required': {'season': '//str', 'sections': {'type': '//arr', 'contents': {'type': '//rec', 'required': {'type': '//str', 'session': '//str', 'mandatory': '//bool', 'campus': '//str', 'timeslots': {'type': '//arr', 'contents': {'required': {'term_end': '//str', 'end_time': '//str', 'start_time': '//str', 'instructors': {'type': '//arr', 'contents': '//str'}, 'location': '//str', 'day_of_week': '//int', 'term_start': '//str'}, 'type': '//rec'}}}, 'optional': {'solus': {'required': {'index': '//str', 'id': '//str'}, 'type': '//rec'}}}}, 'year': '//str'}, 'type': '//rec'}
schema = rx.make_schema(sch)
data = {'season': 'fall', 'sections': [{'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '13:30', 'start_time': '12:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 2, 'term_start': '2013-09-09'}, {'term_end': '2013-11-29', 'end_time': '12:30', 'start_time': '11:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '001', 'id': '2427'}, 'type': 'lecture', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 3, 'term_start': '2013-09-09'}], 'solus': {'index': '002', 'id': '2429'}, 'type': 'lab', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '003', 'id': '2431'}, 'type': 'lab', 'campus': 'main'}], 'year': '2013'}
'''

trace_good_setup = '''
import os
import sys
import pyrx
f = open(os.devnull, 'w')
sys.stdout = f
rx = pyrx.Factory({"register_core_types": True})
sch = {'required': {'season': '//str', 'sections': {'type': '//arr', 'contents': {'type': '//rec', 'required': {'type': '//str', 'session': '//str', 'mandatory': '//bool', 'campus': '//str', 'timeslots': {'type': '//arr', 'contents': {'required': {'term_end': '//str', 'end_time': '//str', 'start_time': '//str', 'instructors': {'type': '//arr', 'contents': '//str'}, 'location': '//str', 'day_of_week': '//int', 'term_start': '//str'}, 'type': '//rec'}}}, 'optional': {'solus': {'required': {'index': '//str', 'id': '//str'}, 'type': '//rec'}}}}, 'year': '//str'}, 'type': '//rec'}
schema = rx.make_schema(sch, trace=True)
data = {'season': 'fall', 'sections': [{'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '13:30', 'start_time': '12:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 2, 'term_start': '2013-09-09'}, {'term_end': '2013-11-29', 'end_time': '12:30', 'start_time': '11:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '001', 'id': '2427'}, 'type': 'lecture', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 3, 'term_start': '2013-09-09'}], 'solus': {'index': '002', 'id': '2429'}, 'type': 'lab', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '003', 'id': '2431'}, 'type': 'lab', 'campus': 'main'}], 'year': '2013'}
'''

trace_bad_setup = '''
import os
import sys
import pyrx
f = open(os.devnull, 'w')
sys.stdout = f
rx = pyrx.Factory({"register_core_types": True})
sch = {'required': {'season': '//str', 'sections': {'type': '//arr', 'contents': {'type': '//rec', 'required': {'type': '//str', 'session': '//str', 'mandatory': '//bool', 'campus': '//str', 'timeslots': {'type': '//arr', 'contents': {'required': {'term_end': '//str', 'end_time': '//str', 'start_time': '//str', 'instructors': {'type': '//arr', 'contents': '//str'}, 'location': '//str', 'day_of_week': '//int', 'term_start': '//str'}, 'type': '//rec'}}}, 'optional': {'solus': {'required': {'index': '//str', 'id': '//str'}, 'type': '//rec'}}}}, 'year': '//str'}, 'type': '//rec'}
schema = rx.make_schema(sch, trace=True)
data = {'season': 'fall', 'sections': [{'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '13:30', 'start_time': '12:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 2, 'term_start': '2013-09-09'}, {'term_end': '2013-11-29', 'end_time': '12:30', 'start_time': '11:30', 'instructors': ['instructors/lamb-margaret'], 'location': 'Humphrey Aud', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '001', 'id': 2427}, 'type': 'lecture', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 3, 'term_start': '2013-09-09'}], 'solus': {'index': '002', 'id': '2429'}, 'type': 'lab', 'campus': 'main'}, {'session': 'Regular Academic Session', 'mandatory': True, 'timeslots': [{'term_end': '2013-11-29', 'end_time': '10:30', 'start_time': '8:30', 'instructors': ['Staff'], 'location': 'Goodwin RM248', 'day_of_week': 4, 'term_start': '2013-09-09'}], 'solus': {'index': '003', 'id': '2431'}, 'type': 'lab', 'campus': 'main'}], 'year': '2013'}
'''

iterations = 10000

normal = timeit.timeit('schema.check(data)', setup=normal_setup, number=iterations)
traced_good = timeit.timeit('schema.check(data)', setup=trace_good_setup, number=iterations)
traced_bad = timeit.timeit('schema.check(data)', setup=trace_bad_setup, number=iterations)

sys.stdout = original_stdout

print 'normal     ', normal / iterations * 1000, 'ms per check'
print 'traced good', traced_good / iterations * 1000, 'ms per check'
print 'traced bad ', traced_bad / iterations * 1000, 'ms per check'

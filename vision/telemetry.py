"""Read-only process memory measurements; unavailable values stay null."""
import ctypes
import sys


def process_memory():
    if sys.platform != 'win32':
        return {'working_set_mib': None, 'process_peak_working_set_mib': None}
    class Counters(ctypes.Structure):
        _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [
            (name, ctypes.c_size_t) for name in ('peak', 'working', 'quota_peak_paged',
            'quota_paged', 'quota_peak_nonpaged', 'quota_nonpaged', 'pagefile', 'peak_pagefile')]
    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    function = ctypes.windll.psapi.GetProcessMemoryInfo
    function.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
    if not function(ctypes.c_void_p(-1), ctypes.byref(counters), counters.cb):
        return {'working_set_mib': None, 'process_peak_working_set_mib': None}
    return {'working_set_mib': counters.working / 2**20,
            'process_peak_working_set_mib': counters.peak / 2**20}

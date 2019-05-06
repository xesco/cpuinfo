import json

def to_bytes(_dict, enc='utf-8'):
    """Convert dict to byte-json"""
    return bytes(json.dumps(_dict), enc)

def get_totals(cpuinfo):
    """Compute totals:
       - real: physical CPUs
       - cores: cores x physical CPU
       - total: logical CPUs real*cores*siblings
    Note: Siblings are only counted if Hyperthreading is enabled
    """
    # We assume same CPU architecture for multi CPU systems
    real     = len({cpuinfo[k]['physical_id'] for k in cpuinfo.keys()})
    cores    = int(cpuinfo['0']['cpu_cores'])
    total    = real*cores

    # Hyperthreading support (added for completeness)
    siblings = int(cpuinfo['0']['siblings'])
    if cores != siblings:
        cpuinfo['siblings'] = siblings
        total *= siblings
    return real, cores, total

def get_cpu_info(file_path='/proc/cpuinfo'):
    """Get System's CPU/s specifications as a dict"""
    cpuinfo = {}
    with open(file_path) as fd:
        for line in fd:
            try:
                key, value = extract_values(line)
                if key == 'processor':
                    processor = value
                    cpuinfo[processor] = {} 
                else:
                   # note: this breaks if 'processor' is not the first key
                    cpuinfo[processor][key] = value
            except ValueError:
                # next processor
                pass

    cpuinfo['real'], cpuinfo['cores'], cpuinfo['total'] = get_totals(cpuinfo)
    return to_bytes(cpuinfo)

def extract_values(line):
    """"Normalize lines taken from /proc/cpuinfo"""
    key, value = line.split(':')
    key, value = key.strip(), value.strip()
    key = key.replace(' ', '_')

    # values as lists
    if key.lower() in ('flags', 'bugs'):
        value = value.split()
    return key.lower(), value

def validate_port(port):
    """Check port is an int an in range: might throw Value expection"""

    port = int(port)
    if not (port >= 1024 and port <= 65535):
        raise ValueError
    return port

# END

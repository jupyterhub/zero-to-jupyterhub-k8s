#/usr/bin/python3

"""Kubernetes API access functions"""

import logging

scale_logger = logging.getLogger("scale")
logging.getLogger("kubernetes").setLevel(logging.WARNING)

SYMBOLS = {
    'customary': ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext': ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                      'zetta', 'iotta'),
    'iec': ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext': ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                'zebi', 'yobi'),
}


def get_pod_host_name(pod):
    """Return the host node name of the pod"""
    # Based on Kubernetes API:
    # https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podspec
    # ** API is unclear the value of nodeName flag after the pod is scheduled
    return pod.spec.node_name


def get_pod_memory_request(pod):
    """Returns the amount of memory requested
    by the node"""
    node_memory_request = 0
    try:
        node_memory_request = \
            convert_size(pod.spec.containers[0].resources.requests['memory'])
    except (KeyError, TypeError):
        pass
    return node_memory_request


def get_node_memory_capacity(node):
    """Converts the specific memory entry 
    of the kubernetes API into the byte capacity"""
    return convert_size(node.status.capacity['memory'])


def convert_size(s):
    if s.isdigit():
        return int(s)
    else:
        return human2bytes(s)


def human2bytes(s):
    """
    Copied from https://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/

    Attempts to guess the string format based on default symbols
    set and return the corresponding bytes as an integer.
    When unable to recognize the format ValueError is raised.

      >>> human2bytes('0 B')
      0
      >>> human2bytes('1 K')
      1024
      >>> human2bytes('1 M')
      1048576
      >>> human2bytes('1 Gi')
      1073741824
      >>> human2bytes('1 tera')
      1099511627776

      >>> human2bytes('0.5kilo')
      512
      >>> human2bytes('0.1  byte')
      0
      >>> human2bytes('1 k')  # k is an alias for K
      1024
      >>> human2bytes('12 foo')
      Traceback (most recent call last):
          ...
      ValueError: can't interpret '12 foo'
    """
    init = s
    num = ""
    while s and s[0:1].isdigit() or s[0:1] == '.':
        num += s[0]
        s = s[1:]
    num = float(num)
    letter = s.strip()
    for _, sset in SYMBOLS.items():
        if letter in sset:
            break
    else:
        if letter == 'k':
            # treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
            sset = SYMBOLS['customary']
            letter = letter.upper()
        else:
            raise ValueError("can't interpret %r" % init)
    prefix = {sset[0]: 1}
    for i, s in enumerate(sset[1:]):
        prefix[s] = 1 << (i + 1) * 10
    return int(num * prefix[letter])


def check_list_intersection(list1, list2):
    """Return True if two lists have intersection,
    otherwise False"""
    if list1 is None or list2 is None:
        return False
    return len(set(list1).intersection(set(list2))) != 0


def user_confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s/%s] ' % (prompt, 'Y', 'n')
    else:
        prompt = '%s [%s/%s]  ' % (prompt, 'y', 'N')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

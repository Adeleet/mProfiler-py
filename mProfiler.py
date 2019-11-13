import re
from time import time
from string import ascii_letters, printable

INVALID_CHARS = [")", "(", "\"", "'", "\t", "\n", "\r", "=", ","]


class mProfiler:
    def __init__(self):
        self.start_time = time()
        self.breakpoints = {}

    def start_breakpoint(self, name, auto_stop=True):
        """
        Initializes a breakpoint to start timing code.

        Args:
            name (str) : unique identifier of the block of code.
            auto_stop (bool) : whether to stop this breakpoint automatically (True)
                or continue until an end_breakpoint for this name is called.
        """
        if not type(name) == str:
            raise ValueError(
                f"Argument 'name' should have type 'str', found: {type(name)}")
        if any(c in name for c in INVALID_CHARS):
            raise ValueError(
                f"Argument 'name' cannot contain any '(' or ')', found: {name}")
        if not type(auto_stop) == bool:
            raise ValueError(
                f"Argument 'auto_stop' should have type 'bool', found {type(auto_stop)}")
        if name in self.breakpoints.keys():
            raise ValueError(
                f"Breakpoint with name {name} already exists, please call .reset_breakpoint if you wish to reset this breakpoint.")
        for existing_name in self.breakpoints.keys():
            breakpoint = self.breakpoints[existing_name]
            if breakpoint["auto_stop"]:
                self.end_breakpoint(existing_name)
        self.breakpoints[name] = {
            "init_time": time(),
            "start": time(),
            "auto_stop": auto_stop
        }

    def end_breakpoint(self, name):
        """
        Ends a breakpoint, stopping its counter and calculates it duration

        Args:
            name (str) : identifier of breakpoint to stop
        """
        if not type(name) == str:
            raise ValueError(
                f"Argument 'name' should have type 'str', found {type(name)}")
        if not name in self.breakpoints.keys():
            raise ValueError(
                f"Breakpoint with name {name} does not exist.")
        breakpoint = self.breakpoints[name]
        end_time = time()
        breakpoint["end"] = end_time
        breakpoint["total_duration"] = end_time - breakpoint["init_time"]

    def breakpoint_step(self, name):
        """
        Restarts a breakpoint, calculating its duration and restarting its counter.

        Args:
            name (str) : identifier of breakpoint to restart
        """
        if not type(name) == str:
            raise ValueError(
                f"Argument 'name' should have type 'str', found {type(name)}")
        if not name in self.breakpoints.keys():
            raise ValueError(
                f"Breakpoint with name {name} does not exist.")
        breakpoint = self.breakpoints[name]
        duration_step = time() - breakpoint["start"]
        if "durations" in self.breakpoints[name].keys():
            breakpoint["durations"].append(duration_step)
        else:
            breakpoint["durations"] = [duration_step]
        breakpoint['start'] = time()

    def end(self):
        """
        Ends profiler, displaying all summary statistics
        """
        total_duration = time() - self.start_time
        print(f"Total duration: {total_duration}s\n")
        for name in self.breakpoints.keys():
            breakpoint = self.breakpoints[name]
            if "end" not in breakpoint.keys():
                self.end_breakpoint(name)
            if "durations" in breakpoint.keys():
                mean_duration = sum(
                    breakpoint["durations"])/len(breakpoint["durations"])
                print("{name}:\t mean: {mean_duration}")
            else:
                bp_duration = breakpoint['total_duration']
                bp_perc = 100*bp_duration/total_duration
                print(
                    "\t{}:\t {:.3f}s\t ({:.1f}%)".format(name, bp_duration, bp_perc))


current_file = __file__
regex_auto_stop = re.compile("auto_stop\s{0,1}=\s{0,1}True")


regex_name = re.compile("name\s{0,1}=\s{0,1}")

with open(file=__file__, mode="r", encoding="utf8") as file:
    SCRIPT = file.readlines()

bp_start_indices = [i for i, x in enumerate(
    SCRIPT) if "start_breakpoint(" in x]
bp_end_indices = [i for i, x in enumerate(SCRIPT) if "end_breakpoint(" in x]


def _strip_quotes_(string):
    return string.strip().replace("'", "").replace('"', '')


def _strip_kwarg_(string):
    if "=" in string:
        string = string[string.index('=')+1:]
    return _strip_quotes_(string)


def parse_line_args(line):
    args_start = line.index("start_breakpoint(")
    args_end = line.index(")")
    args_substr = line[args_start+17:args_end].split(",")
    args_substr = args_substr
    args = {}
    if len(args_substr) == 1:  # only required arg will be name
        args["name"] = _strip_quotes_(args_substr[0])
        args["auto_stop"] = True
    else:
        args["name"] = _strip_kwarg_(args_substr[0])
        arg_auto_stop = _strip_kwarg_(args_substr[1])
        if "False" in arg_auto_stop:
            args["auto_stop"] = False
        else:
            args["auto_stop"] = True
    return args


def parse_profiler_name(neglect_before_line=175):
    """
    Returns profiler name, and index of __init__ and end calls

    Args:
        neglect_before_line (int, optional) : neglect lines before this number
    """
    init_index = [i for i, x in enumerate(
        SCRIPT) if "mProfiler()" in x and i >= neglect_before_line-1][0]
    name = SCRIPT[init_index].split("=")[0].strip()
    end_index = [i for i, x in enumerate(
        SCRIPT) if f"{name}.end()" in x][0]

    return (name, init_index+1, end_index+1)


profiler_name, profiler_start_index, profiler_end_index = parse_profiler_name()
breakpoint_code = {}
for i, line_num in enumerate(bp_start_indices):
    line = SCRIPT[line_num]
    if line_num < 168 or "self" in line:
        continue
    args = parse_line_args(line)
    name, auto_stop = args["name"], args["auto_stop"]
    if auto_stop:
        if i+1 < len(bp_start_indices):
            next_line_num = bp_start_indices[i+1]
        else:
            next_line_num = profiler_end_index
        breakpoint_code[name] = SCRIPT[line_num+1:next_line_num-1]
    else:
        pass

for name, code in breakpoint_code.items():
    code = "".join(code)
    print(f"{name}\n\n{code}" + "\n"*5)

# profiler = mProfiler()
# profiler.start_breakpoint("Test1")
# start code here for Test1!

    # sdfksjflsjfdljsf

# end code here for Test1!
# profiler.start_breakpoint("Test2")
# start code here for Test2!

    # sdfksjflsjfdljsf

# end code here for Test2!
# profiler.end()

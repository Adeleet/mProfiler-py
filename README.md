# mProfiler-python
Python time profiler with automatic parsing of .py files


## Todo
- Automatic parsing of .py file to extract and display code blocks that were profiled in summary.
  - __[DONE]__ Parse ```start_breakpoint()``` args (name, auto_stop)
  - __[NOT STARTED]__ Extract code snippets using ```start_breakpoint()``` args (if ```auto_stop=False```, verify that there is a ```stop_breakpoint()``` with same name and get its index. If ```auto_stop=True```, get the next ```start_breakpoint()``` or if there are none further, ```mProfiler.end()```.
  - __[NOT STARTED]__ Write tests for parsing args 
    - lines with comments, difficult to parse names
    - multiple calls to ```mProfiler.__init__()``` or  ```mProfiler.end()```.
  - __[NOT STARTED]__ Develop class ```BreakPoint``` to replace breakpoint dicts
    - Args: ```name``` and ```loop```. Use ```loop``` arg to differentiate between code that should be timed once (statement) vs. code that is repeated (loop, if/else, etc.). For loop breakpoints, additional calculations are necessary (mean, std, max, etc.)
  - __[NOT STARTED]__ Write Class documentation for ```mProfiler``` and ```BreakPoint```
  - __[NOT STARTED]__ Prettier/readable summary statistics 
    - Formatting (horizontally/vertically aligned, display more statistics)
    - RGB color output in terminal
    - Save to `txt`, `csv`, `json`, etc.
  - __[NOT STARTED]__ Parse .py code to automatically insert breakpoints
    - Insert before each line, group indented (loops or ':') lines together.
    - Create and then run a new ```mProfiler__[scriptName]__.py``` with these inserted lines.
    - Calculate times and remove irrelevant/insignificant lines/blocks.
    - Display relevant lines/blocks of code (e.g. >5% ) 
    - Transform into function/method with ```threshold_percentage``` argument to specify above which to display code lines/blocks.


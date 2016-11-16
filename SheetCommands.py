## Komsjer's csv command generator.
## @Komsjer, Komsjer@kpnmail.nl
## Feel free to edit and use this filter however you like, just attribute me some credit yo.

## Also TexelElf is pretty great. I used his code as an example. http://elemanser.com/filters.html
from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from pymclevel import MCSchematic
import StringIO
import inspect
import math
import csv
import re
import os
import sys

displayName = "SheetCommands"

inputs = (
  ("Uses:\nFILEPATH\FILENAME.csv for a single file\nGOOGLESHEET_URL to load a google sheet\n*make sure the sheet is public","label"),
  ("csv_file", ("string","value=C:\\")),
  ("                     - made by Komsjer\n                              - Komsjer@kpnmail.nl\n","label"),
)

def csv_from_url(url):
    import urllib2
    spreadsheet_id = re.findall(r"/([\s\S]*?)/", url)
    spreadsheet_id = max(spreadsheet_id, key=len)
    spreadsheet_grid_id = re.findall(r"gid=(\d+)", url)[0]
    url = "https://docs.google.com/spreadsheets/d/"+spreadsheet_id+"/export?format=csv&id="+spreadsheet_id+"&gid="+spreadsheet_grid_id
    header = {"User-Agent": 'MCSheetLoader'}
    req = urllib2.Request(url, headers = header)

    f = urllib2.urlopen(req)
    return f.read()

def text_to_bool(text):
    if text.lower() == "false" or text == "0":
	return False
    else:
	return  True

# returns a schematic commandblock TileEntitie tag, code from "ToSummonCommand.py" by TexelElf
def CommandBlock(x,y,z,command, auto = False):
	cmd = TAG_Compound()
	cmd["x"] = TAG_Int(x)
	cmd["y"] = TAG_Int(y)
	cmd["z"] = TAG_Int(z)
	cmd["id"] = TAG_String("Control")
	cmd["Command"] = TAG_String(command)
	cmd["TrackOutput"] = TAG_Byte(0)
	cmd["auto"] = TAG_Byte(1 if auto else 0)
	return cmd

class SheetCommandsLoader:
    def __init__(self, csv_filepath):
        self.global_values = {}
        self.chain_values = []
        self.exceptions = {}
        self.command_block = {"main":[{"COMMAND":"Your sheet is missing a command chain."}]}

        self.output = []

        self.programhead = 0
        self.c = 5
        self.program = ["main"]

        self.linereaders = {} #name:[head_function_name, evaltarget]

        self.filter = {} # {var_name:{target_value:replacement}}
        
        self.output = self.read(csv_filepath)


    def load_csv(self, csv_filepath):
        if os.path.isfile(csv_filepath) and csv_filepath.endswith(".csv"):
            print "--PARSING SINGLE FILE--"
            f = open(csv_filepath,"rb")
            return f
        elif "https://" in csv_filepath:
            print "--Loading google doc--"
            csv_string =  csv_from_url(csv_filepath)
            f = StringIO.StringIO(csv_string)
            return f
        else:
            raise Exception("Could not open: ",csv_filepath)

    def get_command_chain(self):
        return self.command_block["main"]

    def read_row_to_var(self, variables, row):
        var_chain = {}
        for n,var in enumerate(variables):
            if n == 0: continue
            if var != "":
                var_chain.update({var:row[n]})
        return var_chain

    def get_dimensions(self):
        x= len(max(self.command_block.values(), key = lambda x: len(x) if type(x)==list else 0))##TODO calculate the max of all the outputs instead of over command_block because of *EXCEPTIONS
        y= 1 + self.output.count("NEWLINE")
        def countz (out):
            z_max = 0
            c_max = 0
            for o in out:
                c_max += 1
                z_max = c_max if c_max > z_max else z_max
                if o == "NEWLINE":
                    c_max = 0
            return z_max
        z= countz(self.output)
        
        return (x,y,z)

    def next_program_step(self,target = None):
        if target != None: self.programhead = target
        if len(self.program) == 0: self.program = ["main"]
        if self.programhead >= len(self.program): self.programhead = 0
        op = self.program[self.programhead]
        self.programhead += 1
        return op

    def add_linereader(self,name,target,code):
        self.linereaders.update({name:[target,code]})

    def call_linereader(self, name, row, output):
        out = None
        if name in self.linereaders:
            reader = self.linereaders[name]
            try:
                exec(reader[1])
                func = eval(reader[0])
                out = func(self,row, output)

            except:
                e = sys.exc_info()
                raise Exception(e)
        else:
            print "!CALLED UNDIFINED LINE READER: "+ str(name)
        return out
        
    def read(self, csv_filepath):
        csv_file = self.load_csv(csv_filepath)
        print type(csv_file)
        reader = csv.reader(csv_file)
        output = []
        _default_operator = "IGNORE"
        #GLOBAL
        _global_new_vars = []
        #COMMANDS
        _command_vars = []
        _command_chain = []
        #START
        _is_reading = False
        _reading_vars = []
        #FILTER
        _filter_vars = []
        _filter_targets = []
        
        
        for row in reader:
            _line_complete = False
            operator = str(row [0]) if str(row [0]) != "" else _default_operator
            while not _line_complete:
                _line_complete = True
                if operator == "RUN":
                    operator = self.next_program_step()
                if operator.startswith("GOTO"):
                    commands = operator.split(" ")
                    readhead_target = int(commands[1]) if len (commands) >= 2 else 0
                    operator = self.next_program_step(readhead_target)
                    _line_complete = False
                    if not (text_to_bool(commands[2]) if len (commands) >= 3 else True):
                        _line_complete = True
                    continue
                print operator

                if operator == "PARENT":
                    p_out = self.read(row[1])
                    output += p_out
                
                if operator == "PROGRAM":
                    _default_operator = "PROGRAMREAD"
                    self.program = []
                elif operator == "PROGRAMREAD":
                    self.program.append(row[1])
                elif operator == "PROGRAMEND":
                    _default_operator = "IGNORE"
                elif operator == "GLOBAL":
                    _global_new_vars = row
                    _default_operator = "GLOBALREAD"
                    continue
                elif operator == "COMMANDS":
                    _command_vars = row
                    _reading_command_chain = True
                    _default_operator = "COMMANDSREAD"
                    _command_chain = []
                    continue
                elif operator == "COMMANDSEND":
                    block_name = row[1].lower() if row[1].lower() != "" else "main"
                    self.command_block.update({block_name :_command_chain})
                    print "LOADED COMMAND CHAIN: ",row[1] ,":",_command_chain
                    _command_vars = []
                    _command_chain = []
                    continue
                elif operator == "START":
                    _is_reading = True
                    _reading_vars = row
                    self.programhead = 0
                    _default_operator = "RUN"
                    continue
                elif operator == "END":
                    _reading_vars = []
                    _default_operator = "IGNORE"
                    continue
                elif operator == "BLANK":
                    output.append("BLANK")
                    continue
                elif operator == "ENDB":
                    _reading_vars = []
                    output.append("BLANK")
                    _default_operator = "IGNORE"
                    continue
                elif operator == "IGNORE":
                    continue
                elif operator == "GLOBALREAD":
                    variables = self.read_row_to_var(_global_new_vars, row)
                    self.global_values.update(variables)
                    print "LOADED GLOBAL VARS: ", variables
                    _global_new_vars = []
                    _default_operator = "IGNORE"
                    continue
                elif operator == "COMMANDSREAD":
                    variables = self.read_row_to_var(_command_vars, row)
                    _command_chain.append(variables)
                    continue

                elif operator == "FILTER":
                    _filter_vars = row
                    _default_operator = "FILTERFROM"
                elif operator == "FILTERFROM":
                    _filter_targets = row
                    _default_operator = "FILTERTO"
                elif operator == "FILTERTO":
                    _filter_vars = _filter_vars[1:]
                    _filter_targets = _filter_targets[1:]
                    _filter_replacements = row[1:]
                    for n in range(len(_filter_vars)):
                        if _filter_vars[n] != "":
                            if _filter_vars[n] in self.filter:
                                self.filter[_filter_vars[n]].update({_filter_targets[n]:_filter_replacements[n]})
                            else:
                                self.filter[_filter_vars[n]] = {_filter_targets[n]:_filter_replacements[n]} # {var_name:{target_value:replacement}}
                    _filter_vars = []
                    _filter_targets = []
                elif operator == "LOCAL":
                    _reading_vars = row
                elif operator == "HALT":
                    return output
                elif operator.startswith("REPEAT"):
                    _default_operator = operator.split(" ",1)[1]
                elif operator == "NEWLINE":
                    output.append("NEWLINE")
                    
                elif operator == "DEFLINEREADER":
                    self.add_linereader(row[1],row[2],row[3])
                elif operator.startswith("LINEREADER"):
                    commands = operator.split(" ")
                    target = commands[1] if len(commands)>=2 else "EMPTY"
                    out = self.call_linereader(target,row,output)
                        
                elif operator in self.command_block:
                    variables = self.read_row_to_var(_reading_vars, row)
                    output.append( self.output_chain(variables,operator))
                    continue
                
                
        return output
        
                        
    def log(self):
        print "Generating {0} rows of commandblocks".format(self.chain_values)

    def format_command(self, row_vars, command_text):
        temp = lambda matchobj: self.get_var(matchobj.group(1), row_vars, just_value=True)
        command_text = re.sub(r"%([\s\S]*?)%",temp, command_text)
        return command_text
        

    def get_var(self, var_name, row_vars=None,ignore_link=False,just_value=False, soft=False):
        ## Use Ignore link for command! TODO
        ## TODO add a *IGNORE for row_vars so it can grab the global value
        var = {var_name:""}
        if var_name in row_vars:
            var[var_name] = row_vars[var_name]
        else:
            if soft:
                return {}
            else:
                var[var_name] = "!UNKNOWN VARIABLE REQUESTED!"
                print "!UNKNOWN VARIABLE REQUESTED: \""+str(var_name)+"\""
                
        if just_value : return var[var_name]

        ##EVAL all variables with Eval token
        if not soft:
            for v in var:
                var[v] = self.format_command(row_vars, var[v])
        ## special name opperands

        _base_var_name = ""
        for n,op in enumerate( var_name.split(" ") ):
            
            if n == 0:
                _base_var_name = op
            
            if op.startswith("*split=") : # split the variable and assign it to _base_var_name+n
                other = op.replace("*split=", "", 1)
                sep_vars = var[var_name].split(other)
                var.update({str(_base_var_name)+str(n+1):new_var for n,new_var in enumerate(sep_vars)})
        return var

    def resolve(self,data, soft = False):
        new_data_h={}
        for key in data.keys():
            new_data_h.update(self.get_var(key,data, soft=soft))
##            if "Line_green_ *split=/" in new_data_h:
##                if "Line_green_1" in new_data_h:
##                    print new_data_h["Line_green_1"]
        return new_data_h

    def vars_from_exceptions(self, exceptions):
        exceptions = exceptions.split("\n")
        variables = {}
        for e in exceptions:
            e = e.split("=",1)
            if len(e) == 2:
                variables[e[0]] = e[1]
        return variables

    def filter_vars(self,row_vars):
        for var in row_vars:
            if var in self.filter:
                if row_vars[var] in self.filter[var]:
                    row_vars[var] = self.filter[var][row_vars[var]]
        return row_vars
    def get_full_data(self, row_vars, base={}):
        new_data_h = {}
        # Base needed variables TODO MOVE TO GLOBAL PRE SET
        new_data_h.update(base)
        # global based variables
        new_data_h.update(self.global_values)
        # Row based variables
        row_vars_soft_r = self.resolve(row_vars, True)
        new_data_h.update(row_vars)
        new_data_h.update(row_vars_soft_r)
        # Filer
        new_data_h = self.filter_vars(new_data_h)
        # Exception varialbes
        if "EXCEPTION" in new_data_h:
            if new_data_h["EXCEPTION"] != "":
                new_data_h.update(self.vars_from_exceptions(new_data_h["EXCEPTION"]))
                #new_data_h.update(self.resolve(new_data_h))
                if new_data_h["ID"] == "19":
                    print "EXCEPTION: ",new_data_h["EXCEPTION"]
            
        new_data_h.update(self.resolve(new_data_h))
        return new_data_h

    def output_chain(self, row_vars, command_chain_name = "main"):
        command_chain = self.command_block[command_chain_name]
        resolved_chain = []
        base = {"BLOCKID":"137", "COMMAND":"", "META":"5", "ISAUTO":"FALSE"}
        for link in command_chain: ##TODO add row_vars to link so a row can edit the command
            link.update(row_vars)
            data = self.get_full_data(link,base) ##TODO Move outside and put low priority on link but still update
            #print data
            #print "Line_green_1" in data
            resolved_chain.append({"BLOCKID":data["BLOCKID"], "COMMAND":self.format_command(data,data["COMMAND"]), "META":data["META"], "ISAUTO":data["ISAUTO"]})
            #print t["COMMAND"]
        return resolved_chain
        
        
        

def generate(dialog, schematic):
    y = 0
    xd = 0
    zd = 0
    _xd = 0
    _zd = 0
    for z, row in enumerate(dialog.output):
        _zd = z
        if row == "BLANK":
            pass
        elif row == "NEWLINE":
            y+=1
            xd = _xd
            zd = _zd+1
            #print "BLANK"
        elif type(row) == list:
            for x, command_data in enumerate(row):
                _xd = x
                if type(command_data) == dict:
                    BLOCKID = int(command_data["BLOCKID"])
                    COMMAND = str(command_data["COMMAND"])
                    META = int(command_data["META"])
                    ISAUTO = text_to_bool( command_data["ISAUTO"] )
                    schematic.setBlockAt(x-xd,y,z-zd,BLOCKID)
                    schematic.setBlockDataAt(x-xd,y,z-zd, META)
                    schematic.TileEntities.append(CommandBlock(x-xd,y,z-zd,COMMAND,ISAUTO))
                    #print BLOCKID,COMMAND,META,ISAUTO
        
        

                
def perform(level, box, options):
    #Gets the editor, taken from code by TexelElf
    editor = inspect.stack()[1][0].f_locals.get('self', None).editor

    #--Options
    csv_file = options["csv_file"]

    #--Run
    dialog = SheetCommandsLoader(csv_file)
    schematic = MCSchematic(dialog.get_dimensions(), mats=level.materials)
    generate(dialog,schematic)

    #Copies the schematic to the editor, taken from code by TexelElf
    editor.addCopiedSchematic(schematic)

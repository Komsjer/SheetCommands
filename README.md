#SheetCommands

##Current operands

####RUN
- Runs the next iteration of the program

####PROGRAM
- empties the program array
- sets the default operand to PROGRAMREAD

####PROGRAMREAD
- reads row[1] to the program array

####PROGRAMEND
- sets the default operand to IGNORE

####GLOBAL
- sets the succeeding row values as global variable names
- sets the default operand to GLOBALREAD

####GLOBALREAD
- stores the succeeding global variables with their respective names defined by GLOBAL
- sets the default operand to IGNORE

####COMMANDS
- sets the succeeding row values as commandchain variable names
- sets the default operand to COMMANDSREAD

####COMMANDSREAD
- adds a row of variable data to a commands array

####COMMANDSEND
- stores the preseeding commands variable data to a commandchain
- the name of this chain is taken from row[1]
- sets the default operand to IGNORE

####START
- sets the succeeding row values as local variable names
- sets the default operand to RUN

####END
- empties local variable names
- sets the default operand to IGNORE

####IGNORE
- continues to the next row

####BLANK
- adds a blank row to your output

####ENDB
- runs END and BLANK

####PARENT
- adds all the rows found in the file specified into itself
- it reads row[1] for the file location

####[commandchain name]
- runs this commandchain and adds it to the output using the succeeding local variables with their respective names.

##Planned opperands

####GOTO [N=0] [readline=true]
- moves the readhead of the function to a location [N]
- if readline: reads that line with the program found at program[N]

####FILTER
- sets the succeeding row values as filter variable names
- sets the default operand to FILTERFROM

####FILTERFROM
- sets the value to look for when updating other variables
- sets the default operand to FILTERTO

####FILTERTO
- sets the value to replace the -from- instances of the given variable with
- sets the default operand to IGNORE

####REPEAT [target]
- sets the default operand to [target]

####LOCAL
- sets the succeeding row values as local variable names

####HALT
- stops reading anything afther this

####NEWLINE
- Stacks the commandblocks into a new line

####DEFLINEREADER
- write your own linereader
- where row[1] is the linereaderName
- where row[2] is the target function name
- where row[3] is the line reader function

####LINEREADER [linereaderName]
- calls [linereaderName] for that line



####CONDITION [condition name] {parm1} {...} {parmN} *maybe
- a way to call different functions based on contidions

####DEFCONDITION *maybe
- write your own conditional



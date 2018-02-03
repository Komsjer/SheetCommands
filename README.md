
# SheetCommands

SheetCommands is an MCEdit filter made for turning csv data into commandblock chains. Its aim is to make large scale commandblock setups managable. Aswell as provide easy to use yet versatile tools to allow the user to both employ rapid prototyping aswell as beeing able to easily share their creations with others. 

SheetCommands can load csv data straight from googlesheet links. aswell as .csv files

[-RefrenceGuide-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=0 "Basics Sheet")


## Operands:

#### RUN [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1852566837 "Run Sheet")
- Runs the next iteration of the program

#### PROGRAM [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1497223223 "Program Sheet")
- empties the program array
- sets the default operand to PROGRAMREAD

#### PROGRAMREAD [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1497223223 "Program Sheet")
- reads row[1] to the program array

#### PROGRAMEND [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1497223223 "Program Sheet")
- sets the default operand to IGNORE

#### GLOBAL [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=667247320 "ValueRefrence Sheet")
- sets the succeeding row values as global variable names
- sets the default operand to GLOBALREAD

#### GLOBALREAD [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=667247320 "ValueRefrence Sheet")
- stores the succeeding global variables with their respective names defined by GLOBAL
- sets the default operand to IGNORE

#### COMMANDS [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1089643559 "Commands Sheet")
- sets the succeeding row values as commandchain variable names
- sets the default operand to COMMANDSREAD

#### COMMANDSREAD [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1089643559 "Commands Sheet")
- adds a row of variable data to a commands array

#### COMMANDSEND [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1089643559 "Commands Sheet")
- stores the preseeding commands variable data to a commandchain
- the name of this chain is taken from row[1]
- sets the default operand to IGNORE

#### START [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=0 "Basics Sheet")
- sets the succeeding row values as local variable names
- sets the default operand to RUN

#### END [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=0 "Basics Sheet")
- empties local variable names
- sets the default operand to IGNORE

#### IGNORE [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=972831184 "Ignore  Sheet")
- continues to the next row

#### BLANK [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=403804994 "Blank  Sheet")
- adds a blank row to your output

#### ENDB [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=403804994 "Blank  Sheet")
- runs END and BLANK

#### PARENT [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1875644597 "Parent  Sheet") [-Other-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=366900301 "Parented  Sheet")
- adds all the rows found in the file specified into itself
- it reads row[1] for the file location

#### [commandchain name] [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1089643559 "Commands Sheet")
- runs this commandchain and adds it to the output using the succeeding local variables with their respective names.

#### GOTO [N=0] [readline=true] [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=907582265 "Goto  Sheet")
- moves the readhead of the function to a location [N]
- if readline: reads that line with the program found at program[N]

#### FILTER [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1030226065 "Filter  Sheet")
- sets the succeeding row values as filter variable names
- sets the default operand to FILTERFROM

#### FILTERFROM [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1030226065 "Filter  Sheet")
- sets the value to look for when updating other variables
- sets the default operand to FILTERTO

#### FILTERTO [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1030226065 "Filter  Sheet")
- sets the value to replace the -from- instances of the given variable with
- sets the default operand to IGNORE

#### LOCAL [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=663961964 "Local  Sheet")
- sets the succeeding row values as local variable names

#### REPEAT [target] [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1407297482 "Repeat  Sheet")
- sets the default operand to [target]

#### HALT [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=1602113219 "Halt  Sheet")
- stops reading anything afther this

#### NEWLINE [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=345526504 "Newline  Sheet")
- Stacks the commandblocks into a new line

#### DEFLINEREADER
- write your own linereader
- where row[1] is the linereaderName
- where row[2] is the target function name
- where row[3] is the line reader function

#### LINEREADER [linereaderName]
- calls [linereaderName] for that line

## Other Sheets:

#### EXCEPTION HANDLING [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=770940968 "Exception  Sheet")

#### DATA SPLITTING [-Sheet-](https://docs.google.com/spreadsheets/d/1ylzSjWcWe-uwC6NFYCk3W4kxFod8NVA_7ZvtQkXue8k/edit#gid=563084852 "Splitting  Sheet")

# BedrockScript
BedrockScript is a DSL I created to make writing commands in Minecraft: Bedrock Edition more efficient. This project is for me to learn more about compilers and some concepts of Computer Science.

## What it Does
The compiler will take an input written in a C-like syntax and outputs Minecraft commands. This can be helpful for repetitive and tedious processes like evaluating expressions from scoreboard objectives.

## Usage
Run ```main.py``` with an input file being its first argument. The input file must end with an extension of ```.mcbs```. You can also convert it to an executable using tools like PyInstaller to make it more compact.

## Syntax
BedrockScript uses a C-like syntax with curly braces to define a code block. Below are the grammar rules along with examples.
1. Functions ```def <funciton name> {}```
   Firstly, we have to define a funcion with the ```def``` keyword. Since we cannot add arguments to Minecraft functions or commands, we don't have to write any parenthesis here.
```
def myFunction {}
```

2. Execute ```execute```
   Command segment is the segment you put after writing an execute command, e.g. ```execute as @a run ...``` <- ```as @a``` is the command segment.
```
execute (<command segment>) {
  command 1;
  command 2;
  ...
  command n;
}
```

3. Commands
   If the compiler does not recognize a keyword, it will assume it is a command until it finds a semi-colon (```;```). Below is an example.
```
def main {
  say hello;
  tp @a ~~~;
}
```

4. Scorebaords
   This part is a bit unique. We can assign a target's value ```<Target>``` to a scoreboard objective ```<SCRBObj>``` by using the following synax:
```
<Target>.<SCRBObj> = <expression>;
```
Example:
```
@a.timer = 0;
@e[name="Bob"].wins = 2 + @e[name="Alic",c=1].loss;
```

## Additional Info
The first command it will generate is to declare a scoreboard objective with name ```__NUMBER__```. This is to store numeric values for scoreboard operations. If you find that this is redundant, you can choose to ignore it.

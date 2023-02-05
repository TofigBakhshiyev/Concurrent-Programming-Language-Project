# Concurrent Programming Language Project 2023
This program creates a new window when url entered or multiple urls entered and program works concurrently with threads, first program downloads html contents concurrently and creates the window because it is not thread safe to create a window in a thread
#### Requirments and packages
- Windows 10 OS
- PyQt5 `pip install PyQt5`
- Python 3.11.1 
- requests `pip install requests`

#### Demo Video
[!(Demo)](https://github.com/TofigBakhshiyev/Concurrent-Programming-Language-Project/blob/main/Demo.webm)

 
#### Example Urls for testing
`https://medium.com/` <br>
`https://github.com/TofigBakhshiyev` <br>
`https://courses.cs.ut.ee/` <br>

Two urls in same time example <br>
`https://medium.com/ https://courses.cs.ut.ee/`
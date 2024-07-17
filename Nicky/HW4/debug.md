Issue :Add the required request lines to find-anagrams.sub file
cd into MECH-892/OSPool_workflow/lecture-7/troubleshooting/
type nano troubleshooting
add the required request line
click on control O enter and then control X to exit
 "cat" troubleshooting to see the changes.
The results would appear like this: 
executable = find_anagrams.py
arguments = p098_words.txt

request_memory = 1GB
request_cpus = 1
request_desk = 1TB
transfer_input_files = p098_words,txt

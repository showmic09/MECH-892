---
ospool:
    path: software_examples/python/tutorial-wordfreq/README.md
---

# Wordcount Tutorial for Submitting Multiple Jobs

Imagine you have a collection of books, and you want to analyze how word usage 
varies from book to book or author to author. The type of workflow covered in 
this tutorial can be used to describe workflows that take have different input 
files or parameters from job to job.

To download the materials for this tutorial, type:

	$ git clone https://github.com/OSGConnect/tutorial-wordfreq

## Analyzing One Book

### Test the Command

We can analyze one book by running the `wordcount.py` script, with the 
name of the book we want to analyze: 

	$ ./wordcount.py Alice_in_Wonderland.txt 

If you run the `ls` command, you should see a new file with the prefix `counts`
which has the results of this python script. This is the output we want to 
produce within an HTCondor job. For now, remove the output: 

	$ rm counts.Alice_in_Wonderland.tsv

### Create a Submit File

To submit a single job that runs this command and analyzes the 
Alice's Adventures in Wonderland book, we need to translate this command 
into HTCondor submit file syntax. The two main components we care about 
are (1) the actual command and (2) the needed input files. 

The command gets turned into the submit file `executable` and `arguments` options: 

	executable = wordcount.py
	arguments = Alice_in_Wonderland.txt	

The `executable` is the script that we want to run, and the `arguments` is 
everything else that follows the script when we run it, like the test above.
The input file for this job is the `Alice_in_Wonderland.txt` 
text file. While we provided the name as in the `arguments`, we need
to explicitly tell HTCondor to transfer the corresponding file.
We include the file name in the following submit file option: 

	transfer_input_files = Alice_in_Wonderland.txt

There are other submit file options that control other aspects of the job, like 
where to save error and logging information, and how many resources to request per 
job. 

This tutorial has a sample submit file (`wordcount.sub`) with most of these submit file options filled in: 

	$ cat wordcount.sub
	executable = 
	arguments = 
	
	transfer_input_files = 
	
	should_transfer_files   = Yes
	when_to_transfer_output = ON_EXIT
	
	log           = logs/job.$(Cluster).$(Process).log
	error         = logs/job.$(Cluster).$(Process).error
	output        = logs/job.$(Cluster).$(Process).out
	
	+JobDurationCategory = "Medium"
	requirements   = (OSGVO_OS_STRING == "RHEL 7")
	
	request_cpus   = 1
	request_memory = 512MB
	request_disk   = 512MB
	
	queue 1   

Open (or create) this file with a terminal-based text editor (like `vi` or `nano`) and 
add the executable, arguments, and input information described above. 

### Submit and Monitor the Job

After saving the submit file, submit the job: 

	$ condor_submit wordcount.sub

You can check the job's progress using `condor_q`, which will print out the status of 
your jobs in the queue.  You can also use the command `condor_watch_q` to monitor the
queue in real time (use the keyboard shortcut `Ctrl` `c` to exit). Once the job finishes, you 
should see the same `counts.Alice_in_Wonderland.tsv` output when you enter `ls`.

## Analyzing Multiple Books

Now suppose you wanted to analyze multiple books - more than one at a time. 
You could create a separate submit file for each book, and submit all of the
files manually, but you'd have a lot of file lines to modify each time
(in particular, the `arguments` and `transfer_input_files` lines from the 
previous submit file). 

This would be overly verbose and tedious. HTCondor has options that make it easy to 
submit many jobs from one submit file. 

### Make a List of Inputs

First we want to make a list of inputs that we want to use for our jobs. This 
should be a list where each item on the list corresponds to a job. 

In this example, our inputs are the different text files for different books. We 
want each job to analyze a different book, so our list should just contain the 
names of these text files. We can easily create this list by using an `ls` command and 
sending the output to a file: 

	$ ls *.txt > book.list 

The `book.list` file now contains each of the `.txt` file names in the current directory.

	$ cat book.list
	Alice_in_Wonderland.txt
	Dracula.txt
	Huckleberry_Finn.txt
	Pride_and_Prejudice.txt
	Ulysses.txt

### Modify the Submit File

Next, we will make changes to our submit file so that it submits a job for 
each book title in our list (seen in the `book.list` file). 

Create a copy of our existing submit file, which we will use for this job submission. 

	$ cp wordcount.sub many-wordcount.sub

We want to tell the `queue` keyword to use our list of inputs to submit jobs. 
The default syntax looks like this: 

 	queue <item> from <list> 

Open the `many-wordcount.sub` file with a text editor and go to the end. 
Following the syntax above, we modify the `queue` statement to fit our example: 

	queue book from book.list 

This statement works like a `for` loop. For every item in the `book.list` 
file, HTCondor will create a job using this submit file but replacing every
occurrence of `$(book)` with the item from `book.list`. 

> The syntax `$(variablename)` represents a submit variable whose value
> will be substituted at the time of submission.

Therefore, everywhere we used the name of the book in our submit file should be
replaced with the variable `$(book)` (in the previous example, everywhere you entered
"Alice_in_Wonderland.txt"). 

So the following lines in the submit file should be changed to use the variable `$(book)`: 

	arguments = $(book)
	
	transfer_input_files = $(book)

### Submit and Monitor the Job

We're now ready to submit all of our jobs. 

	$ condor_submit many-wordcount.sub

This will now submit five jobs (one for each book on our list). Once all five 
have finished running, we should see five "counts" files, one for each book in the directory. 

If you don't see all five "counts" files, consider investigating the log files and see if
you can identify what caused that to happen.

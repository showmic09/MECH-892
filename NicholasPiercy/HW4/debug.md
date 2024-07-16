# To solve the issue of submitting a file with a large quantity of words for use with the Anagram finding
# function, as opposed to submitting many smaller jobs using subsets of the words contained in teh large
# file, I propose thw following workflow:

#1. At the submit/access node, create a folder named /input.
#2. Write and run a script which separates the single input file into input files of a desired size
#   (separate by line).
#3. Submit the job to htc_condor and queue the input files such that only the input file for each 
#   specific job is transferred for that job (minimizes useless copy/tranfer of data.
#4. Make sure to combine all of the outputs into a single output folder on the access node. 
#5. Concatenate the results before transfering to the local machine.

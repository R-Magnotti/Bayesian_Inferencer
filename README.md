# Bayesian_Inferencer

The XML files are updated and formatted and are provided in the 'src' folder, please use those instead of the original XML files.

Instructions to run the code:

For Exact Inference :
-> Open terminal from the 'src' folder.
-> Enter : python BN_Driver.py filename.xml query_variable evidence

Example : python BN_Driver.py aima-alarm.xml B J True M True

(The output will also show the results of sampling , the number of samples are by default 10,000)


For Approximate Inference :
-> Open terminal from the 'src' folder.
-> Enter : python BN_Driver_Approximate.py number_of_runs filename.xml query_variable evidence

Example : python BN_Driver.py 100000 aima-alarm.xml B J True M True


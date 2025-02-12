1 I set the buffer to 32 which means if the input is too large, there may occur an error report which may be decimal error or unexpected character error. There is no error report on the overflow of input. If the input are overflowed with numbers the error report will be unexpected characters. 
2 The priority of the error report is due to the sequnence of input.
    For example, 1.2a refers to decimal error while 1a.2 refers to unexpected characters.
3 If both M and N are negtive numbers, the error report is overflow.
4 A space or an enter is recognized as an unexpected character.
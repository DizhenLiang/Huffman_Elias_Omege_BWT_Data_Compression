import sys
def read_bytes_from_bin_file(filename):
    byte_values = []  # Initialize an empty list for byte values
    with open(filename, 'rb') as file:
        for line in file:
            # Convert each line to an integer and append to the list
            byte_values.append(int(line.strip()))
    return byte_values


def bytes_to_bitstream(byte_values):
    bitstream = ''
    for byte in byte_values:
        # Convert each byte to its 8-bit binary representation and concatenate
        bitstream += format(byte, '08b')
    return bitstream


def elias_omega_decode(codeword, bits_consumed):
    pos = bits_consumed
    readlen = 1
    N = None
    bits_consumed = 0  # Initialize a counter for bits consumed

    while N is None:
        try:
            # Read substring from pos to pos + readlen
            component = codeword[pos:pos + readlen]
            
            # Check if the first bit is '1'
            if component[0] == '1':
                # Convert to integer from base of 2
                N = int(component, 2)
            else:
                # If first bit is '0', flip to '1'
                component = '1' + component[1:]
                pos += readlen
                # Convert bits into integer and extend the coverage
                readlen = int(component, 2) + 1

        except IndexError:
            # Handle the case where pos + readlen exceeds codeword length
            print("Error: Index out of range. Codeword may be incomplete.")
            break  # Exit the loop if an error occurs
    
    num_1s = readlen
    bits_consumed = pos + num_1s
    return N, bits_consumed  # Return the decoded number and bits consumed


def ascii_decode(bits):
    #convert bits base 2) into ascii character 
    ascii_char = chr(int(bits, 2))
    return ascii_char


def write_to_output(filename, res):
    """Write the lexicographic ranks to the output file."""
    with open(filename, 'w') as file:
        file.write(f"{res}\n")


def ascii_huff_set(bit_stream, bits_consumed):
    count = 0
    char = None

    while char is None:
        count+=1
        converage = bit_stream[bits_consumed:bits_consumed+count]

        #for bit_stream[bits_consumed:bits_consumed+1]
        # bit_stream[0] = bit_stream[-1]
        if converage == '0':
            char = '0'
            
        
        else:
            if converage[-1] == '0':
                char = converage
                
    
    next_start = bits_consumed+count
    return char, next_start

def huff_char_set(huff_char_set, bits_consumed, bit_stream):
    count = 0
    char = None
    while char is None:
        count+=1
        converage = bit_stream[bits_consumed:bits_consumed+count]
        char = huff_char_set.get(converage)
        
    next_start = bits_consumed + count
    return char, next_start

def rank(f_string):
    rank = {}
    #j = 0

    for i, char in enumerate(f_string):

        if char not in rank.keys():
            rank[char] = i
        

    # print("rank", rank)
    # print("n_occur", n_occur)
    return rank

def nccourence(bwt_string):
    n_occur = []

    for i in range(len(bwt_string)):
        match_count = 0
        for match_char in bwt_string[:i]:
            if match_char == bwt_string[i]:
                match_count+=1

        n_occur.append(match_count)
    return n_occur

def f_string_pos(bwt_string, rank, n_occur):
    fs_pos=[]
    for i, char in enumerate(bwt_string):
        pos = rank[char] + n_occur[i]
        fs_pos.append(pos)
    #print(fs_pos)

    return fs_pos

def q2_dec(bitstream):

    #print(bitstream)
    # Decode the bitstream
    num_chars, bits_consumed = elias_omega_decode(bitstream,0)
    uniq_chars, bits_consumed = elias_omega_decode(bitstream,bits_consumed)
    #print(bits_consumed)
    char_huff_code = {}
    #print(bitstream[0:bits_consumed])

    for i in range(uniq_chars):
        #print(bitstream[bits_consumed:bits_consumed+7])
        ascii_7_char = ascii_decode(bitstream[bits_consumed:bits_consumed+7])
        bits_consumed += 7
        #print(ascii_7_char)
        #print(bitstream[bits_consumed:bits_consumed+7])
        
        bits_huff_cons, bits_consumed = elias_omega_decode(bitstream,bits_consumed)
        #print(bits_huff_cons) 

        #huff_bits, bits_consumed = ascii_huff_set(bitstream, bits_consumed)
        coverage = bitstream[bits_consumed: bits_consumed+bits_huff_cons]
        bits_consumed += bits_huff_cons
        #print(huff_bits)
        char_huff_code[ascii_7_char] = coverage

    #print(bits_consumed)
    #print(char_huff_code)

    
    bits_char_set = {v:k for k,v in char_huff_code.items()}
    #print(bits_char_set)

    tuple_lst = []

    j = num_chars
    #print(j)
    while j > 0:
        char = None

        char, bits_consumed = huff_char_set(bits_char_set,bits_consumed,bitstream)
        #print(char)
        freq, bits_consumed = elias_omega_decode(bitstream,bits_consumed)
        #print(freq)
        #decreament j for frequency, since frequency of each chars in runlength 
        j -= freq
        tuple_lst.append((char,freq))
    
    bwt_string = ""
    

    #print(tuple_lst)
    for b in tuple_lst:
        char, freq = b
        bwt_string += char * freq
    
    F_string = sorted(bwt_string)
    #print(F_string)
    bwt_rank= rank(F_string)
    #print("rank", bwt_rank)
    bwt_noccur = nccourence(bwt_string)
    #print(bwt_noccur)

    str_pos = f_string_pos(bwt_string,bwt_rank,bwt_noccur)
    #print(str_pos)

    inverted_str = "$"
    start_index = 0
    pos = str_pos[start_index]
    inverted_str += bwt_string[0]

    while bwt_string[pos] != '$':
        l_char = bwt_string[pos]
        inverted_str += l_char
        pos = str_pos[pos]

    original_str = inverted_str[::-1]
    #print(original_str)
    
    #print(tuple_lst)

    return original_str

def main(string_filename):
    # Read the input string and positions from the files
    bytes = read_bytes_from_bin_file(string_filename)
    bitstream = bytes_to_bitstream(bytes)
    res = q2_dec(bitstream)
    #print(res)
    write_to_output('q2 decoder ouput.txt', res)  


if __name__ == "__main__":
    
    # string = "banana$"

    # bytes = read_bytes_from_bin_file("q2_encoder_output.bin")
    # bit_stream = bytes_to_bitstream(bytes)
    # q2_dec(bit_stream)

    string_filename = sys.argv[1]
    main(string_filename)


        

    




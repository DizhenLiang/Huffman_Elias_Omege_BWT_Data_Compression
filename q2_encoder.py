
import heapq, sys
from bitarray import bitarray

def huffman_tree(string):
    uni_count = 0
    freq_hash= {}

    #string = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    #
    for char in string:
        if char in freq_hash:
            freq_hash[char] += 1
        else:
            freq_hash[char] = 1
            uni_count += 1

    #minheap for most in-frequent characters
    #heap for O(log n) push and removal
    heap = [(freq_hash[char], char) for char in freq_hash]
    heapq.heapify(heap)

    huffman_hash = {}


    #Build huffman tree
    while len(heap) > 1:
        fir_char = heapq.heappop(heap)
        sec_char = heapq.heappop(heap)

        #merge least two frequent node to create new node to form huffman tree
        comb_freq = fir_char[0] + sec_char[0]

        #print(comb_freq)
        comb_char = fir_char[1] + sec_char[1]
        #print(comb_char)
        
        #huffman encode for distnict characters
        # char with smaller frequency at left always
        #for loop for left child
        for char in fir_char[1]:
            if char in huffman_hash:
                huffman_hash[char] = bitarray('0') + huffman_hash[char]
            
            else:
                huffman_hash[char] = bitarray('0')
                

        #for loop for right child
        for char in sec_char[1]:
            if char in huffman_hash:
                huffman_hash[char] = bitarray('1') + huffman_hash[char]
            
            else:
                huffman_hash[char] = bitarray('1')
                


        #reuse, since those nodes are poped out already
        heapq.heappush(heap, (comb_freq, comb_char))
    
    return heap, uni_count, huffman_hash




def naive_bwt_enc(string):
    #
    bwt_m = []
    #
    bwt_L_str = ""

    # Generate cyclic suffixed
    for i in range(len(string)):
        bwt_m.append(string[i:]+string[0:i])

    bwt_m = sorted(bwt_m)

    for j in range(len(bwt_m)):
        bwt_L_str += bwt_m[j][-1]
    
    return bwt_L_str


def bit_len(integer):
    bit_len=0

    while integer!=0:

        bit_len+=1
        #treat integer as decimal number
        integer = integer>>1
    return bit_len


def binary_representation(x):
    #print(bin(x)[2:])
    #bin function give string of binary representation
    return bin(x)[2:]  # Remove the '0b' and the leading '1'

#print(binary_representation(n))
def encode_length(length):
    #print(length)
    if length == 1:
        return ""

    else:
        #10 - 1 = 9
        length -= 1
        
        length_bin = binary_representation(length)

        if length_bin[0] == '1':
            length_bin = "0" + length_bin[1:]
            #print(length_bin)
        
        #record it before first 0 become 1 
        #otherwise wrong count
        len_count = len(length_bin)

        #print("length_bin: ", length_bin)
        return encode_length(len_count) + length_bin


def elias_omega_encode(n):
    
    N = binary_representation(n)
    L1 = len(N)
    Ln = encode_length(L1)
    return Ln + N

def run_len_enc(string):
    run_len=[]
    counter=1
    #string[0] = string[-1]
    i=-1
    #avoid index out of range
    for i in range(len(string)-1):
        if string[i]==string[i+1]:
            counter+=1
        else:
            run_len.append((string[i],counter))
            #reset counter for next character
            counter=1
    run_len.append((string[i+1],counter))

    return run_len

def get_7bit_ascii_codes(string):
    # Create a set of distinct characters
    
    # Dictionary to store the 7-bit ASCII codes
    ascii_codes = {}
    
    for char in string:
        # Get the ASCII value and convert to a 7-bit binary string
        ascii_codes[char] = format(ord(char), '07b')
    
    return ascii_codes



def elias_omega_huff_code(huffman_hash):
    elias_encoded_lengths = {}
    for char, huffman_code in huffman_hash.items():
        # Get the length of the Huffman codeword
        length_of_huffman_code = len(huffman_code)
        # Encode this length using Elias Omega encoding
        elias_encoded_length = elias_omega_encode(length_of_huffman_code)
        elias_encoded_lengths[char] = elias_encoded_length
    return elias_encoded_lengths

#4.
def runlen_huff(run_len_list, huff_hash):
    for i in range(len(run_len_list)):
        char, freq = run_len_list[i]
        run_len_list[i]= (huff_hash[char], freq)
    return run_len_list

def runlen_elias(run_len_list):
    for i in range(len(run_len_list)):
        char_enc, freq = run_len_list[i]
        #print(freq)
        run_len_list[i] = (char_enc,elias_omega_encode(freq))
    return run_len_list

def q2(string):
    # 1. BWT of the input string
    bwt_string = naive_bwt_enc(string)
    bwt_str_len = len(bwt_string)
    encoded_n = elias_omega_encode(bwt_str_len)

    # 2. Huffman encode the characters -> uniq_chars -> elias encode
    huff_heap, uniq_chars, huff_encode = huffman_tree(bwt_string)
    #print(huff_encode)
    # number of distinct characters in the BWT string,
    # encoded using its corresponding Elias Omega codeword.
    encoded_unique_chars = elias_omega_encode(uniq_chars)
    #print(uniq_chars)


    # 3. 
    # 7-bit ASCII code word
    # print(huff_heap[0][1])
    bit7_ascii = get_7bit_ascii_codes(huff_heap[0][1])
    #print(huff_heap[0][1])
    #print(bit7_ascii)
    

    # length of its constructed Huffman code word,
    # length is encoded - Elias Omega integer codeword,
    elias_huff_code = elias_omega_huff_code(huff_encode)
    #print(elias_huff_code)

    # huff_encode = Huffman codeword you computed for that character


    # 4. Each runlength encoded tuple derived on the BWT string 
    # Huffman codeword of the character being encoded by run length
    run_len_list = run_len_enc(bwt_string)
    #print(run_len_list)
    run_len_huff_enc = runlen_huff(run_len_list, huff_encode)
    #print(run_len_huff_enc)
    run_len_elias = runlen_elias(run_len_huff_enc)
    #print(run_len_elias)

    #print(encoded_n)
    #Length(bwt) = 7 => EliasCode(7) = 000111
    #nUniqChars(bwt) = 4 = 000100
    final_bitstream = bitarray()
    
    final_bitstream.extend(encoded_n)
    
    final_bitstream.extend(encoded_unique_chars)
    
    # print(huff_encode)
    # Add the ASCII and Elias Omega encoded lengths for each unique character
    for char in huff_heap[0][1]:
        final_bitstream.extend(bit7_ascii[char])
        # print(char)
        # print(bit7_ascii[char])
        final_bitstream.extend(elias_huff_code[char]) 
        # print(elias_huff_code[char])
        # print(final_bitstream)
        # print(huff_encode[char])
        final_bitstream.extend(huff_encode[char])
        # print(final_bitstream)
        

     # Add the encoded run-length tuples
    for char_enc, freq_enc in run_len_elias:
        final_bitstream.extend(char_enc)
        #print(final_bitstream)
        final_bitstream.extend(freq_enc)
        
    #print(final_bitstream)   
    
    
    #pad the bitarray to be multiples of 8
    final_bitstream.fill()
    #print(final_bitstream)

    # Convert to bytes
    packed_bytes = final_bitstream.tobytes()

    return packed_bytes
    

    # Elias Omega encode the lengths of runs and the length of the BWT string
    

def read_file(filename):
    """Read the contents of the file."""
    with open(filename, 'r') as file:
        return file.read()

# Rest of the script to read files and write the output remains the same

def write_to_output(filename, ranks):
    """Write the lexicographic ranks to the output file."""
    with open(filename, 'w') as file:
        for rank in ranks:
            file.write(f"{rank}\n")

def main(string_filename):
    # Read the input string and positions from the files
    input_string = read_file(string_filename)
    res = q2(input_string)
    #print(res)
    write_to_output('q2_encoder_output.bin', res)  

if __name__ == "__main__":
    
    string = "banana$"
    #q2(string)

    string_filename = sys.argv[1]
    main(string_filename)







   
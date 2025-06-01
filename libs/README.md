
# Baabnq Libraries
This is a collection of Baabnq standard libraries and their respective unit tests.
All libraries expect to be included like so: ```use 'libs/<library>.baabnq'```

### File Descriptions
- **chunk.baabnq**: operations for heap chunks
- **fast.baabnq**: low level / assembler routines optimized for speed
- **float.baanq**: floating-point implementation based on bfloat16 and respective mathematical operations
- **math.baabnq**: mathematical operations for integers
- **no.baabnq**: panic, stack dumping, and other exception handling utilities
- **rand.baabnq**: pseudo-random number generator
- **stack.baabnq**: atomic stack operations
- **string.baabq**: string handling operations, assuming strings are null-terminated
- **trig.baabq**: trigonometric function approximations
- **twoc.baabnq**: two's complement operations

### Data Structures

#### Integers / Pointers
Integers are always 16-bit unsigned words that may also act as pointers into memory.

#### Chunks
A chunk is a continuous part of heap memory, allocated and managed by the virtual machine. The Baabnq compiler extends them by making chunks always behave like pascal strings, storing the length before the regular start of the chunk. Therefore, they are usually not null-terminated, unless they store a string. Chunks can be directly allocated in Baabnq like this:    
```new <size of chunk> _ptr;```
Chunks may also be statically (compile-time) allocated:    
```static <size of chunk> _ptr;```
This makes the chunk immutable.

#### Strings
Strings are null-terminated chunks. Like chunks, they can also be heap allocated directly in baabnq:    
```new '<string>' _ptr;```   
```static '<string>' _ptr;```
Thus, each node only stores one word, which may be used to point to another structure.

#### Floats
Floats (in routine signatures: Float16) are floating-point values, based on the [bfloat16 format](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format). Each float is based on an integer 16-bit word, where the assignment looks like this:
| 16 (msb) |  15 - 8  | 7 - 1 (lsb) |
| -------- | -------- | ----------- |
| sign     | exponent |   mantissa  |

The only difference between bfloat16 and this implementation is that the exponent does not have bias, but instead uses two's complement. 
This, however, does not affect the external usage or function of the library.


